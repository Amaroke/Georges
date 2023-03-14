import cv2
import numpy as np
import xml.etree.ElementTree as ET

# Charger l'image et le fichier xml
img = cv2.imread("rnord_0035-2624_1994_num_76_306_T1_0472_0000.png")
tree = ET.parse("rnord_0035-2624_1994_num_76_306_T1_0472_0000.xml")
root = tree.getroot()

# Obtenir les dimensions de l'image
height, width, _ = img.shape

# Parcourir tous les mots du fichier xml
for word in root.iter('word'):
    # Vérifier si le mot est "de"
    if word.attrib.get("searchWord") == 'de':
        # Gérer le décalage de l'algorithme
        decalage_gauche = int(word.attrib.get("width")) // 3
        decalage_haut = int(word.attrib.get("height")) // 3

        # Récupéré la position du "de"
        x1 = int(word.attrib.get("left")) - decalage_gauche
        y1 = int(word.attrib.get("top")) - decalage_haut
        x2 = int(word.attrib.get("right"))
        y2 = int(word.attrib.get("bottom"))

        print(x1, y1, x2, y2)

        # Dessiner un rectangle autour du mot
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Afficher l'image modifiée
cv2.imwrite("resultat.jpg", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
