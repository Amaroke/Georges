import os
import cv2
import numpy as np

# Créer un dossier pour stocker les png
if not os.path.exists('de_niveau_gris'):
    os.makedirs('de_niveau_gris')

# Parcourir les fichiers PNG de "de"
for i, fichier in enumerate(os.listdir('de_png')):

    if fichier.endswith('.png'):
        # Charger l'image PNG
        image_de = cv2.imread(os.path.join('de_png', fichier), cv2.IMREAD_GRAYSCALE)

        # Calculer le niveau de gris moyen
        niveau_gris_moyen = np.mean(image_de)

        # Créer une image de 200*200 pixels avec la couleur du niveau de gris moyen
        image = np.zeros((200, 200), dtype=np.uint8)
        image[:, :] = niveau_gris_moyen

        # Enregistrer l'image en PNG
        cv2.imwrite(os.path.join('de_niveau_gris', f"{i + 1}.png"), image)
