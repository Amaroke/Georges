import sys

import numpy as np
from matplotlib import pyplot as plt
from skimage import io

# Charger l'image
image = io.imread(sys.argv[1])

# On fait 15 itérations
i = 1
avg_pixel_val = np.mean(image)
while i <= 15:

    # Calcul de la moyenne des valeurs de pixels de l'image
    avg_pixel_val = np.mean(image)

    # Soustraction de la moyenne de tous les pixels de l'image
    gray_sub = image - avg_pixel_val

    # Égalisation de l'histogramme
    gray_eq = np.uint8(255 * (gray_sub - np.min(gray_sub)) / (np.max(gray_sub) - np.min(gray_sub)))

    # Enregistrement de l'image binaire
    plt.imsave(f'{sys.argv[1]}_iteration{i}.png', gray_eq, cmap='gray')

    i += 1

    # Mise à jour de l'image en niveaux de gris pour la prochaine itération
    image = gray_eq

# Binarisation de l'image
gray_bin = np.zeros_like(image)
gray_bin[image > avg_pixel_val] = 1

# Enregistrer l'image finale
plt.imsave(f'{sys.argv[1]}_iteration.png', gray_bin, cmap='gray')
