import os

import numpy as np
import cv2
import time

baseDeCas = ["barb_0001-4133_1919_num_5_1_T1_0032_0000",
             "barb_0001-4133_1920_num_6_1_T1_0051_0000",
             "barb_0001-4133_1929_num_15_1_T1_0046_0000",
             "barb_0001-4133_1939_num_25_1_T1_0123_0000",
             "barb_0001-4133_1941_num_27_1_T1_0032_0000",
             "barb_0001-4133_1963_num_49_1_T1_0020_0000",
             "barb_0001-4141_1907_num_9_1_T1_0010_0000",
             "barb_0001-4141_1909_num_11_1_T1_0011_0000",
             "barb_0001-4141_1910_num_12_1_T1_0034_0000",
             "barb_0001-4141_1919_num_5_1_T1_0002_0000",
             "rnord_0035-2624_1925_num_11_43_T1_0171_0000",
             "rnord_0035-2624_1927_num_13_51_T1_0206_0000",
             "rnord_0035-2624_1928_num_14_53_T1_0059_0000",
             "rnord_0035-2624_1933_num_19_75_T1_0211_0000",
             "rnord_0035-2624_1934_num_20_78_T1_0156_0000",
             "rnord_0035-2624_1934_num_20_80_T1_0342_0000",
             "rnord_0035-2624_1952_num_34_133_T1_0005_0000",
             "rnord_0035-2624_1960_num_42_167_T1_0007_0000",
             "rnord_0035-2624_1964_num_46_181_T1_0131_0000",
             "rnord_0035-2624_1964_num_46_181_T1_0131_0000",
             "rnord_0035-2624_1967_num_49_192_T1_0005_0000",
             "rnord_0035-2624_1970_num_52_204_T1_0007_0000",
             "rnord_0035-2624_1976_num_58_228_T1_0042_0000",
             "rnord_0035-2624_1976_num_58_230_T1_0373_0000",
             "rnord_0035-2624_1979_num_61_241_T1_0315_0000",
             "rnord_0035-2624_1979_num_61_242_T1_0541_0000",
             "rnord_0035-2624_1989_num_71_282_T1_0615_0000",
             "rnord_0035-2624_1991_num_73_290_T1_0241_0000",
             "rnord_0035-2624_1994_num_76_306_T1_0467_0000",
             "binet_0750-7496_1900_num_1_1_T1_0006_0000",
             "binet_0750-750X_1918_num_18_120_T1_0078_0000",
             "asgn_0767-7367_1980_num_100_1_T1_0006_0000",
             "asgn_0767-7367_1980_num_100_2_T1_0062_0000",
             "asgn_0767-7367_1980_num_100_3_T1_0113_0000",
             "asgn_0767-7367_1980_num_100_4_T1_0161_0000",
             "asgn_0767-7367_1981_num_101_1_T1_0006_0000",
             "asgn_0767-7367_1981_num_101_2_T1_0052_0000",
             "lesb_0754-944X_1988_num_65_1_T1_0011_0000",
             "femou_0180-4162_1978_num_6_1_T1_0019_0000",
             "nbeur_0000-0007_1996_num_0_1_T1_0004_0000"]


def calculer_difference(fichier1, fichier2, fichier_sortie):
    # Charger les deux images
    image1 = cv2.imread(fichier1)
    image2 = cv2.imread(fichier2)

    # Calculer la différence de chaque pixel entre les deux images
    diff = cv2.absdiff(image1, image2)

    # Calculer les statistiques de la différence
    mean_diff = np.mean(diff)
    std_dev_diff = np.std(diff)
    min_diff = np.min(diff)
    max_diff = np.max(diff)

    # Écrire les statistiques de la différence dans le fichier de sortie
    with open(fichier_sortie, 'a') as f:
        f.write(str(fichier2) + ', ' + str(mean_diff) + ', ' + str(std_dev_diff) + ', ' + str(min_diff) + ', ' +
                str(max_diff) + '\n')


debut = time.time()

if os.path.exists("../datas/BasesDeCas/TestsAutomatiques/Approximation1x1/resultats.csv"):
    os.remove("../datas/BasesDeCas/TestsAutomatiques/Approximation1x1/resultats.csv")
    open("../datas/BasesDeCas/TestsAutomatiques/Approximation1x1/resultats.csv", 'w').close()
if os.path.exists("../datas/BasesDeCas/TestsAutomatiques/Approximation2x3/resultats.csv"):
    os.remove("../datas/BasesDeCas/TestsAutomatiques/Approximation2x3/resultats.csv")
    open("../datas/BasesDeCas/TestsAutomatiques/Approximation2x3/resultats.csv", 'w').close()
if os.path.exists("../datas/BasesDeCas/TestsAutomatiques/Extrapolation1x1/resultats.csv"):
    os.remove("../datas/BasesDeCas/TestsAutomatiques/Extrapolation1x1/resultats.csv")
    open("../datas/BasesDeCas/TestsAutomatiques/Extrapolation1x1/resultats.csv", 'w').close()
if os.path.exists("../datas/BasesDeCas/TestsAutomatiques/Extrapolation2x3/resultats.csv"):
    os.remove("../datas/BasesDeCas/TestsAutomatiques/Extrapolation2x3/resultats.csv")
    open("../datas/BasesDeCas/TestsAutomatiques/Extrapolation2x3/resultats.csv", 'w').close()
if os.path.exists("../datas/BasesDeCas/TestsAutomatiques/Interpolation1x1/resultats.csv"):
    os.remove("../datas/BasesDeCas/TestsAutomatiques/Interpolation1x1/resultats.csv")
    open("../datas/BasesDeCas/TestsAutomatiques/Interpolation1x1/resultats.csv", 'w').close()

# On évalue les images avec le moteur d'approximation 1x1
for i in range(0, len(baseDeCas)):
    calculer_difference("../datas/BasesDeCas/TestsAutomatiques/Expert/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Approximation1x1/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Approximation1x1/resultats.csv")

# On évalue les images avec le moteur d'approximation 2x3
for i in range(0, len(baseDeCas)):
    calculer_difference("../datas/BasesDeCas/TestsAutomatiques/Expert/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Approximation2x3/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Approximation2x3/resultats.csv")

# On évalue les images avec le moteur d'extrapolation 1x1
for i in range(0, len(baseDeCas)):
    calculer_difference("../datas/BasesDeCas/TestsAutomatiques/Expert/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Extrapolation1x1/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Extrapolation1x1/resultats.csv")

# On évalue les images avec le moteur d'extrapolation 2x3
for i in range(0, len(baseDeCas)):
    calculer_difference("../datas/BasesDeCas/TestsAutomatiques/Expert/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Extrapolation2x3/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Extrapolation2x3/resultats.csv")

# On évalue les images avec le moteur d'interpolation 1x1
for i in range(0, len(baseDeCas)):
    calculer_difference("../datas/BasesDeCas/TestsAutomatiques/Expert/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Interpolation1x1/" + baseDeCas[i] + ".png",
                        "../datas/BasesDeCas/TestsAutomatiques/Interpolation1x1/resultats.csv")

fin = time.time()
temps_execution = fin - debut
print("Temps d'exécution : ", temps_execution, " secondes")
