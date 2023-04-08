import os
import shutil
from PIL import Image
import numpy as np
from skimage import exposure
from matplotlib import pyplot as plt


def traitement_kavallieratou(nom_image, chemin):
    # Création du dossier de l'image
    if os.path.exists(nom_image):
        shutil.rmtree(nom_image)
    os.makedirs(nom_image)

    # Chargement de l'image
    img = Image.open(chemin)

    # Conversion de l'image en tableau NumPy
    img_array = np.array(img)

    # On fait 15 itérations, on ignore totalement la condition d'arrêt.
    for i in range(1, 15):
        # On soustrait la moyenne de l'image à l'image
        img_array = img_array - np.mean(img_array)

        # On normalise l'image sur 0-255
        img_array = (img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array)) * 255

        # On égalise l'histogramme avec un masque sur les pixels qui sont en dessous de la moyenne,
        # pour éviter d'égaliser les zones les plus claires (et donc le fond de l'image).
        img_array = exposure.equalize_hist(img_array, mask=img_array < np.mean(img_array))

        # Enregistrement de l'image itérée
        plt.imsave(f'{nom_image}/iteration{i}.png', img_array, cmap='gray')


traitement_kavallieratou("rnord_0035-2624_1989_num_71_282_T1_0687_0000",
                         "../datas/Fascicules/rnord_0035-2624_1989_num_71_282/Pages_volume/GreyScale/rnord_0035"
                         "-2624_1989_num_71_282_T1_0687_0000.png")
traitement_kavallieratou("barb_0001-4133_1920_num_6_1_T1_0035_0000",
                         "../datas/Fascicules/barb_0001-4133_1920_num_6_1/Pages_volume/GreyScale/barb_0001"
                         "-4133_1920_num_6_1_T1_0035_0000.png")
traitement_kavallieratou("barb_0001-4133_1920_num_6_1_T1_0417_0000",
                         "../datas/Fascicules/barb_0001-4133_1920_num_6_1/Pages_volume/GreyScale/barb_0001"
                         "-4133_1920_num_6_1_T1_0417_0000.png")
traitement_kavallieratou("barb_0001-4141_1910_num_12_1_F_0002_0000",
                         "../datas/BasesDeCas/TestsManuels/Sale/Origine/barb_0001-4141_1910_num_12_1_F_0002_0000.png")
traitement_kavallieratou("rnord_0035-2624_1994_num_76_306_T1_0471_0000",
                         "../datas/Fascicules/rnord_0035-2624_1994_num_76_306/Pages_volume/GreyScale/rnord_0035"
                         "-2624_1994_num_76_306_T1_0471_0000.png")
traitement_kavallieratou("rnord_0035-2624_1994_num_76_306_T1_0564_0000",
                         "../datas/Fascicules/rnord_0035-2624_1994_num_76_306/Pages_volume/GreyScale/rnord_0035"
                         "-2624_1994_num_76_306_T1_0564_0000.png")
traitement_kavallieratou("rnord_0035-2624_1991_num_73_290_T1_0436_0000",
                         "../datas/Fascicules/rnord_0035-2624_1991_num_73_290/Pages_volume/GreyScale/rnord_0035"
                         "-2624_1991_num_73_290_T1_0436_0000.png")
