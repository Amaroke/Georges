import csv
import statistics

# Définir une liste vide pour stocker les données de chaque méthode
approximation1x1_data = []
approximation2x3_data = []
extrapolation1x1_data = []
extrapolation2x3_data = []
interpolation1x1_data = []
interpolation2x3_data = []
persee_data = []

# Ouvrir le fichier CSV et lire les données ligne par ligne
with open('astier.csv') as csvfile:
    reader = csv.reader(csvfile)
    # Ignorer la première ligne si elle contient des en-têtes
    next(reader, None)
    for row in reader:
        row = [elem.strip() for elem in row]
        # Ajouter la valeur à la liste appropriée en fonction de la méthode
        if row[0].split("_")[-1] == 'approximation1x1':
            approximation1x1_data.append(float(row[1]))
        elif row[0].split("_")[-1] == 'approximation2x3':
            approximation2x3_data.append(float(row[1]))
        elif row[0].split("_")[-1] == 'extrapolation1x1':
            extrapolation1x1_data.append(float(row[1]))
        elif row[0].split("_")[-1] == 'extrapolation2x3':
            extrapolation2x3_data.append(float(row[1]))
        elif row[0].split("_")[-1] == 'interpolation1x1':
            interpolation1x1_data.append(float(row[1]))
        elif row[0].split("_")[-1] == 'interpolation2x3':
            interpolation2x3_data.append(float(row[1]))
        elif row[0].split("_")[-1] == 'persee':
            persee_data.append(float(row[1]))

# Liste des données
data = [approximation1x1_data, approximation2x3_data, extrapolation1x1_data,
        extrapolation2x3_data, interpolation1x1_data, interpolation2x3_data,
        persee_data]

# Liste des noms de méthodes
method_names = ['approximation1x1', 'approximation2x3', 'extrapolation1x1',
                'extrapolation2x3', 'interpolation1x1', 'interpolation2x3', 'persee']

# Ouvrir le fichier de sortie en mode écriture
with open('resultats.txt', 'w') as f:
    # Pour chaque méthode, écrire la médiane, l'écart-type, la valeur minimale et maximale dans le fichier
    for i in range(len(data)):
        mediane = statistics.median(data[i])
        ecart_type = statistics.stdev(data[i])
        valeur_min = min(data[i])
        valeur_max = max(data[i])
        f.write(f"Méthode {method_names[i]}:\n")
        f.write(f"Médiane: {mediane:.2f}\n")
        f.write(f"Écart-type: {ecart_type:.2f}\n")
        f.write(f"Valeur minimale: {valeur_min:.2f}\n")
        f.write(f"Valeur maximale: {valeur_max:.2f}\n\n")
