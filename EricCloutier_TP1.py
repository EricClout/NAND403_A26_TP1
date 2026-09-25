import sys # Load les modules interpréteur Python / ligne de commande
import json # Load le module JSON
import os # Load le module Operating System interactions avec ton ordinateur / Windows (fichiers, dossiers, chemins d'accès)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QHeaderView,
    QLineEdit,
    QAbstractItemView
    )


# Vérifie s'il y a fichier JSON fourni
if len(sys.argv) < 2:
    print("<<<< Attention, Aucun fichier JSON de fourni >>>>")
    sys.exit(1)

json_path = sys.argv[1]
print(f"<<<< Fichier JSON bien reçu: ''{json_path}'' >>>>")

# Charge le fichier JSON sécuritairement (try / except) avec affichage d'erreur si le fichier n'est pas trouvé
try:
    file = open(json_path, "r", encoding="utf-8") # Encodage pour les mots accentués Windows
    data = json.load(file)
    file.close()

    # Récupère les info métadonnées du fichier JSON
    nom_fichier = os.path.basename(json_path)   # Extrait le nom du fichier
    taille_octets = os.path.getsize(json_path)
    taille_ko = round(taille_octets / 1024, 2)  # Convertit en Ko divise par 1024 et garde 2 décimales
    nb_elements = len(data)

    # print affiche les info du fichier JSON
    print(f"<<<< Chargement complété ! >>>>")
    print(f" : Nom du fichier : {nom_fichier}")
    print(f" : Taille : {taille_ko} Ko")
    print(f" : Nombre d'éléments : {nb_elements}")


except Exception as e:
    print(f"<<<< Erreur, le fichier n'a pas chargé correctement {json_path} : {e} >>>>")
    sys.exit(1)


    # ----------------------------------------------------------------------------------------------------
    # Initialisation de l'interface graphique
    # ----------------------------------------------------------------------------------------------------

class FenetrePrincipale(QMainWindow):
    def __init__(self, data_json):
        super().__init__()

        self.setWindowTitle(f"Données du fichier JSON")
        self.resize(800, 600)

        # Crée un label (étiquette) pour afficher les métadonnées
        texte_data = f"Fichier : {nom_fichier}  |  Taille : {taille_ko} Ko  |  Éléments : {nb_elements}"
        self.texte_info = QLabel(texte_data)

        # Champ de recherche (QLineEdit)
        self.champ_recherche = QLineEdit()
        self.champ_recherche.setPlaceholderText("Ce Que Je Veux Rechercher...")
        self.champ_recherche.textChanged.connect(self.filtrer_tableau) # Connexion textChanged à la méthode de filtrage

        # Crée un tableau + config de la grille
        self.tableau = QTableWidget()
        self.tableau.setRowCount(len(data_json))
        self.tableau.setColumnCount(len(data_json[0]))
        self.tableau.setHorizontalHeaderLabels(list(data_json[0].keys()))

        # Empêche l'édition des cellules du tableau
        self.tableau.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Ajustement automatique des colonnes sur la largeur de la fenêtre
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Remplissage dynamique avec for
        for rows, objet in enumerate(data_json):
            for colonnes, valeur in enumerate(objet.values()):
                item = QTableWidgetItem(str(valeur)) # Conversion en str() pour éviter les crashs
                self.tableau.setItem(rows, colonnes, item)

        # Agencement des layouts
        # Agencement horizontal
        ligne_entete = QHBoxLayout()
        ligne_entete.addWidget(self.texte_info)
        ligne_entete.addWidget(self.champ_recherche)

        # Agencement vertical
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(ligne_entete)    # Métadonnées en haut
        layout_principal.addWidget(self.tableau)    # Tableau en bas

        cadre_principal = QWidget()
        cadre_principal.setLayout(layout_principal)

        # Assigne le cadre_principal comme widget central de la fenêtre
        self.setCentralWidget(cadre_principal)

    # Masque ou affiche les lignes du tableau selon le texte recherché.
    def filtrer_tableau(self, texte):
        texte = texte.lower()  # Ignore les majuscules / minuscules

        # Parcourt toutes les lignes du tableau
        for row in range(self.tableau.rowCount()):
            ligne_visible = False

            # Parcourt chaque colonne de la ligne actuelle
            for colonne in range(self.tableau.columnCount()):
                item = self.tableau.item(row, colonne)
                if item and texte in item.text().lower():
                    ligne_visible = True
                    break
            self.tableau.setRowHidden(row, not ligne_visible)  # Cache la ligne si elle ne correspond pas

#Lancement de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale(data)
    fenetre.show()
    sys.exit(app.exec())
