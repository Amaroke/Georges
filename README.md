# NettoyArchiv

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

### Structuration des données à traiter et des fichiers de configuration

Un fichier `config.ini` est nécessaire pour la connexion à la BDD du programme, il faudra donc le créer sous cette forme, à la racine du projet :
```config.ini
[settings]
host : localhost
username : VOTRE USERNAME BDD
password : VOTRE MOT DE PASSE BDD
database : NettoyArchiv
```
Il faut également ajouter à la racine du projet le dossier `datas`, qui contient lui-même les dossiers `Fascicules` et `OCR`, ainsi que `Triplets.xlsx`, la feuille de calcul format excel contenant les Triplets des Fascicules à traiter. <br>
Par la suite il faut simplement mettre les fascicules à traiter ainsi que les OCR respectivement dans leur dossier dédié, `Fascicules` et `OCR`.
