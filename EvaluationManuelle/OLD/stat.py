import csv
import matplotlib.pyplot as plt


def histogramme_manu(nom_csv):
    data = {"approximation1x1": [0, 0, 0, 0, 0], "approximation2x3": [0, 0, 0, 0, 0],
            "extrapolation1x1": [0, 0, 0, 0, 0], "extrapolation2x3": [0, 0, 0, 0, 0],
            "interpolation1x1": [0, 0, 0, 0, 0]}

    with open(nom_csv + ".csv", newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            row = [elem.strip() for elem in row]
            print(row)
            if row[1] == '1':
                data[row[0].split("_")[-1]][0] += 1
            if row[1] == '2':
                data[row[0].split("_")[-1]][1] += 1
            if row[1] == '3':
                data[row[0].split("_")[-1]][2] += 1
            if row[1] == '4':
                data[row[0].split("_")[-1]][3] += 1
            if row[2] == "Meilleure":
                data[row[0].split("_")[-1]][4] += 1

    bar_width = 0.15
    index = [0, 1, 2, 3, 4]
    opacity = 0.8

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    plt.figure(figsize=(10, 6))

    for i, motor in enumerate(data.keys()):
        plt.bar([x + (i * bar_width) for x in index], data[motor], bar_width,
                alpha=opacity, color=colors[i], label=motor)
        for j, val in enumerate(data[motor]):
            plt.text(j + (i * bar_width) - 0.03, val + 0.2, str(val))

    plt.xlabel('Note')
    plt.ylabel('Nombre de tests')
    plt.title('Histogramme des notes par moteur')
    plt.xticks([x + bar_width * 2 for x in index], ('1', '2', '3', '4', 'Meilleure'))
    plt.legend()

    plt.savefig(nom_csv + '.png')


# Génération des différents histogrammes sur les évaluations manuelles.
histogramme_manu("eric_test")
histogramme_manu("loris_test")
histogramme_manu("ludivine_nicolas_eric_majorite_test")
histogramme_manu("ludivine_test")
histogramme_manu("nicolas_test")
histogramme_manu("sarah_test")
