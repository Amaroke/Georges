import os
import cv2
import numpy as np

# Définir la taille des images
taille_souhaitee = (100, 100)

# Initialiser l'image finale
image = np.zeros((taille_souhaitee[1], taille_souhaitee[0]), dtype=np.float32)

cpt = 0

# Parcourir les fichiers PNG de "de"
for filename in os.listdir('de_png'):
    if filename.endswith('.png'):
        # Charger l'image PNG
        image_de = cv2.imread(os.path.join('de_png', filename), cv2.IMREAD_GRAYSCALE)

        # Redimensionner l'image
        image_de = cv2.resize(image_de, taille_souhaitee)

        # Normaliser les valeurs des pixels entre 0 et 1
        image_de = image_de.astype(np.float32) / 255.0

        # Ajouter l'image à l'image finale
        image += image_de

        # Incrémenter le compteur d'images traitées
        cpt += 1

# Diviser l'image finale par le nombre d'images traitées pour obtenir la moyenne
image /= cpt

# Enregistrer l'image finale en PNG
cv2.imwrite('fusion_de.png', (image * 255.0).astype(np.uint8))
