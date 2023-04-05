import matplotlib.pyplot as plt


def afficher_boites_moustaches(data):
    fig, axs = plt.subplots(ncols=5, figsize=(15, 5))
    for i in range(5):
        axs[i].boxplot(data[i])
    plt.show()


# Les noms des fichiers CSV
csv_files = ["../datas/BasesDeCas/TestsAutomatiques/Approximation1x1/resultats.csv",
             "../datas/BasesDeCas/TestsAutomatiques/Approximation2x3/resultats.csv",
             "../datas/BasesDeCas/TestsAutomatiques/Extrapolation1x1/resultats.csv",
             "../datas/BasesDeCas/TestsAutomatiques/Extrapolation2x3/resultats.csv",
             "../datas/BasesDeCas/TestsAutomatiques/Interpolation1x1/resultats.csv"]

# Les données
data = [[] for _ in range(len(csv_files))]  # Créer une liste vide pour chaque fichier CSV

# Lire les données de chaque fichier CSV et les stocker dans les listes correspondantes
for i, file in enumerate(csv_files):
    with open(file, "r") as f:
        for line in f:
            split = line.split(",")
            data[i].append(float(split[2]))

afficher_boites_moustaches(data)
