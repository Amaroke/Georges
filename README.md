# Georges

## Prérequis & mise en place du programme

Plusieurs prérequis sont nécessaires à l'utilisation de ce programme.

### Python, mySQL

La version 3.11 de Python a été choisi pour ces performances et est nécessaire, vous pouvez l'installer sur n'importe quelle machine facilement en suivant ce [lien](https://www.python.org/downloads/release/python-3111/).<br>
De même vous avez besoin d'un serveur de base de données, mySQL définit le choix de notre SGBD pour son côté open-source et ses performances sur de gros jeu de données, vous pouvez également l'installer facilement en suivant ce [lien](https://dev.mysql.com/downloads/mysql/). 

### Dépendances nécessaires à Python

Pour faciliter l'utilisation de notre programme, nous n'utilisons que des dépendances facilement obtenables à l'aide de pip, déjà présent dans la version 3.11 de python.<br >
Il faudra donc installer les dépendances suivantes simplement en exécutant ces commandes :
* pip install mysql-connector-python
* pip install configparser
* pip install openpyxl
* pip install Pillow
* pip install matplotlib
* pip install numpy
* pip install tkinter

### Structuration des données à traiter et des fichiers de configuration

Un fichier `config.ini` est nécessaire pour la connexion à la BDD du programme, il faudra donc le créer sous cette forme, à la racine du projet :
```config.ini
[settings]
host : localhost
username : VOTRE USERNAME BDD
password : VOTRE MOT DE PASSE BDD
database : Georges
```
Il faut également ajouter à la racine du projet le dossier `datas`, qui contient lui-même les dossiers `Fascicules` et `OCR`, ainsi que `Triplets.xlsx`, la feuille de calcul format excel contenant les Triplets des Fascicules à traiter. <br>
Par la suite il faut simplement mettre les fascicules à traiter ainsi que les OCR respectivement dans leur dossier dédié, `Fascicules` et `OCR`.

Nous travaillons avec l'architecture suivante pour le dossier `datas` :
```
├───Fascicules
│   ├───barb_0001-4133_1919_num_5_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───barb_0001-4133_1920_num_6_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───barb_0001-4133_1929_num_15_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───barb_0001-4133_1939_num_25_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───barb_0001-4133_1941_num_27_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   ├───Couleur
│   │   │   └───GreyScale
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───barb_0001-4133_1963_num_49_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───barb_0001-4141_1907_num_9_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───barb_0001-4141_1909_num_11_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───barb_0001-4141_1910_num_12_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───barb_0001-4141_1919_num_5_1
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1925_num_11_43
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1927_num_13_51
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1928_num_14_53
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   ├───Couleur
│   │   │   └───GreyScale
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1933_num_19_75
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1934_num_20_78
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1934_num_20_80
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1952_num_34_133
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1960_num_42_167
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   ├───Couleur
│   │   │   └───GreyScale
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1964_num_46_181
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   ├───Couleur
│   │   │   └───GreyScale
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1967_num_49_192
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1970_num_52_204
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   ├───Couleur
│   │   │   └───GreyScale
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1976_num_58_228
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1976_num_58_230
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1979_num_61_241
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1979_num_61_242
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1989_num_71_282
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   ├───Couleur
│   │   │   └───GreyScale
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   ├───rnord_0035-2624_1991_num_73_290
│   │   ├───Fantomes_Couvertures_Figures
│   │   │   ├───Bitmap
│   │   │   └───Couleur
│   │   ├───Pages_volume
│   │   │   ├───Bitmap
│   │   │   └───GreyScale
│   │   └───Resultat_OCR
│   └───rnord_0035-2624_1994_num_76_306
│       ├───Fantomes_Couvertures_Figures
│       │   ├───Bitmap
│       │   └───Couleur
│       ├───Pages_volume
│       │   ├───Bitmap
│       │   └───GreyScale
│       └───Resultat_OCR
├───janvier2023
│   ├───Images
│   └───OCR
├───mars2023
├───OCR
│   ├───barb_0001-4133_1919_num_5_1
│   ├───barb_0001-4133_1920_num_6_1
│   ├───barb_0001-4133_1929_num_15_1
│   ├───barb_0001-4133_1939_num_25_1
│   ├───barb_0001-4133_1941_num_27_1
│   ├───barb_0001-4133_1963_num_49_1
│   ├───barb_0001-4141_1907_num_9_1
│   ├───barb_0001-4141_1909_num_11_1
│   ├───barb_0001-4141_1910_num_12_1
│   ├───barb_0001-4141_1919_num_5_1
│   ├───rnord_0035-2624_1925_num_11_43
│   ├───rnord_0035-2624_1927_num_13_51
│   ├───rnord_0035-2624_1928_num_14_53
│   ├───rnord_0035-2624_1933_num_19_75
│   ├───rnord_0035-2624_1934_num_20_78
│   ├───rnord_0035-2624_1934_num_20_80
│   ├───rnord_0035-2624_1952_num_34_133
│   ├───rnord_0035-2624_1960_num_42_167
│   ├───rnord_0035-2624_1964_num_46_181
│   ├───rnord_0035-2624_1966_num_48_191
│   ├───rnord_0035-2624_1967_num_49_192
│   ├───rnord_0035-2624_1970_num_52_204
│   ├───rnord_0035-2624_1976_num_58_228
│   ├───rnord_0035-2624_1976_num_58_230
│   ├───rnord_0035-2624_1979_num_61_241
│   ├───rnord_0035-2624_1979_num_61_242
│   ├───rnord_0035-2624_1989_num_71_282
│   ├───rnord_0035-2624_1991_num_73_290
│   └───rnord_0035-2624_1994_num_76_306
└───ressources_evaluateur
```