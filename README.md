# Georges

## Prérequis & mise en place du programme

Plusieurs prérequis sont nécessaires à l'utilisation de ce programme.

### Python, mySQL

La version 3.11 de Python a été choisi pour ces performances et est nécessaire, vous pouvez l'installer sur n'importe
quelle machine facilement en suivant ce [lien](https://www.python.org/downloads/release/python-3111/).<br>
De même, vous avez besoin d'un serveur de base de données, mySQL définit le choix de notre SGBD pour son côté
open-source et ses performances sur de gros jeu de données, vous pouvez également l'installer facilement en suivant
ce [lien](https://dev.mysql.com/downloads/mysql/).

### Dépendances nécessaires à Python

Pour faciliter l'utilisation de notre programme, nous n'utilisons que des dépendances facilement obtenables à l'aide de
pip, déjà présent dans la version 3.11 de python.<br >
Il faudra donc installer les dépendances suivantes simplement en exécutant ces commandes :

* pip install mysql-connector-python
* pip install configparser
* pip install openpyxl
* pip install Pillow
* pip install matplotlib
* pip install numpy
* pip install tkinter
* pip install opencv-python
* pip install skimage

### Structuration des données à traiter et des fichiers de configuration

Un fichier `config.ini` est nécessaire pour la connexion à la BDD du programme, il faudra donc le créer sous cette
forme, à la racine du projet :

```config.ini
[settings]
host : localhost
username : VOTRE USERNAME BDD
password : VOTRE MOT DE PASSE BDD
database : Georges
```

Il faut également ajouter à la racine du projet le dossier `datas`.
Nous travaillons avec l'architecture suivante pour le dossier `datas`, il est important de respecter cette structure
pour que le programme puisse fonctionner correctement, il faut donc remplis le dossier `Fascicules` avec les fascicules
et le dossier `OCR` avec les fichiers OCR.

```
├───BasesDeCas
│   ├───TestsAutomatiques
│   │   ├───Approximation1x1
│   │   ├───Approximation2x3
│   │   ├───Expert
│   │   ├───Extrapolation1x1
│   │   ├───Extrapolation2x3
│   │   ├───Interpolation1x1
│   │   ├───Interpolation2x3
│   │   └───Origine
│   └───TestsManuels
│       ├───Approximation1x1
│       ├───Approximation2x3
│       ├───Extrapolation1x1
│       ├───Extrapolation2x3
│       ├───Interpolation1x1
│       ├───Interpolation2x3
│       └───Origine
├───Fascicules
│   ├───[...]
└───OCR
    ├───[...]
```

### Utilisation du programme et de ses fonctionnalités

#### Base de données

Le dossier `./DB` contient le script sql `bdd.sql` qui permet de créer la base de données nécessaire au bon
fonctionnement du programme.
Il faut exécuter `db_setup.py` pour créer la base de données et les tables nécessaires au bon fonctionnement du
programme.
Le fichier `deplacer_base_de_cas.py` permet de déplacer les pages qui sont à renseigner dans la variable `target_files`.
Et ainsi de les retirer de la base d'apprentissage.

#### Utilisation de Georges

Pour utiliser Georges, il faut simplement mettre le fascicule que l'on veut nettoyer avec les autres, sans l'ajouter à
la base de données.
Ensuite, il faut exécuter georges.py et suivre les instructions, et donc renseigner le nom du fascicule à traiter.

#### Évaluation automatique

Pour l'évaluation automatique, dans le fichier `./EvaluationAutomatique/evaluation_automatique.py`, il faut modifier la
variable `baseDeCas` avec le nom des pages à évaluer.
On peut ensuite lancer le script `./EvaluationAutomatique/statistiques.py` et le
script `./EvaluationAutomatique/graphes_moustaches.py` qui vont utiliser les résultats
générés.

#### Évaluation manuelle

Pour l'évaluation manuelle, si le besoin est, il faut utiliser le git
suivant : https://github.com/Amaroke/EvaluateurGeorges

Une fois le csv obtenus, il faut le placer dans le dossier `./EvaluationManuelle/`.

Pour modifier le fichier à traiter pour les diagrammes en boite, il faut modifier le nom du fichier utilisé à la ligne
15 du fichier `./EvaluationManuelle/graphes_moustaches.py`

#### Pour Kavallieratou

Il faut simplement utiliser la fonction `traitement_kavallieratou` en mettant comme paramètre le nom de la page à
traiter et le chemin.
Un exemple fictif est présent, il faut le retirer/modifier pour que le script fonctionne.

#### Pour les autres fonctionnalités

Le dossier `./Statistiques_de` servait à la génération des statistiques sur les "de". Il n'est pas utile de le
conserver.
Le fichier `separer_res.py` permet d'extraire les résultats voulus des triplets renvoyés par Georges.
Le fichier `xnview.py` est un script qui permettait de simuler les outils de Persee pour le traitement.
Des données sont présentes dans ces deux derniers fichiers, il faut les retirer/modifier pour que le script fonctionne.
Mais il n'est pas utile de conserver ces fichiers pour le bon fonctionnement de Georges.