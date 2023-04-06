import os
import shutil
from PIL import Image
import numpy as np
from skimage import exposure
from matplotlib import pyplot as plt


def effectuer_traitement(nom_image, chemin):
    if os.path.exists(nom_image):
        shutil.rmtree(nom_image)
    os.makedirs(nom_image)

    # Chargement de l'image
    img = Image.open(chemin)

    # Conversion de l'image en tableau NumPy
    img_array = np.array(img)

    i = 1
    while i <= 10:
        # Soustraction de la moyenne à tous les pixels de l'image
        img_array = img_array - np.mean(img_array)

        # Normalisation de l'image sur 0 255
        img_array = (img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array)) * 255

        # Égalisation de l'histogramme avec un mask autour de la valeur moyenne
        img_array = exposure.equalize_hist(img_array, mask=img_array < np.mean(img_array))

        # Enregistrement de l'image itérée
        plt.imsave(f'{nom_image}/iteration{i}.png', img_array, cmap='gray')

        i += 1


effectuer_traitement("rnord_0035-2624_1989_num_71_282_T1_0687_0000",
                     "../datas/Fascicules/rnord_0035-2624_1989_num_71_282/Pages_volume/GreyScale/rnord_0035"
                     "-2624_1989_num_71_282_T1_0687_0000.png")
effectuer_traitement("barb_0001-4133_1920_num_6_1_T1_0035_0000",
                     "../datas/Fascicules/barb_0001-4133_1920_num_6_1/Pages_volume/GreyScale/barb_0001"
                     "-4133_1920_num_6_1_T1_0035_0000.png")
effectuer_traitement("barb_0001-4133_1920_num_6_1_T1_0417_0000",
                     "../datas/Fascicules/barb_0001-4133_1920_num_6_1/Pages_volume/GreyScale/barb_0001"
                     "-4133_1920_num_6_1_T1_0417_0000.png")
effectuer_traitement("barb_0001-4141_1910_num_12_1_F_0002_0000",
                     "../datas/BasesDeCas/TestsManuels/Sale/Origine/barb_0001-4141_1910_num_12_1_F_0002_0000.png")
effectuer_traitement("rnord_0035-2624_1994_num_76_306_T1_0471_0000",
                     "../datas/Fascicules/rnord_0035-2624_1994_num_76_306/Pages_volume/GreyScale/rnord_0035"
                     "-2624_1994_num_76_306_T1_0471_0000.png")
effectuer_traitement("rnord_0035-2624_1994_num_76_306_T1_0564_0000",
                     "../datas/Fascicules/rnord_0035-2624_1994_num_76_306/Pages_volume/GreyScale/rnord_0035"
                     "-2624_1994_num_76_306_T1_0564_0000.png")
effectuer_traitement("rnord_0035-2624_1991_num_73_290_T1_0436_0000",
                     "../datas/Fascicules/rnord_0035-2624_1991_num_73_290/Pages_volume/GreyScale/rnord_0035"
                     "-2624_1991_num_73_290_T1_0436_0000.png")
