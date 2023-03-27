import cv2
import xml.etree.ElementTree as ET
import os

# Charger l'image et le fichier xml
image = cv2.imread("rnord_0035-2624_1994_num_76_306_T1_0472_0000.png")
fichier_xml = ET.parse("rnord_0035-2624_1994_num_76_306_T1_0472_0000.xml")
xml = fichier_xml.getroot()

# Obtenir les dimensions de l'image
hauteur, largeur, _ = image.shape

# Créer un dossier pour stocker les png de "de"
if not os.path.exists('de_png'):
    os.makedirs('de_png')

# Initialiser le compteur de "de"
cpt = 1

# Parcourir tous les mots du fichier xml
for mot in xml.iter('word'):
    # Vérifier si le mot est "de"
    if mot.attrib.get("searchWord") == 'de':
        # Gérer le décalage de l'algorithme
        decalage_gauche = int(mot.attrib.get("width")) // 3
        decalage_haut = int(mot.attrib.get("height")) // 3

        # Récupéré la position du "de"
        x1 = int(mot.attrib.get("left")) - decalage_gauche
        y1 = int(mot.attrib.get("top")) - decalage_haut
        x2 = int(mot.attrib.get("right"))
        y2 = int(mot.attrib.get("bottom"))

        # Créer un nouveau fichier png pour le "de"
        image_de = image[y1:y2, x1:x2]
        cv2.imwrite("de_png/de_" + str(cpt) + ".png", image_de)
        cpt += 1

        # Dessiner un rectangle autour du mot
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Enregistrer l'image modifiée
cv2.imwrite("resultat.png", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
