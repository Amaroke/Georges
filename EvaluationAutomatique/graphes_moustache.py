import matplotlib.pyplot as plt


def afficher_boites_moustaches(data):
    fig, axs = plt.subplots(ncols=5, figsize=(15, 5))
    for i in range(5):
        # On génère le diagramme moustache pour un moteur
        box_data = axs[i].boxplot(data[i])
        # On mets les noms
        q1 = box_data["whiskers"][0].get_ydata()[1]
        q2 = box_data["medians"][0].get_ydata()[0]
        q3 = box_data["whiskers"][1].get_ydata()[1]

        axs[i].annotate("Médiane".format(q2), xy=(0.5, q2),
                        xytext=(38, -5), textcoords="offset points", color="b",
                        ha="center", va="bottom")

        axs[i].annotate("Q1".format(q1), xy=(0.5, q1),
                        xytext=(50, -5), textcoords="offset points", color="b",
                        ha="center", va="bottom")

        axs[i].annotate("Q3".format(q3), xy=(0.5, q3),
                        xytext=(50, 5), textcoords="offset points", color="b",
                        ha="center", va="top")

        title = csv_files[i].split("/")[-2]  # Extraire le nom du dossier parent du fichier CSV pour le titre
        axs[i].set_title(title)
        axs[i].set_xticks([])
        axs[i].invert_yaxis()  # On inverse l'axe y
        axs[i].set_ylim(20, 0)  # On limite entre 0 et 20%
        # Normaliser les données entre 0 et 100%
        data[i] = [x / 255 * 100 for x in data[i]]

        # Définir les étiquettes d'axe personnalisées en pourcentage
        axs[i].set_yticklabels(['{:.0f}%'.format(x) for x in axs[i].get_yticks()])

    fig.suptitle("Moyenne des différences au nettoyage de l'expert", fontsize=16)
    plt.show()


csv_files = ["../datas/BasesDeCas/TestsAutomatiques/Approximation1x1/resultats.csv",
             "../datas/BasesDeCas/TestsAutomatiques/Approximation2x3/resultats.csv",
             "../datas/BasesDeCas/TestsAutomatiques/Extrapolation1x1/resultats.csv",
             "../datas/BasesDeCas/TestsAutomatiques/Extrapolation2x3/resultats.csv",
             "../datas/BasesDeCas/TestsAutomatiques/Interpolation1x1/resultats.csv"]

data = [[] for _ in range(len(csv_files))]  # Créer une liste vide pour chaque fichier CSV

# Lire les données de chaque fichier CSV et les stocker dans les listes correspondantes
for i, file in enumerate(csv_files):
    with open(file, "r") as f:
        for line in f:
            split = line.split(",")
            data[i].append(float(split[2]))

afficher_boites_moustaches(data)
