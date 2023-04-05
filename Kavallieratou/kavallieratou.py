import sys

import numpy as np
from matplotlib import pyplot as plt
from skimage import io

# Charger l'image
img = io.imread(sys.argv[1])

# Convertir l'image en niveau de gris
gray = img

# Initialisation des seuils
T_old = 0
T = np.mean(gray)

# On fait 15 itérations
i = 1
while i <= 15:
    T_old = T

    # Calcul de la moyenne des valeurs de pixels de l'image
    avg_pixel_val = np.mean(gray)

    # Soustraction de la moyenne de tous les pixels de l'image
    gray_sub = gray - avg_pixel_val

    # Égalisation de l'histogramme
    gray_eq = np.uint8(255 * (gray_sub - np.min(gray_sub)) / (np.max(gray_sub) - np.min(gray_sub)))

    # Calcul du nouveau seuil T
    T = np.mean(gray_eq)

    # Enregistrement de l'image binaire
    plt.imsave(f'{sys.argv[1]}_iteration{i}.png', gray_eq, cmap='gray')

    i += 1

    # Mise à jour de l'image en niveaux de gris pour la prochaine itération
    gray = gray_eq

# Binarisation de l'image
gray_bin = np.zeros_like(gray)
gray_bin[gray > T] = 1

# Enregistrer l'image finale
plt.imsave(f'{sys.argv[1]}_iteration.png', gray_bin, cmap='gray')
