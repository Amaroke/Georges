import configparser
import os
import sys
import xml.etree.ElementTree
import zipfile
from pathlib import Path
from statistics import mean
import mysql.connector
import mysql.connector
import openpyxl
from PIL import Image
from PIL import ImageStat


def connexionBDD():
    try:
        # Création de l'objet de configuration pour lire le fichier config.ini.
        config = configparser.RawConfigParser()
        config.read('config.ini')

        # Connexion à la base de données en utilisant les informations de connexion
        # lues dans le fichier config.ini.
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

        # Suppression de la base de données si elle existe déjà.
        cursor.execute("DROP DATABASE IF EXISTS " + db_name)

        # Création de la base de données.
        cursor.execute("CREATE DATABASE " + db_name)

        # Utilisation de la base de données créée.
        cursor.execute("USE " + db_name)

        # Exécution du script SQL pour initialiser la structure de la base de données.
        with open("bdd.sql") as sql:
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


def insererPageBDD(conn, id_image, id_fascicule, niveau_gris, triplet, hg, hm, hd, bg, bm, bd):
    cursor = conn.cursor()
    config = configparser.ConfigParser()
    config.read('config.ini')
    db_name = config.get('settings', 'database')
    cursor.execute("USE " + db_name)
    try:
        cursor.execute("""INSERT INTO page (page_id, fascicule_id, niveau_gris) VALUES (%s, %s, %s);""",
                       (id_image, id_fascicule, niveau_gris))
        cursor.execute("""INSERT INTO triplet (page_id, point_noir, point_blanc, gamma) VALUES (%s, %s, %s, %s);""",
                       (id_image, triplet[0], triplet[1], triplet[2]))
        cursor.execute(
            """INSERT INTO matrice (page_id, haut_gauche, haut_milieu, haut_droite, bas_gauche, bas_milieu, 
            bas_droite) VALUES (%s, %s, %s, %s, %s, %s, %s);""",
            (id_image, hg, hm, hd, bg, bm, bd))
        conn.commit()
    except mysql.connector.errors.DataError as e:
        print(e, " : ", id_image, " : ", niveau_gris)
        conn.rollback()


def decoupe_mot(word):
    # Calcul des décalages à appliquer aux coordonnées du mot.
    decalage_gauche = int(word.attrib.get("width")) / 3
    decalage_haut = int(word.attrib.get("height")) / 3

    # Calcul des coordonnées de la zone découpée.
    gauche = int(word.attrib.get("left")) - decalage_gauche
    haut = int(word.attrib.get("top")) - decalage_haut
    droite = int(word.attrib.get("right"))
    bas = int(word.attrib.get("bottom"))

    # Vérification des limites de la zone découpée.
    if gauche >= droite:
        droite += 20
    if haut >= bas:
        bas += 20

    return gauche, haut, droite, bas


def decoupe_matrice(word, im):
    # Calcul des décalages à appliquer aux coordonnées du mot
    decalage_gauche = int(word.attrib.get("width")) / 3
    decalage_haut = int(word.attrib.get("height")) / 3

    # Calcul des coordonnées de la zone découpée
    gauche = int(word.attrib.get("left")) - decalage_gauche
    haut = int(word.attrib.get("top")) - decalage_haut
    droite = int(word.attrib.get("right"))
    bas = int(word.attrib.get("bottom"))

    # Vérification des limites de la zone découpée
    if gauche >= droite:
        droite = gauche + 20
    if haut >= bas:
        bas = haut + 20

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
    somme_hg, somme_hm, somme_hd, somme_bg, somme_bm, somme_bd = [], [], [], [], [], []
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
                        print('Un fascicule ne contenait pas le mot "de"')
                    archive.close()
                    im.close()


def remplirBDDAnalogie(conn):
    cursor = conn.cursor()
    config = configparser.RawConfigParser()
    config.read('config.ini')
    db_name = config.get('settings', 'database')
    cursor.execute("USE " + db_name)

    # Requête qui récupère toutes les pages dont le page_id commence par 0011 ou 0012.
    requete = """SELECT * FROM page WHERE page_id LIKE '%0011%' OR page_id LIKE '%0012%'"""
    cursor.execute(requete)
    resultat = cursor.fetchall()

    # Pour chaque page, on récupère les informations nécessaires.
    for row in resultat:
        page_id = row[0]
        niveau_gris = row[2]
        cursor.execute("""SELECT * FROM triplet WHERE page_id LIKE '""" + page_id + "'")
        resultat2 = cursor.fetchall()
        point_noir = resultat2[0][2]
        point_blanc = resultat2[0][3]
        gamma = resultat2[0][4]

        # On fait de même pour la deuxième page et on entre les données dans la BDD.
        for row2 in resultat:
            page_id2 = row2[0]
            niveau_gris2 = row2[2]
            cursor.execute("""SELECT * FROM triplet WHERE page_id LIKE '""" + page_id2 + "'")
            resultat3 = cursor.fetchall()
            point_noir2 = resultat3[0][2]
            point_blanc2 = resultat3[0][3]
            gamma2 = resultat3[0][4]
            try:
                # On calcule la difference entre les donnees des deux pages.
                reference = (page_id, page_id2, niveau_gris - niveau_gris2, point_noir - point_noir2,
                             point_blanc - point_blanc2, gamma - gamma2)
                # On insère cette différence dans la table analogie.
                cursor.execute(
                    """INSERT INTO analogie (page1, page2, difference_niveau_gris, difference_point_noir, 
                    difference_point_blanc, difference_gamma) VALUES(%s, %s, %s, %s, %s, %s)""",
                    reference)
                conn.commit()
            except mysql.connector.errors.DataError as e:
                print(e, " : ", row[0], " : ", row2[0])
                conn.rollback()


bdd = connexionBDD()
choix = input("Que voulez vous faire ?\n"
              "1. Réinitialiser la Base de Données.\n"
              "2. Remplir la BDD avec les fascicules et OCR fournis.\n"
              "3. Remplir la BDD avec les analogies.\n"
              "Choisir toute autre option pour quitter le programme.\n"
              "Votre choix : ")
if choix == "1":
    verification = input('Veuillez confirmer (saisissez "Je confirme la réinitialisation de la BDD") : ')
    if verification == "Je confirme la réinitialisation de la BDD":
        creationBDD(bdd)
        print("Réinitialisation de la BDD effectuée.")
    else:
        print("Abandon de la procédure.")
elif choix == "2":
    remplirBDD(bdd)
elif choix == "3":
    remplirBDDAnalogie(bdd)
else:
    print("Abandon du programme.")
    bdd.close()
