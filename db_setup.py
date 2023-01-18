import configparser
import os
import sys
import xml.etree.ElementTree
import zipfile
from pathlib import Path
from statistics import mean

import mysql.connector
import openpyxl
from PIL import Image
from PIL import ImageStat


def connexionBDD():
    try:
        config = configparser.RawConfigParser()
        config.read('config.ini')
        conn = mysql.connector.connect(
            host=config.get('settings', 'host'),
            user=config.get('settings', 'username'),
            passwd=config.get('settings', 'password'),
        )
        return conn
    except Exception as e:
        print("Erreur lors de la connexion à la BDD: " + str(e))
        sys.exit(1)


def creationBDD(conn):
    try:
        cursor = conn.cursor()
        config = configparser.RawConfigParser()
        config.read('config.ini')
        db_name = config.get('settings', 'database')
        cursor.execute("DROP DATABASE IF EXISTS " + db_name)
        cursor.execute("CREATE DATABASE " + db_name)
        with open("bdd.sql") as sql:
            cursor.execute("USE " + db_name)
            cursor.execute(sql.read())
    except Exception as e:
        print("Erreur lors de la création de la BDD." + str(e))
        sys.exit(1)


def calcul_score_proprete(image):
    try:
        img_stats = ImageStat.Stat(image)
        return img_stats.mean[0]
    except ZeroDivisionError:
        print("L'image ne possède pas assez de pixels")
        sys.exit(1)


def insererPageBDD(conn, id_image, id_dossier, score_image, triplet, hg, hm, hd, bg, bm, bd):
    cursor = conn.cursor()
    config = configparser.RawConfigParser()
    config.read('config.ini')
    db_name = config.get('settings', 'database')
    cursor.execute("USE " + db_name)
    try:
        cursor.execute("""INSERT INTO page (page_id, fascicule_id, niveau_gris) VALUES (%s, %s, %s);""",
                       (id_image, id_dossier, score_image))
        cursor.execute("""INSERT INTO triplet (page_id, point_noir, point_blanc, gamma) VALUES (%s, %s, %s, %s);""",
                       (id_image, triplet[0], triplet[1], triplet[2]))
        cursor.execute(
            """INSERT INTO matrice (page_id, haut_gauche, haut_milieu, haut_droite, bas_gauche, bas_milieu, 
            bas_droite) VALUES (%s, %s, %s, %s, %s, %s, %s);""",
            (id_image, hg, hm, hd, bg, bm, bd))
        conn.commit()
    except mysql.connector.errors.DataError as e:
        print(e, " : ", id_image, " : ", score_image)
        conn.rollback()


def decoupe_mot(word):
    decalage_gauche = int(word.attrib.get("width")) / 3
    decalage_haut = int(word.attrib.get("height")) / 3

    gauche = int(word.attrib.get("left")) - decalage_gauche
    haut = int(word.attrib.get("top")) - decalage_haut
    droite = int(word.attrib.get("right"))
    bas = int(word.attrib.get("bottom"))

    if gauche >= droite:
        droite += 20
    if haut >= bas:
        bas += 20

    return gauche, haut, droite, bas


def decoupe_matrice(word, im):
    decalage_gauche = int(word.attrib.get("width")) / 3
    decalage_haut = int(word.attrib.get("height")) / 3

    gauche = int(word.attrib.get("left")) - decalage_gauche
    haut = int(word.attrib.get("top")) - decalage_haut
    droite = int(word.attrib.get("right"))
    bas = int(word.attrib.get("bottom"))

    if gauche >= droite:
        droite += 20
    if haut >= bas:
        bas += 20

    return im.crop((gauche, haut, droite, bas))


def decoupe_matrice_2_par_3(word, im):
    mot = decoupe_mot(word)
    hauteur_mot = mot[1] - mot[3]
    largeur_mot = mot[0] - mot[2]

    rectangle_hg = (mot[0], mot[1], mot[0] - largeur_mot / 3, mot[1] - hauteur_mot / 2)
    rectangle_hm = (mot[0] - largeur_mot / 3, mot[1], mot[0] - (largeur_mot / 3) * 2, mot[1] - hauteur_mot / 2)
    rectangle_hd = (mot[0] - (largeur_mot / 3) * 2, mot[1], mot[2], mot[1] - hauteur_mot / 2)
    rectangle_bg = (mot[0], mot[1] - hauteur_mot / 2, mot[0] - largeur_mot / 3, mot[3])
    rectangle_bm = (mot[0] - largeur_mot / 3, mot[1] - hauteur_mot / 2, mot[0] - (largeur_mot / 3) * 2, mot[3])
    rectangle_bd = (mot[0] - (largeur_mot / 3) * 2, mot[1] - hauteur_mot / 2, mot[2], mot[3])

    return (im.crop(mot), im.crop(rectangle_hg), im.crop(rectangle_hm), im.crop(rectangle_hd), im.crop(rectangle_bg),
            im.crop(rectangle_bm), im.crop(rectangle_bd))


def score_global_matrice(tab_score_mots_matrice):
    somme_hg, somme_hm, somme_hd, somme_bg, somme_bm, somme_bd = ([] for _ in range(6))
    for mot in tab_score_mots_matrice:
        somme_hg.append(mot[0])
        somme_hm.append(mot[1])
        somme_hd.append(mot[2])
        somme_bg.append(mot[3])
        somme_bm.append(mot[4])
        somme_bd.append(mot[5])

    return mean(somme_hg), mean(somme_hm), mean(somme_hd), mean(somme_bg), mean(somme_bm), mean(somme_bd)


def remplirBDD(conn):
    xlsx_file = Path('datas/Triplets.xlsx')
    wb_obj = openpyxl.load_workbook(xlsx_file)
    sheet = wb_obj.active

    mot_choisi = "de"

    fascicules = os.path.join(os.getcwd(), "datas", "Fascicules")
    ocr = os.path.join(os.getcwd(), "datas", "OCR")

    for dossier in os.listdir(fascicules):
        if os.path.isdir(os.path.join(fascicules, dossier)):
            for filename in os.listdir(os.path.join(fascicules, dossier, "Pages_volume", "GreyScale")):
                if filename.endswith(".png"):
                    chemin_file = os.path.join(fascicules, dossier, "Pages_volume", "GreyScale", filename)
                    im = Image.open(chemin_file)

                    chemin_ocr = os.path.join(ocr, dossier, filename.replace(".png", " - ocr.zip"))
                    archive = zipfile.ZipFile(chemin_ocr, 'r')
                    try:
                        imgdata = archive.open(filename.replace(".png", ".xml"))
                        arbre_xml = xml.etree.ElementTree.parse(imgdata)
                        racine = arbre_xml.getroot()
                        tab_score_mots = []
                        tab_score_mots_matrice = []
                        for word in racine.iter("word"):
                            if word.attrib.get("searchWord") == mot_choisi:
                                mot_decoupe = decoupe_matrice(word, im)
                                tab_score_mots.append(calcul_score_proprete(mot_decoupe))

                                mat = decoupe_matrice_2_par_3(word, im)
                                tab_score_mots_matrice.append(
                                    (calcul_score_proprete(mat[0]), calcul_score_proprete(mat[1]),
                                     calcul_score_proprete(mat[2]), calcul_score_proprete(mat[3]),
                                     calcul_score_proprete(mat[4]),
                                     calcul_score_proprete(mat[5])))

                        if tab_score_mots:
                            stockage_scores = mean(tab_score_mots)
                        else:
                            stockage_scores = 0.0

                        if tab_score_mots_matrice:
                            moyennes_matrice = score_global_matrice(tab_score_mots_matrice)
                        else:
                            moyennes_matrice = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                        for row in sheet.iter_rows(min_row=4, max_row=33):
                            if row[0].value == dossier:
                                insererPageBDD(conn, filename.replace(".png", ""), dossier,
                                               stockage_scores,
                                               [str(row[2].value), str(row[3].value), str(row[4].value)],
                                               moyennes_matrice[0],
                                               moyennes_matrice[1],
                                               moyennes_matrice[2],
                                               moyennes_matrice[3],
                                               moyennes_matrice[4],
                                               moyennes_matrice[5])

                        imgdata.close()
                    except KeyError:
                        print("ERROR")
                    archive.close()
                    im.close()


bdd = connexionBDD()
#creationBDD(bdd)
remplirBDD(bdd)