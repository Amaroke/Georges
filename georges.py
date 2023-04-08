import configparser
import math
import os
import sys
import xml.etree.ElementTree as ET
import zipfile
from statistics import mean

import mysql.connector
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


# Fonction qui crée un curseur sur la BDD et le place au bon endroit
def setup_curseur(conn):
    cursor = conn.cursor()
    config = configparser.ConfigParser()
    config.read('config.ini')
    db_name = config.get('settings', 'database')
    cursor.execute("USE " + db_name)
    return cursor


# Fonction qui donne les coordonnées autour d'un mot (ajustement des coordonnées de l'OCR).
def decoupe_mot(word):
    # Ajustement des coordonnées de l'OCR choisi arbitrairement après des tests 'à la main'.
    # On décale à gauche et en haut car l'OCR coupe le mot 'de' avec le coin haut-gauche.
    decalage_gauche = int(word.attrib.get("width")) / 3
    decalage_haut = int(word.attrib.get("height")) / 3

    gauche = int(word.attrib.get("left")) - decalage_gauche
    haut = int(word.attrib.get("top")) - decalage_haut
    droite = int(word.attrib.get("right"))
    bas = int(word.attrib.get("bottom"))

    # On gère les cas ou l'OCR donne des coordonnées incorrectes
    if gauche >= droite:
        droite += 20
    if haut >= bas:
        bas += 20

    return gauche, haut, droite, bas


# Fonction qui découpe la matrice autour d'un mot en une matrice 1*1 et en retourne l'image en résultant.
def decoupe_matrice(word):
    return im.crop(decoupe_mot(word))


# Fonction qui découpe la matrice autour d'un mot en une matrice 2*3 et en retourne les images en résultant.
def decoupe_matrice_2_par_3(word):
    # On récupère les coordonnées de la bounding box du mot
    mot = decoupe_mot(word)
    hauteur_mot = mot[1] - mot[3]
    largeur_mot = mot[0] - mot[2]

    # On découpe ces coordonnées en une matrice 2*3.
    rectangle_hg = (mot[0], mot[1], mot[0] -
                    largeur_mot / 3, mot[1] - hauteur_mot / 2)
    rectangle_hm = (mot[0] - largeur_mot / 3, mot[1], mot[0] -
                    (largeur_mot / 3) * 2, mot[1] - hauteur_mot / 2)
    rectangle_hd = (mot[0] - (largeur_mot / 3) * 2, mot[1],
                    mot[2], mot[1] - hauteur_mot / 2)
    rectangle_bg = (mot[0], mot[1] - hauteur_mot / 2,
                    mot[0] - largeur_mot / 3, mot[3])
    rectangle_bm = (mot[0] - largeur_mot / 3, mot[1] -
                    hauteur_mot / 2, mot[0] - (largeur_mot / 3) * 2, mot[3])
    rectangle_bd = (mot[0] - (largeur_mot / 3) * 2,
                    mot[1] - hauteur_mot / 2, mot[2], mot[3])

    return (im.crop(mot), im.crop(rectangle_hg), im.crop(rectangle_hm), im.crop(rectangle_hd), im.crop(rectangle_bg),
            im.crop(rectangle_bm), im.crop(rectangle_bd))


# Fonction qui calcule le score de propreté de l'image envoyé.
def calcul_moyenne_image(image):
    # on récupère la moyenne des pixels (moyenne arithmétique des valeurs des pixels) de l'image.
    img_stats = ImageStat.Stat(image)
    return img_stats.mean[0]


# Fonction qui calcule la moyenne globale à partir de toutes les moyennes de la page.
def moyenne_globale(tab_score_mots):
    return mean(tab_score_mots)


# Fonction qui calcule la somme des différences entre 2 matrices (2*3)
def calcul_somme_diff_matrice_dist1(m1, m2):
    return abs(m1[0] - m2[0]) + abs(m1[1] - m2[1]) + abs(m1[2] - m2[2]) + abs(m1[3] - m2[3]) + abs(m1[4] - m2[4]) + abs(
        m1[5] - m2[5])


def calcul_somme_diff_matrice_dist2(m1, m2):
    return math.sqrt((m1[0] - m2[0]) ** 2 + (m1[1] - m2[1]) ** 2 + (m1[2] - m2[2]) ** 2 + (m1[3] - m2[3]) ** 2 + (
            m1[4] - m2[4]) ** 2 + (m1[5] - m2[5]) ** 2)


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


def recupere_x_plus_proches_1x1(x_plus_proches, cursor, id_page, ng_page, fascicule_id):
    tab = []
    requete = """SELECT page_id, niveau_gris 
        FROM page 
        WHERE page_id != %s AND fascicule_id != %s
        ORDER BY ABS(niveau_gris - %s) ASC 
        LIMIT %s"""
    cursor.execute(requete, (id_page, fascicule_id, ng_page, x_plus_proches))
    for row in cursor:
        tab.append(row)
    return tab


def recupere_x_plus_proches_2x3(x_plus_proches, cursor, id_page, matrice_page, fascicule_id):
    tab = []
    requete = """SELECT P.page_id, haut_gauche, haut_milieu, haut_droite, bas_gauche, bas_milieu, bas_droite 
        FROM page P, matrice M 
        WHERE P.page_id = M.page_id AND P.page_id != %s AND P.fascicule_id != %s
        ORDER BY SQRT(POW(haut_gauche - %s, 2) + POW(haut_milieu - %s, 2) + POW(haut_droite - %s, 2) + POW(bas_gauche - %s, 2) + POW(bas_milieu - %s, 2) + POW(bas_droite - %s, 2)) ASC 
        LIMIT %s"""
    cursor.execute(requete, (
        id_page, fascicule_id, matrice_page[0], matrice_page[1], matrice_page[2], matrice_page[3], matrice_page[4],
        matrice_page[5], x_plus_proches))
    for row in cursor:
        tab.append(row)
    return tab


def calcul_diff_matrice(m1, m2):
    return (m1[0] - m2[0]), (m1[1] - m2[1]), (m1[2] - m2[2]), (m1[3] - m2[3]), (m1[4] - m2[4]), (m1[5] - m2[5])


def produit_scalaire(m1, m2):
    return m1[0] * m2[0] + m1[1] * m2[1] + m1[2] * m2[2] + m1[3] * m2[3] + m1[4] * m2[4] + m1[5] * m2[5]


def distance_itgt_h(b, c, tgt):
    # On calcule l'aire du triangle
    A = calcul_aire_triangle(b, c, tgt)

    # On calcule la distance de itgt à h
    return 2 * A / calcul_somme_diff_matrice_dist2(b, c)


def calcul_aire_triangle(b, c, tgt):
    # On utilise la formule d'Héron

    # On calcule d'abord les longueurs des 3 côtés du triangle
    l = calcul_somme_diff_matrice_dist2(b, c)
    m = calcul_somme_diff_matrice_dist2(c, tgt)
    n = calcul_somme_diff_matrice_dist2(b, tgt)

    # On calcule ensuite le demi périmètre
    p = (l + m + n) / 2

    # On calcule enfin l'aire du triangle
    return math.sqrt(p * (p - l) * (p - m) * (p - n))


def distance_b_h(b, tgt, distance_itgt_h):
    # On calcule la distance de ib à h
    return math.sqrt(calcul_somme_diff_matrice_dist2(b, tgt) ** 2 - distance_itgt_h ** 2)


def calcul_barycentre(b, c, dist_b_h, dist_b_c):
    return b + (c - b) * (dist_b_h / dist_b_c)


def inverse(m):
    return (-m[0], -m[1], -m[2], -m[3], -m[4], -m[5])


# Initialisation des variables constantes utilisée dans tout le fichier
id_fascicule = input("Donnez moi l'id du fascicule à analyser : ")
# Peut être remplacé par un input mais il faut modifier la bdd (stocker les valeurs correspondant
mot_choisi = "de"
# à cet input)

chemin = os.path.join(os.getcwd(), "datas", "Fascicules",
                      id_fascicule, "Pages_volume", "GreyScale")
chemin_archive = os.path.join(os.getcwd(), "datas", "OCR", id_fascicule)

# Initialisations des structures de données et variables nécessaires au stockage de données sur les images.
tab_moyennes = []
tab_moyennes_matrice = []
tab_fichiers_traites = []
i = 0
cpt_erreur = 0
# Parcours de toutes les images cibles.
for filename in os.listdir(chemin):
    if filename.endswith(".png"):
        # On ouvre l'image
        chemin_file = os.path.join(chemin, filename)
        im = Image.open(chemin_file)

        # On ouvre le .zip contenant le fichier .xml
        chemin_ocr = os.path.join(
            chemin_archive, filename.replace(".png", " - ocr.zip"))
        archive = zipfile.ZipFile(chemin_ocr, 'r')
        try:
            # Ouverture du .xml
            imgdata = archive.open(filename.replace(".png", ".xml"))

            # Traitement du .xml
            arbre_xml = ET.parse(imgdata)
            racine = arbre_xml.getroot()
            tab_score_mots = []
            tab_score_mots_matrice = []

            # Parcours du .xml (on cherche les mots).
            for word in racine.iter("word"):
                if word.attrib.get("searchWord") == mot_choisi:
                    # Possibilité d'enlever les mots en gras ou en italique (pas eu le temps de tester).

                    # NGU & ANA
                    # On découpe le mot de l'image et on calcule la moyenne dessus.
                    mot_decoupe = decoupe_matrice(word)
                    tab_score_mots.append(calcul_moyenne_image(mot_decoupe))

                    # MAT
                    # On découpe en matrice 2*3 le mot et on calcule les moyennes sur cette matrice.
                    mat = decoupe_matrice_2_par_3(word)
                    tab_score_mots_matrice.append((calcul_moyenne_image(mat[0]), calcul_moyenne_image(mat[1]),
                                                   calcul_moyenne_image(
                                                       mat[2]), calcul_moyenne_image(mat[3]),
                                                   calcul_moyenne_image(mat[4]), calcul_moyenne_image(mat[5])))

            # NGU & ANA
            # On fait la moyenne des moyennes pour trouver le "mot moyen"
            if tab_score_mots:
                tab_moyennes.append(moyenne_globale(tab_score_mots))
            else:
                tab_moyennes.append(0.0)

            # MAT
            # On fait la moyenne des moyennes des matrices.
            if tab_score_mots_matrice:
                tab_moyennes_matrice.append(
                    score_global_matrice(tab_score_mots_matrice))
            else:
                tab_moyennes_matrice.append((0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

            # Stockage des fichiers traités (à supprimer si on veut traiter fichier par fichier)
            tab_fichiers_traites.append(filename)
            i += 1
        except KeyError:
            cpt_erreur += 1
        im.close()
        imgdata.close()
        archive.close()

# Détection d'erreurs
if cpt_erreur == 0:
    print("Images analysées avec succès, recherche des pages similaires en cours !")
else:
    print("Images analysées avec ", cpt_erreur,
          "erreurs detectées (les erreurs indiquent que les fichiers dans les archives ont des noms différents de "
          "l'image !")
    exit(4)

#####################################
# Méthode par niveau de gris unique #
#####################################

# NGU & ANA
# On regarde les correspondance dans la bdd (création de la requête)
requete = """(select P.page_id, niveau_gris, point_noir, point_blanc, gamma 
                from page as P, triplet as T 
                where P.page_id = T.page_id AND niveau_gris >= %s and P.fascicule_id != %s 
                order by niveau_gris asc limit 1) 
            union 
             (select P.page_id, niveau_gris, point_noir, point_blanc, gamma 
                from page as P, triplet as T 
                where P.page_id = T.page_id AND niveau_gris < %s and P.fascicule_id != %s 
                order by niveau_gris desc limit 1)
            order by abs(niveau_gris - %s) limit 1 """

# Connexion à la BDD
conn = connexionBDD()
cursor = setup_curseur(conn)

# On commence par la méthode par niveaux de gris simples.
# Ouverture des fichiers dans lesquels on écrit la sortie du programme
fichier_reponses = open("reponses.txt", "w")

stockage_triplets = dict()
stockage_reponse_score = dict()
# On recherche le fichier le plus similaire à chaque page du fascicule cible et on écrit la réponse dans le fichier
# réponse.
for i in range(len(tab_fichiers_traites)):
    cursor.execute(
        requete, (tab_moyennes[i], id_fascicule, tab_moyennes[i], id_fascicule, tab_moyennes[i]))
    row = cursor.fetchone()
    triplet_string = "(" + str(row[2]) + ", " + \
                     str(row[3]) + ", " + str(row[4]) + ")"
    fichier_reponses.write(
        tab_fichiers_traites[i] + " -> " + triplet_string + "\n")
    stockage_triplets[tab_fichiers_traites[i]] = triplet_string
    stockage_reponse_score[tab_fichiers_traites[i]] = (row[1], triplet_string)

fichier_reponses.close()
print("Recherche par niveau de gris basique terminée, résultats écrits dans le fichier 'reponses.txt'.")

#######################
# Méthode par matrice #
#######################

# MAT
# On passe à la méthode par matrice
fichier_reponses_2 = open("reponses2.txt", "w")

requete = """select P.page_id, point_noir, point_blanc, gamma, haut_gauche, haut_milieu, haut_droite, bas_gauche, bas_milieu, bas_droite, fascicule_id 
                from page as P, matrice as M, triplet as T 
                where P.page_id = T.page_id AND P.page_id = M.page_id """

# On se replace au début de la BDD.
cursor = setup_curseur(conn)
cursor.execute(requete)

# Déclaration des tableau nécessaires au parcours
matrice_calcul = []
matrice_proche = []
matrice_triplet = []
# Initialisation des tableau nécessaires au parcours
for i in range(len(tab_fichiers_traites)):
    matrice_calcul.append(sys.maxsize)
    matrice_proche.append("")
    matrice_triplet.append("")

# On récupère toutes les données des matrices de la BDD et on cherche pour chaque fichier la plus proche.
est_termine = False
while not est_termine:
    # On en récupère 1000 par 1000 pour ne pas surcharger la mémoire.
    rows = cursor.fetchmany(1000)
    if not rows:
        est_termine = True
    else:
        for row in rows:
            if not (row[10] == id_fascicule):  # On exclue le fascicule cible.
                for i in range(len(tab_fichiers_traites)):
                    temp = calcul_somme_diff_matrice_dist1(tab_moyennes_matrice[i], (
                        float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9])))
                    # Si la matrice est plus proche que celles précédentes, on la stocke.
                    if temp < matrice_calcul[i]:
                        matrice_calcul[i] = temp
                        matrice_proche[i] = row[0]
                        matrice_triplet[i] = "(" + str(row[1]) + \
                                             ", " + str(row[2]) + ", " + str(row[3]) + ")"

stockage_triplets_v2 = dict()
# On écrit les réponses dans le second fichier réponses.
for i in range(len(tab_fichiers_traites)):
    fichier_reponses_2.write(
        tab_fichiers_traites[i] + " -> " + matrice_triplet[i] + "\n")
    stockage_triplets_v2[tab_fichiers_traites[i]] = matrice_triplet[i]

fichier_reponses_2.close()
print("Recherche par matrice 2*3 terminée, résultats écrits dans le fichier 'reponses2.txt'.")

########################
# Méthode par analogie 1*1 #
########################

# ANA
fichier_reponses_3 = open("reponses3.txt", "w")

# On prépare les requêtes qui récupèrent les données de la BDD
# TODO : Remplacer par une requête plus efficace, cf requete ANA 2*3.
requete = """(select * 
                from analogie 
                where difference_niveau_gris >= %s and page1 != %s and page2 != %s
                order by difference_niveau_gris asc limit 1) 
            union 
             (select * 
                from analogie 
                where difference_niveau_gris < %s and page1 != %s and page2 != %s
                order by difference_niveau_gris desc limit 1) 
            order by abs(difference_niveau_gris - %s) limit 1 """

# On se replace au début de la BDD.
cursor = setup_curseur(conn)

x_plus_proches = 10
stockage_triplets_v3 = dict()
# On récupère les fichiers les plus proches calculés en approximation 1*1.
for i in range(len(tab_fichiers_traites)):
    tab_x_plus_proches = recupere_x_plus_proches_1x1(x_plus_proches, cursor, tab_fichiers_traites[i], tab_moyennes[i],
                                                     id_fascicule)

    diff_min = sys.maxsize
    diff_temp = 0.0
    tuple_min = ""
    x_min = ["", -1]
    # On récupère la diff_NG qui à la distance la plus petite à tous les couple de la BDD.
    for x in tab_x_plus_proches:
        diff_temp = abs(x[1] - tab_moyennes[i])
        cursor.execute(requete, (diff_temp, tab_fichiers_traites[i], tab_fichiers_traites[i],
                                 diff_temp, tab_fichiers_traites[i], tab_fichiers_traites[i], diff_temp))
        row = cursor.fetchone()
        if row is not None:
            if (abs(diff_temp - float(row[3])) < diff_min):
                diff_min = abs(diff_temp - float(row[3]))
                tuple_min = row
                x_min = x

    # On écrit les réponses dans le troisième fichier réponses.
    triplet = stockage_reponse_score[tab_fichiers_traites[i]][1].replace("(", "").replace(")", "").replace(" ",
                                                                                                           "").split(
        ",")
    pn_analogie = max(int(triplet[0]) + int(tuple_min[4]), 0)
    pb_analogie = min(int(triplet[1]) + int(tuple_min[5]), 255)
    g_analogie = max(float(triplet[2]) + float(tuple_min[6]), 0.0)
    fichier_reponses_3.write(tab_fichiers_traites[i] + " : (" + str(pn_analogie) + ", " + str(pb_analogie) + ", " + str(
        g_analogie) + ") depuis " + str(triplet) + " avec changement de : " + str(int(tuple_min[4])) + ", " + str(
        int(tuple_min[5])) + ", " + str(float(tuple_min[6])) + " | page c choisie : " + x[0] + "\n")
    stockage_triplets_v3[tab_fichiers_traites[i]] = "(" + str(pn_analogie) + ", " + str(pb_analogie) + ", " + str(
        g_analogie) + ")"
fichier_reponses_3.close()

print("Recherche par analogie 1*1 terminée, résultats écrits dans le fichier 'reponses3.txt'.")

############################
# Méthode par analogie 2*3 #
############################

# ANA
fichier_reponses = open("reponses4.txt", "w")

# Requete qui récupère les données de la BDD
requete = """SELECT *
            FROM analogie
            WHERE page1 != %s AND page2 != %s
            ORDER BY 
                ABS(difference_matrices - %s) ASC
            LIMIT 1"""

# On se replace au début de la BDD.
cursor = setup_curseur(conn)

x_plus_proches = 10
stockage_triplets_v4 = dict()
# On récupère les fichiers les plus proches calculés en approximation 2*3.
for i in range(len(tab_fichiers_traites)):
    # On garde le même fonctionnement que pour la méthode 1*1, C = meilleur page des X plus proches.
    tab_x_plus_proches = recupere_x_plus_proches_2x3(x_plus_proches, cursor, tab_fichiers_traites[i],
                                                     tab_moyennes_matrice[i], id_fascicule)

    diff_min = sys.maxsize
    diff_temp = 0.0
    tuple_min = ""
    x_min = ["", -1]
    # On récupère la diff_NG qui à la distance la plus petite à tous les couple de la BDD.
    for x in tab_x_plus_proches:
        diff_temp = calcul_somme_diff_matrice_dist2(tab_moyennes_matrice[i], (x[1], x[2], x[3], x[4], x[5], x[6]))
        cursor.execute(requete, (tab_fichiers_traites[i], tab_fichiers_traites[i], diff_temp))
        row = cursor.fetchone()
        if row is not None:
            if (abs(diff_temp - float(row[3])) < diff_min):
                diff_min = abs(diff_temp - float(row[3]))
                tuple_min = row
                x_min = x

    # On récupère les triplets de la page C.
    triplet = stockage_triplets_v2[tab_fichiers_traites[i]].replace("(", "").replace(")", "").replace(" ", "").split(
        ",")

    # On calcule les pn, pb et gamma de la page TGT.
    pn_analogie = max(int(triplet[0]) + int(tuple_min[4]), 0)
    pb_analogie = min(int(triplet[1]) + int(tuple_min[5]), 255)
    g_analogie = max(float(triplet[2]) + float(tuple_min[6]), 0)

    fichier_reponses.write(tab_fichiers_traites[i] + " : (" + str(pn_analogie) + ", " + str(pb_analogie) + ", " + str(
        g_analogie) + ") depuis " + str(triplet) + " avec changement de : " + str(int(tuple_min[4])) + ", " + str(
        int(tuple_min[5])) + ", " + str(float(tuple_min[6])) + "\n")
    stockage_triplets_v4[tab_fichiers_traites[i]] = "(" + str(pn_analogie) + ", " + str(pb_analogie) + ", " + str(
        g_analogie) + ")"
fichier_reponses.close()

print("Recherche par analogie 2*3 terminée, résultats écrits dans le fichier 'reponses4.txt'.")

#########################################################
# Interpolation donnant contrainte et valeur exacte 1*1 #
#########################################################

requete = """(select P.page_id, niveau_gris, point_noir, point_blanc, gamma 
                from page as P, triplet as T 
                where P.page_id = T.page_id AND niveau_gris >= %s and P.fascicule_id != %s 
                order by niveau_gris asc limit 1) 
            union 
              (select P.page_id, niveau_gris, point_noir, point_blanc, gamma 
                from page as P, triplet as T 
                where P.page_id = T.page_id AND niveau_gris < %s and P.fascicule_id != %s 
                order by niveau_gris desc limit 1) """

# On se replace au début de la BDD.
cursor = setup_curseur(conn)

# On commence par la méthode par niveaux de gris simples.
# Ouverture des fichiers dans lesquels on écrit la sortie du programme
fichier_reponses = open("reponses5.txt", "w")

# On recherche le fichier le plus similaire à chaque page du fascicule cible et on écrit la réponse dans le fichier réponse.
for i in range(len(tab_fichiers_traites)):
    if (tab_moyennes[i] != 0.0):
        cursor.execute(
            requete, (tab_moyennes[i], id_fascicule, tab_moyennes[i], id_fascicule))

        # Contrainte
        row = cursor.fetchone()
        triplet_string_1 = "(" + str(row[2]) + ", " + \
                           str(row[3]) + ", " + str(row[4]) + ")"
        ng_1 = row[1]
        pn_1 = row[2]
        pb_1 = row[3]
        gamma_1 = row[4]
        row = cursor.fetchone()
        triplet_string_2 = "(" + str(row[2]) + ", " + \
                           str(row[3]) + ", " + str(row[4]) + ")"
        ng_2 = row[1]
        pn_2 = row[2]
        pb_2 = row[3]
        gamma_2 = row[4]

        # Intervalle
        t = abs(tab_moyennes[i] - ng_1) / abs(ng_2 - ng_1)
        pn_3 = int((1 - t) * pn_1 + t * pn_2)
        pb_3 = int((1 - t) * pb_1 + t * pb_2)
        gamma_3 = float((1 - t) * gamma_1 + t * gamma_2)
        triplet_string_3 = "(" + str(pn_3) + ", " + \
                           str(pb_3) + ", " + str(gamma_3) + ")"

        fichier_reponses.write(tab_fichiers_traites[i] + " -> " + triplet_string_3 +
                               " -> [" + triplet_string_1 + ", " + triplet_string_2 + "]\n")
    else:
        fichier_reponses.write(
            tab_fichiers_traites[i] + " -> ng = 0 donc pas d'interpolation\n")

fichier_reponses.close()
print("Recherche par interpolation (1*1) terminée, résultats écrits dans le fichier 'reponses5.txt'.")

#####################
# Interpolation 2x3 #
#####################

requete = """select P.page_id, M.haut_gauche, M.haut_milieu, M.haut_droite, M.bas_gauche, M.bas_milieu, M.bas_droite, point_noir, point_blanc, gamma
                from page as P, triplet as T, matrice as M
                where P.page_id = T.page_id AND P.page_id = M.page_id AND P.fascicule_id != %s
                order by SQRT(POW(M.haut_gauche - %s, 2) + POW(M.haut_milieu - %s, 2) + POW(M.haut_droite - %s, 2) + POW(M.bas_gauche - %s, 2) + POW(M.bas_milieu - %s, 2) + POW(M.bas_droite - %s, 2))
                asc limit %s"""

# On se replace au début de la BDD.
cursor = setup_curseur(conn)

# Ouverture des fichiers dans lesquels on écrit la sortie du programme
fichier_reponses = open("reponses6.txt", "w")

x = 20
# cf. explication dans le rapport
for i in range(len(tab_fichiers_traites)):
    cursor.execute(requete, (
        id_fascicule, tab_moyennes_matrice[i][0], tab_moyennes_matrice[i][1], tab_moyennes_matrice[i][2],
        tab_moyennes_matrice[i][3], tab_moyennes_matrice[i][4], tab_moyennes_matrice[i][5], x))

    # On récupère les X pages les plus proches
    tab_x_plus_proches = []
    for row in cursor:
        tab_x_plus_proches.append(row)

    # On forme tous les couples possibles saufs ceux composés de 2 fois la même page entre les X pages les plus proches
    tab_couples = []
    for j in range(len(tab_x_plus_proches)):
        for k in range(len(tab_x_plus_proches)):
            if tab_x_plus_proches[j][0] != tab_x_plus_proches[k][0]:
                tab_couples.append((tab_x_plus_proches[j], tab_x_plus_proches[k]))

    # On vérifie les couples valides en calculant les produits sclaires.
    tab_couples_valides = []
    for couple in tab_couples:
        matrice_couple_b = (couple[0][1], couple[0][2], couple[0][3], couple[0][4], couple[0][5], couple[0][6])
        matrice_couple_c = (couple[1][1], couple[1][2], couple[1][3], couple[1][4], couple[1][5], couple[1][6])
        diff_couple = calcul_diff_matrice(matrice_couple_c, matrice_couple_b)
        if produit_scalaire(diff_couple,
                            calcul_diff_matrice(tab_moyennes_matrice[i], matrice_couple_b)) > 0 and produit_scalaire(
            inverse(diff_couple), calcul_diff_matrice(tab_moyennes_matrice[i], matrice_couple_c)) > 0:
            tab_couples_valides.append(couple)

    # On calcule les distances itgt à h pour chaque couple valide, on ne retiens que le couple avec la plus petite distance.
    dist_min = sys.maxsize
    couple_min = None
    for couple in tab_couples_valides:
        matrice_couple_b = (couple[0][1], couple[0][2], couple[0][3], couple[0][4], couple[0][5], couple[0][6])
        matrice_couple_c = (couple[1][1], couple[1][2], couple[1][3], couple[1][4], couple[1][5], couple[1][6])
        dist = distance_itgt_h(matrice_couple_b, matrice_couple_c, tab_moyennes_matrice[i])
        if dist < dist_min:
            dist_min = dist
            couple_min = couple

    # On calcule la distance ib à h pour le couple avec la plus petite distance.
    matrice_couple_b = (
        couple_min[0][1], couple_min[0][2], couple_min[0][3], couple_min[0][4], couple_min[0][5], couple_min[0][6])
    dist_b_h = distance_b_h(matrice_couple_b, tab_moyennes_matrice[i], dist_min)
    dist_b_c = calcul_somme_diff_matrice_dist2(matrice_couple_b, (
        couple_min[1][1], couple_min[1][2], couple_min[1][3], couple_min[1][4], couple_min[1][5], couple_min[1][6]))

    # On applique l'interpolation sur les triplets pour obtenir une contrainte et une valeur exacte du triplet.
    # Contrainte
    triplet_string_b = "(" + str(couple_min[0][7]) + ", " + \
                       str(couple_min[0][8]) + ", " + str(couple_min[0][9]) + ")"
    pn_b = couple_min[0][7]
    pb_b = couple_min[0][8]
    gamma_b = couple_min[0][9]

    triplet_string_c = "(" + str(couple_min[1][7]) + ", " + \
                       str(couple_min[1][8]) + ", " + str(couple_min[1][9]) + ")"
    pn_c = couple_min[1][7]
    pb_c = couple_min[1][8]
    gamma_c = couple_min[1][9]

    # Intervalle
    pn_tgt = calcul_barycentre(pn_b, pn_c, dist_b_h, dist_b_c)
    pb_tgt = calcul_barycentre(pb_b, pb_c, dist_b_h, dist_b_c)
    gamma_tgt = calcul_barycentre(gamma_b, gamma_c, dist_b_h, dist_b_c)

    triplet_string_tgt = "(" + str(pn_tgt) + ", " + \
                         str(pb_tgt) + ", " + str(gamma_tgt) + ")"

    fichier_reponses.write(tab_fichiers_traites[i] + " -> " + triplet_string_tgt +
                           " -> [" + triplet_string_b + ", " + triplet_string_c + "]\n")

fichier_reponses.close()
print("Recherche par interpolation (2*3) terminée, résultats écrits dans le fichier 'reponses6.txt'.")

conn.close()

###########################
# Récupération de donéees #
###########################
"""
# Ecriture des données pour l'histogramme et les statistiques.
fichier_donnees = open("donnees.csv", "w")
# On ouvre le fichier excel
xlsx_file = Path('datas/Triplets.xlsx')
wb_obj = openpyxl.load_workbook(xlsx_file)
sheet = wb_obj.active

# On récupère le triplet expert
for row in sheet.iter_rows(min_row=4, max_row=33):
    if row[0].value == id_fascicule:
        pn_expert = row[2].value
        pb_expert = row[3].value
        gamma_expert = row[4].value

# Ensuite, on écrit les données dans un fichier csv pour pouvoir en faire un histogramme
texte = " PN_Original PN_Outil PB_Original PB_Outil G_Original G_Outil\n"
for fichier in stockage_triplets:
    tab_triplet = stockage_triplets[fichier].replace(
        "(", "").replace(")", "").split(",")
    point_noir = int(tab_triplet[0])
    point_blanc = int(tab_triplet[1])
    gamma = float(tab_triplet[2])

    # Normalisations choisies arbitrairement, peuvent être changée.
    # On normalise le triplet solution.
    pn_normalise = point_noir / 255
    pb_normalise = point_blanc / 255
    gamma_normalise = gamma / 2
    # On normalise le triplet expert.
    pn_original_normalise = pn_expert / 255
    pb_original_normalise = pb_expert / 255
    gamma_original_normalise = gamma_expert / 2

    texte += fichier.replace(id_fascicule, "").replace(".png", "") + " " + \
        str(pn_original_normalise).replace(".", ",") + " " + str(pn_normalise).replace(".", ",") + " " + str(
        pb_original_normalise).replace(".", ",") + " " + str(pb_normalise).replace(".", ",") + " " + str(
        gamma_original_normalise).replace(".", ",") + " " + str(gamma_normalise).replace(".", ",") + "\n"

fichier_donnees.write(texte)

print("Données nécessaires à l'histogrammes écrites dans le fichier 'donnees.csv'.")

#####################
# Calcul des scores #
#####################

print("On passe au calcul des scores des résultats des trois versions !")

fichier_scores = open("scores.csv", "w")

# On commence par le calcul sur le triplet original
# On normalise le triplet expert.
pn_original_normalise = pn_expert / 255
pb_original_normalise = pb_expert / 255
gamma_original_normalise = gamma_expert / 2
# On calcule le total
tot_original = (pn_original_normalise +
                pb_original_normalise + gamma_original_normalise) / 3

texte = ";score_v1;score_v2;score_v3;=MOYENNE(B:B);=MEDIANE(B:B);=MOYENNE(C:C);=MEDIANE(C:C);=MOYENNE(D:D);=MEDIANE(" \
        "D:D)\n "
for fichier in stockage_triplets:
    # On passe au calcul sur la v1
    # On cherche les données
    tab_triplet = stockage_triplets[fichier].replace(
        "(", "").replace(")", "").split(",")
    point_noir = int(tab_triplet[0])
    point_blanc = int(tab_triplet[1])
    gamma = float(tab_triplet[2])
    # On normalise le triplet solution.
    pn_normalise = point_noir / 255
    pb_normalise = point_blanc / 255
    gamma_normalise = gamma / 2
    # On calcule le score
    tot_v1 = (pn_normalise + pb_normalise + gamma_normalise) / 3
    score_v1 = abs(tot_v1 - tot_original)

    # On passe au calcul sur la v2
    # On cherche les données
    tab_triplet = stockage_triplets_v2[fichier].replace(
        "(", "").replace(")", "").split(",")
    point_noir = int(tab_triplet[0])
    point_blanc = int(tab_triplet[1])
    gamma = float(tab_triplet[2])
    # On normalise le triplet solution.
    pn_normalise = point_noir / 255
    pb_normalise = point_blanc / 255
    gamma_normalise = gamma / 2
    # On calcule le score
    tot_v2 = (pn_normalise + pb_normalise + gamma_normalise) / 3
    score_v2 = abs(tot_v2 - tot_original)

    # On passe au calcul sur la v3
    # On cherche les données
    tab_triplet = stockage_triplets_v3[fichier].replace(
        "(", "").replace(")", "").split(",")
    point_noir = int(tab_triplet[0])
    point_blanc = int(tab_triplet[1])
    gamma = float(tab_triplet[2])
    # On normalise le triplet solution.
    pn_normalise = point_noir / 255
    pb_normalise = point_blanc / 255
    gamma_normalise = gamma / 2
    # On calcule le score
    tot_v3 = (pn_normalise + pb_normalise + gamma_normalise) / 3
    score_v3 = abs(tot_v3 - tot_original)

    # On écrit dans le fichier les résultats
    texte += fichier.replace(id_fascicule, "").replace(".png", "") + ";" + str(score_v1).replace(".", ",") + ";" + str(
        score_v2).replace(".", ",") + ";" + str(score_v3).replace(".", ",") + "\n"

fichier_scores.write(texte)

print("Fin de l'écriture des scores dans le fichier 'scores.csv'")
"""
