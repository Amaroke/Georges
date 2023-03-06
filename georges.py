import os
from statistics import mean
from PIL import Image
from PIL import ImageStat
import zipfile
import xml.etree.ElementTree as ET
import openpyxl
from pathlib import Path
import mysql.connector
import sys
import configparser


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
    rectangle_hg = (mot[0], mot[1], mot[0] - largeur_mot / 3, mot[1] - hauteur_mot / 2)
    rectangle_hm = (mot[0] - largeur_mot / 3, mot[1], mot[0] - (largeur_mot / 3) * 2, mot[1] - hauteur_mot / 2)
    rectangle_hd = (mot[0] - (largeur_mot / 3) * 2, mot[1], mot[2], mot[1] - hauteur_mot / 2)
    rectangle_bg = (mot[0], mot[1] - hauteur_mot / 2, mot[0] - largeur_mot / 3, mot[3])
    rectangle_bm = (mot[0] - largeur_mot / 3, mot[1] - hauteur_mot / 2, mot[0] - (largeur_mot / 3) * 2, mot[3])
    rectangle_bd = (mot[0] - (largeur_mot / 3) * 2, mot[1] - hauteur_mot / 2, mot[2], mot[3])

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
def calcul_somme_diff_matrice(m1, m2):
    return abs(m1[0] - m2[0]) + abs(m1[1] - m2[1]) + abs(m1[2] - m2[2]) + abs(m1[3] - m2[3]) + abs(m1[4] - m2[4]) + abs(
        m1[5] - m2[5])


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


# Initialisation des variables constantes utilisée dans tout le fichier
id_fascicule = input("Donnez moi l'id du fascicule à analyser : ")
mot_choisi = "de"  # Peut être remplacé par un input mais il faut modifier la bdd (stocker les valeurs correspondant
# à cet input)

chemin = os.path.join(os.getcwd(), "datas", "Fascicules", id_fascicule, "Pages_volume", "GreyScale")
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
        chemin_ocr = os.path.join(chemin_archive, filename.replace(".png", " - ocr.zip"))
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
                                                   calcul_moyenne_image(mat[2]), calcul_moyenne_image(mat[3]),
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
                tab_moyennes_matrice.append(score_global_matrice(tab_score_mots_matrice))
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
requete = """(select P.page_id, niveau_gris, point_noir, point_blanc, gamma from page as P, triplet as T where 
P.page_id = T.page_id AND niveau_gris >= %s and P.page_id != %s order by niveau_gris asc limit 1) union (select 
P.page_id, niveau_gris, point_noir, point_blanc, gamma from page as P, triplet as T where P.page_id = T.page_id AND 
niveau_gris < %s and P.page_id != %s order by niveau_gris desc limit 1) order by abs(niveau_gris - %s) limit 1 """
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
    cursor.execute(requete, (tab_moyennes[i], id_fascicule, tab_moyennes[i], id_fascicule, tab_moyennes[i]))
    row = cursor.fetchone()
    triplet_string = "(" + str(row[2]) + ", " + str(row[3]) + ", " + str(row[4]) + ")"
    fichier_reponses.write(tab_fichiers_traites[i] + " -> " + triplet_string + "\n")
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

requete = """select P.page_id, point_noir, point_blanc, gamma, haut_gauche, haut_milieu, haut_droite, bas_gauche, 
bas_milieu, bas_droite, fascicule_id from page as P, matrice as M, triplet as T where P.page_id = T.page_id AND 
P.page_id = M.page_id """

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
    rows = cursor.fetchmany(1000)  # On en récupère 1000 par 1000 pour ne pas surcharger la mémoire.
    if not rows:
        est_termine = True
    else:
        for row in rows:
            if not (row[10] == id_fascicule):  # On exclue le fascicule cible.
                for i in range(len(tab_fichiers_traites)):
                    temp = calcul_somme_diff_matrice(tab_moyennes_matrice[i], (
                        float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9])))
                    if temp < matrice_calcul[i]:  # Si la matrcie est plus proche que celles précédentes, on la stocke.
                        matrice_calcul[i] = temp
                        matrice_proche[i] = row[0]
                        matrice_triplet[i] = "(" + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ")"

stockage_triplets_v2 = dict()
# On écrit les réponses dans le second fichier réponses.
for i in range(len(tab_fichiers_traites)):
    fichier_reponses_2.write(tab_fichiers_traites[i] + " -> " + matrice_triplet[i] + "\n")
    stockage_triplets_v2[tab_fichiers_traites[i]] = matrice_triplet[i]

fichier_reponses_2.close()
print("Recherche par matrice 2*3 terminée, résultats écrits dans le fichier 'reponses2.txt'.")

########################
# Méthode par analogie #
########################

# ANA
# On passe à la méthode par matrice
fichier_reponses_3 = open("reponses3.txt", "w")

# On prépare les requêtes qui récupèrent les données de la BDD
requete = """(select * from analogie where difference_niveau_gris >= %s and page1 != %s order by 
difference_niveau_gris asc limit 1) union (select * from analogie where difference_niveau_gris < %s and page1 != %s 
order by difference_niveau_gris desc limit 1) order by abs(difference_niveau_gris - %s) limit 1 """
# On se replace au début de la BDD.
cursor = setup_curseur(conn)

stockage_triplets_v3 = dict()
# On récupère les fichiers les plus proches calculés à la v2 (à recalculer si on fait pas la v2)
for i in range(len(tab_fichiers_traites)):
    diff_NG = tab_moyennes[i] - float(stockage_reponse_score[tab_fichiers_traites[i]][0])
    cursor.execute(requete, (diff_NG, tab_fichiers_traites[i], diff_NG, tab_fichiers_traites[i], diff_NG))
    row = cursor.fetchone()
    triplet = stockage_reponse_score[tab_fichiers_traites[i]][1].replace("(", "").replace(")", "").replace(" ",
                                                                                                           "").split(
        ",")
    pn_analogie = int(triplet[0]) + int(row[4])
    pb_analogie = int(triplet[1]) + int(row[5])
    g_analogie = float(triplet[2]) + float(row[6])
    fichier_reponses_3.write(tab_fichiers_traites[i] + " : (" + str(pn_analogie) + ", " + str(pb_analogie) + ", " + str(
        g_analogie) + ") depuis " + str(triplet) + " avec changement de : " + str(
        int(row[4]) + int(row[5]) + float(row[6])) + "\n")
    stockage_triplets_v3[tab_fichiers_traites[i]] = "(" + str(pn_analogie) + ", " + str(pb_analogie) + ", " + str(
        g_analogie) + ")"
fichier_reponses_3.close()

conn.close()

print("Recherche par analogie terminée, résultats écrits dans le fichier 'reponses3.txt'.")

###########################
# Récupération de donéees #
###########################

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
    tab_triplet = stockage_triplets[fichier].replace("(", "").replace(")", "").split(",")
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
tot_original = (pn_original_normalise + pb_original_normalise + gamma_original_normalise) / 3

texte = ";score_v1;score_v2;score_v3;=MOYENNE(B:B);=MEDIANE(B:B);=MOYENNE(C:C);=MEDIANE(C:C);=MOYENNE(D:D);=MEDIANE(" \
        "D:D)\n "
for fichier in stockage_triplets:
    # On passe au calcul sur la v1
    # On cherche les données
    tab_triplet = stockage_triplets[fichier].replace("(", "").replace(")", "").split(",")
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
    tab_triplet = stockage_triplets_v2[fichier].replace("(", "").replace(")", "").split(",")
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
    tab_triplet = stockage_triplets_v3[fichier].replace("(", "").replace(")", "").split(",")
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
