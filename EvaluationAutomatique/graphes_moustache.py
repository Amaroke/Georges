import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generer_graphe_moustahce(fichier):
    # Charger les données en utilisant pandas
    df = pd.read_csv(fichier + ".txt", header=None, names=['nom', 'moyenne', 'ecarttype', 'min', 'max'])

    # Calculer les statistiques nécessaires
    mediane = np.median(df['moyenne'])
    q1 = np.percentile(df['moyenne'], 25)
    q3 = np.percentile(df['moyenne'], 75)
    min_value = np.min(df['min'])
    max_value = np.max(df['max'])

    # Créer un graphique en boîte à moustaches
    fig, ax = plt.subplots()
    ax.boxplot(df['moyenne'], vert=False, widths=0.5, boxprops=dict(color='green'),
               medianprops=dict(color='red', linewidth=2), whiskerprops=dict(color='blue', linewidth=1.5),
               capprops=dict(color='blue'))
    ax.set_title('Boîte à moustaches des moyennes')
    ax.set_xlabel('Moyenne')
    ax.axvline(x=mediane, color='red', linestyle='-', label='Médiane')
    ax.axvline(x=q1, color='blue', linestyle='--', label='25e percentile')
    ax.axvline(x=q3, color='blue', linestyle='--', label='75e percentile')
    ax.axvline(x=min_value, color='purple', linestyle='-.', label='Minimum')
    ax.axvline(x=max_value, color='purple', linestyle='-.', label='Maximum')
    ax.legend()
    ax.set_yticklabels([])

    plt.savefig(fichier + "_moustache.png")


generer_graphe_moustahce("../datas/BasesDeCas/TestsAutomatiques/Approximation1x1/resultats")
generer_graphe_moustahce("../datas/BasesDeCas/TestsAutomatiques/Approximation2x3/resultats")
generer_graphe_moustahce("../datas/BasesDeCas/TestsAutomatiques/Extrapolation1x1/resultats")
generer_graphe_moustahce("../datas/BasesDeCas/TestsAutomatiques/Extrapolation2x3/resultats")
generer_graphe_moustahce("../datas/BasesDeCas/TestsAutomatiques/Interpolation1x1/resultats")
