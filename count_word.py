import os
import xml.etree.ElementTree
import zipfile

import matplotlib.pyplot as plt
import numpy as np


def count_word_in_OCR(searched_word):
    ocr_directory = os.path.join("datas", "OCR")
    nb_words = [0] * 51
    nb_words_real = [0] * 10000
    total_occurrences = 0
    total_pages = 0
    for dossier in os.listdir(ocr_directory):
        for filename in os.listdir(os.path.join(ocr_directory, dossier)):
            total_pages += 1
            cpt = 0
            if filename.endswith(".zip"):
                archive = zipfile.ZipFile(os.path.join(ocr_directory, dossier, filename), 'r')
                xml_filename = filename.replace(" - ocr.zip", ".xml")
                try:
                    archive.extractall(os.path.join(ocr_directory, dossier))
                    tree = xml.etree.ElementTree.parse(os.path.join(ocr_directory, dossier, xml_filename))
                    root = tree.getroot()
                    for word in root.iter("word"):
                        if word.attrib.get("searchWord") == searched_word:
                            cpt += 1
                            total_occurrences += 1
                except:
                    print("Erreur lors de l'ouverture du fichier", xml_filename)
                os.remove(os.path.join(ocr_directory, dossier, xml_filename))
            nb_words_real[cpt] += 1
            if cpt < 50:
                nb_words[cpt] += 1
            else:
                nb_words[50] += 1

    mean = total_occurrences / total_pages
    return nb_words, mean, nb_words_real


de = count_word_in_OCR("de")
n = len(de[2])
variance = sum(de[2][i] * (i - de[1]) ** 2 for i in range(n)) / sum(de[2])
standard_deviation = np.sqrt(variance)

print("La moyenne de \"de\" par page est", str(de[1]), " et l'écart type est de", str(standard_deviation))
# La moyenne de "de" par page est 16.19943992298941 et l'écart type est de 11.532348134972942

de = de[0]
le = count_word_in_OCR("le")[0]

x = list(range(len(de)))

fig, ax = plt.subplots()

bar_width = 0.35

bar1 = ax.bar(x, de, bar_width)
bar2 = ax.bar([x + bar_width for x in x], le, bar_width)

ax.set_xlabel('Nombre d\'itérations')
ax.set_ylabel('Nombre de pages')
ax.set_title('Histogramme du nombre de pages avec une certaine itération des mots "de" et "le"')
ax.legend((bar1[0], bar2[0]), ('de', 'le'))

plt.show()
