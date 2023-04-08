import numpy as np

def generer_statistiques(data, csv_files):
    for i in range(len(data)):
        mediane = np.median(data[i])
        ecart_type = np.std(data[i])
        valeur_min = np.min(data[i])
        valeur_max = np.max(data[i])

        with open(csv_files[i].replace(".csv", ".txt"), "w") as f:
            f.write(f"Mediane : {mediane:.2f}\n")
            f.write(f"Ecart type : {ecart_type:.2f}\n")
            f.write(f"Valeur minimale : {valeur_min:.2f}\n")
            f.write(f"Valeur maximale : {valeur_max:.2f}\n")

csv_files = ["approximation1x1.csv",
             "approximation2x3.csv",
             "extrapolation1x1.csv",
             "extrapolation2x3.csv",
             "interpolation1x1.csv",
             "interpolation2x3.csv"]

data = [[] for _ in range(len(csv_files))]  # Créer une liste vide pour chaque fichier CSV

# Lire les données de chaque fichier CSV et les stocker dans les listes correspondantes
for i, file in enumerate(csv_files):
    with open(file, "r") as f:
        for line in f:
            split = line.split(",")
            data[i].append(float(split[2]))

generer_statistiques(data, csv_files)
