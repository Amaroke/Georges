from tkinter import *
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import os
import random


# Fonction qui retourne une image TK à partir du nom du fichier, d'une largeur et d'une hauteur.
def creer_imageTk(dossier, nom_fichier, largeur, hauteur):
    img = Image.open(os.path.join(dossier, nom_fichier + ".png"))
    img = img.resize((largeur, hauteur - 50), Image.LANCZOS)
    return ImageTk.PhotoImage(img)


# Fonction qui retourne une image TK découpée à partir du nom du fichier, d'une largeur et d'une hauteur et d'une
# boîte de coordonnées (gauche, haut, droite, bas).
def creer_imageTk_decoupee(dossier, nom_fichier, largeur, hauteur, box):
    img = Image.open(os.path.join(dossier, nom_fichier + ".png"))
    box = ((box[0] * img.width) / largeur, (box[1] * img.height) / hauteur, (box[2] * img.width) / largeur,
           (box[3] * img.height) / hauteur)
    img = img.crop(box)
    img = img.resize((largeur, hauteur), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)


# Fonction qui crée, place et retourne un label contenant l'image envoyée en paramètre.
def creer_labelTk(window, gestionnaire_fenetre, img, x, y):
    labelTk = Label(window, image=img, bg="white")
    labelTk.place(x=x, y=y)
    labelTk.bind("<Button-1>", gestionnaire_fenetre.reagir_zoom)
    return labelTk


# Fonction qui crée, place et retourne un curseur pour noter une image.
def creer_curseurTk(window, gest_fenetre, x):
    slider = Scale(window, from_=0, to=5, resolution=0.5, orient=HORIZONTAL)
    slider.place(x=x, y=gest_fenetre.hauteur - 50, width=gest_fenetre.largeur, height=40)
    return slider


# Fonction qui crée, place et retourne une boîte de texte pour commenter la notation de l'image.
def creer_text_box_Tk(window, gest_fenetre, x):
    text = Text(window, state='normal')
    text.place(x=x, y=gest_fenetre.hauteur - 10, width=gest_fenetre.largeur, height=60)
    return text


# Procédure qui crée et place un bouton de confirmation permettant à l'utilisateur de confirmer sa notation et de
# passer à la suite.
def creer_bouton_confirmation(gest_fenetre, id_pages, window):
    bouton = Button(window, text="Confirmer", command=lambda: fin_eval(gest_fenetre, id_pages, window))
    bouton.place(x=gest_fenetre.largeur/4, y=gest_fenetre.hauteur-10)


# # Procédure qui est déclenchée lors de l'appui du bouton de confirmation, confirme la notation, l'enregistre et
# passe à la prochaine page.
def fin_eval(gest_fenetre, id_pages, window):
    gest_fenetre.confirmer()
    # Si on est à la dernière image, on notifie l'utilisateur et le programme s'interrompt.
    if gest_fenetre.num_page_actuelle == len(id_pages) - 1:
        messagebox.showinfo("Fin de l'évaluation",
                            "Vous avez fini d'évaluer les images actuellement stockées !\n Les résultats sont "
                            "enregistrés sous 'Résultats/reponses_eval.csv' !")
        window.destroy()
        exit(0)

    # Autrement on passe à la page suivante (pour cela, on réinitialise le gestionnaire de la fenêtre).
    gest_fenetre.__init__(id_pages, gest_fenetre.num_page_actuelle + 1, window, gest_fenetre.dossier)


# Procédure qui initialise le fichier de réponses en effaçant son contenu et en rajoutant les étiquettes des réponses.
def initialiser_fichier_reponses():
    fichier_reponses = open("Résultats/reponses_eval.csv", "w")
    fichier_reponses.write(
        ";Image_expert;Image_outil_v1;Image_outil_v2;Image_outil_v3;Commentaire_expert;Commentaire_outil_v1"
        ";Commentaire_outil_v2;Commentaire_outil_v3\n")
    fichier_reponses.close()


# Classe qui permet de gérer l'état de la fenêtre à un instant t, stocke la plupart des informations importantes du
# programme.
class Gestionnaire_Fenetre:
    def __init__(self, id_pages, num_page_actuelle, window, dossier):
        # Initialisation des champs de la classe
        self.est_zoome = None
        self.label_4 = None
        self.label_3 = None
        self.label_2 = None
        self.label_1 = None
        self.label_ori = None
        self.img_1 = None
        self.img_2 = None
        self.img_3 = None
        self.img_4 = None
        self.img_originale = None
        self.appart_textes = None
        self.appart_sliders = None
        self.slider_1 = None
        self.slider_2 = None
        self.slider_3 = None
        self.slider_4 = None
        self.text_box_1 = None
        self.text_box_2 = None
        self.text_box_3 = None
        self.text_box_4 = None
        self.window = window
        self.dossier = dossier
        self.num_page_actuelle = num_page_actuelle
        self.id_page = id_pages[num_page_actuelle]
        self.largeur = int(window.winfo_screenwidth()/5)
        self.hauteur = window.winfo_screenheight()-50

        # On génère les trois images à évaluer dans un ordre aléatoire
        self.rand_img = ["_resultat_expert", "_resultat_outil_v1", "_resultat_outil_v2", "_resultat_outil_v3"]
        random.shuffle(self.rand_img)

        # Initialisation et affichage des éléments graphiques de la fenêtre
        self.creer_images()
        self.creer_sliders()
        self.creer_text_boxes()
        creer_bouton_confirmation(self, id_pages, window)

    # Procédure qui réagit à un clic droit de la souris sur une des images, permet de zoomer ou de dézoomer.
    def reagir_zoom(self, num):
        if self.est_zoome:
            # Pour dézoomer, on affiche juste les images originales.
            self.creer_images()
        else:
            self.zoom_images(num)

    # Procédure qui crée et initialise les trois curseurs de notation.
    def creer_sliders(self):
        self.slider_1 = creer_curseurTk(self.window, self, self.largeur)
        self.slider_2 = creer_curseurTk(self.window, self, self.largeur * 2)
        self.slider_3 = creer_curseurTk(self.window, self, self.largeur * 3)
        self.slider_4 = creer_curseurTk(self.window, self, self.largeur * 4)

        # Création d'un dictionnaire contenant l'appartenance des curseurs à leurs images respectives
        self.appart_sliders = {self.rand_img[0]: self.slider_1, self.rand_img[1]: self.slider_2,
                               self.rand_img[2]: self.slider_3, self.rand_img[3]: self.slider_4}

    # Procédure qui crée et initialise les trois boîtes de commentaire.
    def creer_text_boxes(self):
        # Création des textes
        self.text_box_1 = creer_text_box_Tk(self.window, self, self.largeur)
        self.text_box_2 = creer_text_box_Tk(self.window, self, self.largeur * 2)
        self.text_box_3 = creer_text_box_Tk(self.window, self, self.largeur * 3)
        self.text_box_4 = creer_text_box_Tk(self.window, self, self.largeur * 4)

        # Création d'un dictionnaire contenant l'appartenance des textes à leurs images respectives
        self.appart_textes = {self.rand_img[0]: self.text_box_1, self.rand_img[1]: self.text_box_2,
                              self.rand_img[2]: self.text_box_3, self.rand_img[3]: self.text_box_4}

    # Procédure qui créer les images et labels initiaux
    def creer_images(self):
        # Préparation des images
        self.img_originale = creer_imageTk(self.dossier, self.id_page + "_original", self.largeur, self.hauteur)
        self.img_1 = creer_imageTk(self.dossier, self.id_page + self.rand_img[0], self.largeur, self.hauteur)
        self.img_2 = creer_imageTk(self.dossier, self.id_page + self.rand_img[1], self.largeur, self.hauteur)
        self.img_3 = creer_imageTk(self.dossier, self.id_page + self.rand_img[2], self.largeur, self.hauteur)
        self.img_4 = creer_imageTk(self.dossier, self.id_page + self.rand_img[3], self.largeur, self.hauteur)

        # Préparation et placement des labels contenants les images
        if hasattr(self, "label_ori") and self.label_ori is not None:
            self.label_ori.destroy()
        self.label_ori = creer_labelTk(self.window, self, self.img_originale, 0, 0)

        if hasattr(self, "label_1") and self.label_1 is not None:
            self.label_1.destroy()
        self.label_1 = creer_labelTk(self.window, self, self.img_1, self.largeur, 0)

        if hasattr(self, "label_2") and self.label_2 is not None:
            self.label_2.destroy()
        self.label_2 = creer_labelTk(self.window, self, self.img_2, self.largeur * 2, 0)

        if hasattr(self, "label_3") and self.label_3 is not None:
            self.label_3.destroy()
        self.label_3 = creer_labelTk(self.window, self, self.img_3, self.largeur * 3, 0)

        if hasattr(self, "label_4") and self.label_4 is not None:
            self.label_4.destroy()
        self.label_4 = creer_labelTk(self.window, self, self.img_4, self.largeur * 4, 0)

        self.est_zoome = False

    # Procédure qui zoom sur toutes les images à la fois au même endroit.
    def zoom_images(self, num):
        box = (num.x - 20, num.y - 40, num.x + 20, num.y + 40)

        # On zoom sur toutes les images une par une
        self.img_originale = creer_imageTk_decoupee(self.dossier, self.id_page + "_original", self.largeur,
                                                    self.hauteur, box)
        self.label_ori.destroy()
        self.label_ori = creer_labelTk(self.window, self, self.img_originale, 0, 0)

        self.img_1 = creer_imageTk_decoupee(self.dossier, self.id_page + self.rand_img[0], self.largeur, self.hauteur,
                                            box)
        self.label_1.destroy()
        self.label_1 = creer_labelTk(self.window, self, self.img_1, self.largeur, 0)

        self.img_2 = creer_imageTk_decoupee(self.dossier, self.id_page + self.rand_img[1], self.largeur, self.hauteur,
                                            box)
        self.label_2.destroy()
        self.label_2 = creer_labelTk(self.window, self, self.img_2, self.largeur * 2, 0)

        self.img_3 = creer_imageTk_decoupee(self.dossier, self.id_page + self.rand_img[2], self.largeur, self.hauteur,
                                            box)
        self.label_3.destroy()
        self.label_3 = creer_labelTk(self.window, self, self.img_3, self.largeur * 3, 0)

        self.img_4 = creer_imageTk_decoupee(self.dossier, self.id_page + self.rand_img[3], self.largeur, self.hauteur,
                                            box)
        self.label_4.destroy()
        self.label_4 = creer_labelTk(self.window, self, self.img_4, self.largeur * 4, 0)

        self.est_zoome = True

    # Procédure qui confirme les résultats de la page.
    def confirmer(self):
        # On écrit les réponses dans un fichier csv (pour pouvoir manipuler ça par tableur) puis on passe à l'image
        # suivante.
        fichier_reponses = open("Résultats/reponses_eval.csv", "a")
        fichier_reponses.write(self.id_page + ";" +
                               str(self.appart_sliders["_resultat_expert"].get()).replace(".", ",") + ";" +
                               str(self.appart_sliders["_resultat_outil_v1"].get()).replace(".", ",") + ";" +
                               str(self.appart_sliders["_resultat_outil_v2"].get()).replace(".", ",") + ";" +
                               str(self.appart_sliders["_resultat_outil_v3"].get()).replace(".", ",") + ";" +
                               self.appart_textes["_resultat_expert"].get("1.0", "end-1c") + ";" +
                               self.appart_textes["_resultat_outil_v1"].get("1.0", "end-1c") + ";" +
                               self.appart_textes["_resultat_outil_v2"].get("1.0", "end-1c") + ";" +
                               self.appart_textes["_resultat_outil_v3"].get("1.0", "end-1c") +
                               "\n")
        fichier_reponses.close()


dossier = "datas/ressources_evaluateur"

# On récupère les id des pages à utiliser.
id_pages = []
for filename in os.listdir(dossier):
    if filename.endswith("original.png"):
        id_pages.append(filename.replace("_original.png", ""))

window = Tk()
window.title("Évaluation")
window.config(bg="white")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry("%dx%d" % (screen_width, screen_height))
window.attributes('-fullscreen', True)

gestionnaire_fenetre = Gestionnaire_Fenetre(id_pages, 0, window, dossier)
initialiser_fichier_reponses()

window.mainloop()
