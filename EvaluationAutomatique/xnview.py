from PIL import Image
import numpy as np

baseDeCas = [
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000", 55, 236, 0.75],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000", 30, 233, 0.8],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000", 35, 228, 0.8],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000", 30, 235, 0.8],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000", 30, 240, 1],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000", 30, 240, 1],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000", 35, 214, 0.85],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000", 30, 222, 1],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000", 30, 215, 1],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000", 35, 200, 0.7],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000", 10, 230, 1],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000", 15, 220, 1],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000", 25, 200, 1],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000", 1, 200, 0.8],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000", 20, 230, 1],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000", 10, 245, 1],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000", 1, 215, 0.8],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000", 1, 195, 0.85],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000", 1, 210, 0.85],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000", 1, 210, 0.85],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000", 1, 210, 0.9],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000", 1, 210, 0.9],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000", 1, 230, 0.9],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000", 1, 225, 0.8],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000", 1, 215, 1],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000", 1, 215, 0.9],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000", 1, 205, 0.75],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000", 30, 255, 0.75],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000", 30, 255, 0.7],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000", 90, 230, 1],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000", 70, 172, 0.8],
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000", 0, 228, 0.85],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000", 0, 228, 0.85],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000", 30, 220, 0.85],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000", 30, 230, 0.85],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000", 1, 230, 0.85],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000", 1, 225, 0.85],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000", 60, 204, 1],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000", 45, 198, 1],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000", 53, 210, 1]
]


def appliquer_triplets(fichier, noir, blanc, gamma, methode):
    # Ouvrir l'image et la convertir en tableau NumPy
    image = np.array(Image.open("../datas/BasesDeCas/TestsAutomatiques/Origine/" + fichier + ".png"))

    # Appliquer le point noir et le point blanc
    image = np.clip(image, noir, blanc)

    # Normaliser l'image
    image = (image - noir) / (blanc - noir)

    # Appliquer le gamma
    image = image ** (1 / gamma)

    # Dénormaliser l'image
    image = image * (blanc - noir) + noir

    # Arrondir et convertir le tableau NumPy en image PIL
    image = np.round(image).astype(np.uint8)
    image = Image.fromarray(image)

    # Sauvegarder l'image modifiée
    image.save("../datas/BasesDeCas/TestsAutomatiques/" + methode + "/" + fichier + ".png")


# On génère les images en appliquant les triplets experts
for image in baseDeCas:
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets(fichier, noir, blanc, gamma, "Expert")
