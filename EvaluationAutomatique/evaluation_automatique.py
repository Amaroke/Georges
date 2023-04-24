import os

import numpy as np
import cv2
import time

baseDeCas = []


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


def evaluer_images(baseDeCas, methode, resultat):
    for i in range(len(baseDeCas)):
        calculer_difference("../datas/BasesDeCas/TestsAutomatiques/Expert/" + baseDeCas[i] + ".png",
                            f"../datas/BasesDeCas/TestsAutomatiques/{methode}/{baseDeCas[i]}.png",
                            f"{resultat}.csv")


debut = time.time()

if os.path.exists("approximation1x1.csv"):
    os.remove("approximation1x1.csv")
    open("approximation1x1.csv", 'w').close()
if os.path.exists("approximation2x3.csv"):
    os.remove("approximation2x3.csv")
    open("approximation2x3.csv", 'w').close()
if os.path.exists("extrapolation1x1.csv"):
    os.remove("extrapolation1x1.csv")
    open("extrapolation1x1.csv", 'w').close()
if os.path.exists("extrapolation2x3.csv"):
    os.remove("extrapolation2x3.csv")
    open("extrapolation2x3.csv", 'w').close()
if os.path.exists("interpolation1x1.csv"):
    os.remove("interpolation1x1.csv")
    open("interpolation1x1.csv", 'w').close()
if os.path.exists("interpolation2x3.csv"):
    os.remove("interpolation2x3.csv")
    open("interpolation2x3.csv", 'w').close()

evaluer_images(baseDeCas, "Approximation1x1", "approximation1x1")
evaluer_images(baseDeCas, "Approximation2x3", "approximation2x3")
evaluer_images(baseDeCas, "Extrapolation1x1", "extrapolation1x1")
evaluer_images(baseDeCas, "Extrapolation2x3", "extrapolation2x3")
evaluer_images(baseDeCas, "Interpolation1x1", "interpolation1x1")
evaluer_images(baseDeCas, "Interpolation2x3", "interpolation2x3")

fin = time.time()
temps_execution = fin - debut
print("Temps d'exécution : ", temps_execution, " secondes")
