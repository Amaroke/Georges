import os
import shutil

# Définir le dossier racine de la recherche
root_folder = "datas/Fascicules"
root_folder_2 = "datas/FasciculesSupplementaires"

# Page à retirer de la base d'apprentissage
target_files = []

# Définir le dossier de destination pour les fichiers trouvés
dest_folder = "datas/BasesDeCas/TestsAutomatiques/Origine"


def recursive_search(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            # Vérifier si le nom de fichier correspond au motif de nommage
            if filename in target_files:
                # Déplacer le fichier vers le dossier de destination
                src_path = os.path.join(dirpath, filename)
                dest_path = os.path.join(dest_folder, filename)
                shutil.move(src_path, dest_path)
                print(f"Le fichier {filename} a été déplacé vers {dest_folder}.")
        for dirname in dirnames:
            recursive_search(os.path.join(dirpath, dirname))


# Appeler la fonction de recherche récursive
recursive_search(root_folder)
recursive_search(root_folder_2)
