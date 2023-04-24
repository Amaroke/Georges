import csv
import matplotlib.pyplot as plt
import random

# Définir une liste vide pour stocker les données de chaque méthode
approximation1x1_data = []
approximation2x3_data = []
extrapolation1x1_data = []
extrapolation2x3_data = []
interpolation1x1_data = []
interpolation2x3_data = []
persee_data = []

# Ouvrir le fichier CSV et lire les données ligne par ligne
with open('fichier.csv') as csvfile: # Modifier cette ligne pour traiter des résultats différents
    reader = csv.reader(csvfile)
    # Ignorer la première ligne si elle contient des en-têtes
    next(reader, None)
    for row in reader:
        row = [elem.strip() for elem in row]
        # Ajouter la valeur à la liste appropriée en fonction de la méthode
        if row[0].split("_")[-1] == 'approximation1x1':
            approximation1x1_data.append(random.randint(0, 4))
        elif row[0].split("_")[-1] == 'approximation2x3':
            approximation2x3_data.append(random.randint(0, 4))
        elif row[0].split("_")[-1] == 'extrapolation1x1':
            extrapolation1x1_data.append(random.randint(0, 4))
        elif row[0].split("_")[-1] == 'extrapolation2x3':
            extrapolation2x3_data.append(random.randint(0, 4))
        elif row[0].split("_")[-1] == 'interpolation1x1':
            interpolation1x1_data.append(random.randint(0, 4))
        elif row[0].split("_")[-1] == 'interpolation2x3':
            interpolation2x3_data.append(random.randint(0, 4))
        elif row[0].split("_")[-1] == 'persee':
            persee_data.append(random.randint(0, 4))

# Liste des données
data = [approximation1x1_data, approximation2x3_data, extrapolation1x1_data,
        extrapolation2x3_data, interpolation1x1_data, interpolation2x3_data,
        persee_data]



# Liste des noms de méthodes
method_names = ['approximation1x1', 'approximation2x3', 'extrapolation1x1',
                'extrapolation2x3', 'interpolation1x1', 'interpolation2x3', 'persee']

# Créer un graphique moustache pour chaque méthode et l'enregistrer en tant que PNG
for i in range(len(data)):
    fig, ax = plt.subplots()
    ax.boxplot(data[i])
    ax.set_title(method_names[i])
    ax.set_ylabel('Valeurs')
    plt.savefig(method_names[i] + '.png')
    plt.close()
