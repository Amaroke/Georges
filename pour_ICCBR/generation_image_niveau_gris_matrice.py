import os
import cv2
import numpy as np

# Créer un dossier pour stocker les png
if not os.path.exists('de_images_matrices'):
    os.makedirs('de_images_matrices')

# Parcourir les fichiers PNG de "de"
for i, fichier in enumerate(os.listdir('de_png')):
    if fichier.endswith('.png'):
        # Charger l'image PNG
        image_de = cv2.imread(os.path.join('de_png', fichier), cv2.IMREAD_GRAYSCALE)

        # Découper l'image en une matrice 2x3
        h, w = image_de.shape
        sub_h, sub_w = h // 2, w // 3
        sub_images = []
        for y in range(2):
            for x in range(3):
                sub_img = image_de[y * sub_h:(y + 1) * sub_h, x * sub_w:(x + 1) * sub_w]
                sub_images.append(sub_img)

        # Calculer le niveau de gris moyen de chaque portion de la matrice
        moyenne_niveau_gris = [np.mean(sub_img) for sub_img in sub_images]

        # Créer des images de 200*200 pixels avec la couleur du niveau de gris moyen de chaque portion
        images = [np.zeros((200, 200), dtype=np.uint8) for _ in range(6)]
        for image, niveau_gris in zip(images, moyenne_niveau_gris):
            image[:, :] = niveau_gris

        # Assembler les images en une image 2x3
        image_matrice = np.concatenate([np.concatenate(images[:3], axis=1), np.concatenate(images[3:], axis=1)], axis=0)

        # Enregistrer l'image en PNG
        cv2.imwrite(os.path.join('de_images_matrices', f"{i + 1}.png"), image_matrice)
