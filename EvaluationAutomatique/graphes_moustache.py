import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def generer_diagrammes_moustache(data, csv_files):
    for i in range(len(data)):
        fig, ax = plt.subplots()
        ax.boxplot(data[i])
        ax.set_xticks([])
        ax.invert_yaxis()  # On inverse l'axe y
        ax.set_ylim(20, 0)  # On limite l'axe y entre 0 et 20
        ax.grid(axis='y', linestyle='-', alpha=0.7)
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
        plt.savefig(csv_files[i].replace(".csv", ".png"))
        plt.close(fig)


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

generer_diagrammes_moustache(data, csv_files)

