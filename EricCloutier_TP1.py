import sys  # Load les modules interpréteur Python / ligne de commande
import json # Load le module JSON
import os   # Load le module Operating System interactions avec ton ordinateur / Windows (fichiers, dossiers, chemins d'accès)
import re   # Module d'expressions régulières pour extraire les nombres du texte, voir ligne 4, 22, 140, 144
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    )
from PySide6.QtCore import Qt # Ce qui va gérer le tri numérique (Qt.DisplayRole) VOIR ligne 135 (mis à jour)


# ------------------------------------------------------------------------------------------
# Cette partie a été ajouté à la fin après avoir réalisé que le tri de taille ne marchait pas
# voir ligne 4, 22, 140, 144
# ------------------------------------------------------------------------------------------
# Classe personnalisée pour gérer le tri numérique sur du texte (ex: "18.5 MB", "120,5 $")
class ItemTriable(QTableWidgetItem):
    def __lt__(self, other):
        val1 = self.data(Qt.UserRole)
        val2 = other.data(Qt.UserRole)

        # Si les deux éléments ont une valeur numérique personnalisée
        if val1 is not None and val2 is not None:
            return val1 < val2

        # Secours : comparaison texte Python pure (évite la récursion avec super())
        return self.text() < other.text()
# ------------------------------------------------------------------------------------------
    
# Vérifie s'il y a fichier JSON fourni
if len(sys.argv) < 2:
    # Affiche l'erreur dans la console
    print("<<<< Attention, Aucun fichier JSON de fourni >>>>")

    # Affiche le pop-up graphique d'erreur
    app_erreur = QApplication.instance() or QApplication(sys.argv)
    QMessageBox.critical(
        None,
        "!!! Attention !!!",
        "Aucun fichier JSON n'a été fourni dans le terminal."
    )
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
    # Affiche l'erreur dans la console
    print(f"<<<< Erreur, le fichier n'a pas été trouvé : {json_path} : {e} >>>>")

    # Affiche le pop-up graphique d'erreur
    app_erreur = QApplication.instance() or QApplication(sys.argv)
    QMessageBox.critical(
        None,
        "Erreur, le fichier n'a pas été trouvé",
        f"!!! Impossible de lire le fichier !!! \n Ce fichier JSON ne porte pas le bon nom :\n{json_path}\n\nDétail : {e}"
    )

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

        # Permet de réorganiser les colonnes de gauche à droite
        self.tableau.horizontalHeader().setSectionsMovable(True)

        # Permet de trier les colonnes (A-Z / Z-A) en cliquant sur l'en-tête
        self.tableau.setSortingEnabled(True)

        # Pernet d'ajuster manuellement les colonnes sur la largeur de la fenêtre
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        # Étire automatiquement la dernière colonne pour éviter un espace vide à droite
        self.tableau.horizontalHeader().setStretchLastSection(True)

        # Remplissage dynamique avec for
        for rows, objet in enumerate(data_json):
            for colonnes, valeur in enumerate(objet.values()):
                item = ItemTriable()

                # Si c'est un nombre (int ou float), sera traîté comme un vrai nombre
                if isinstance(valeur, (int, float)):
                    item.setData(Qt.DisplayRole, valeur)
                    item.setData(Qt.UserRole, float(valeur))    # Sauvegarde pour le tri, voir ligne 4, 22, 140, 144
                else:
                    item.setText(str(valeur)) # Conversion en str() pour éviter les crashs

            # ------------------------------------------------------------------------------------------
            # Cette partie a été ajouté à la fin après avoir réalisé que le tri de taille ne marchait pas
            # voir ligne 4, 22, 140, 144
            # ------------------------------------------------------------------------------------------
                # Extrait le chiffre (ex: "18.5" de "18.5 MB")
                texte_clean = str(valeur).replace(',', '.').strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}", texte_clean):
                    match = re.search(r"[-+]?\d*\.?\d+", texte_clean)
                    if match and match.group():
                        try:
                            item.setData(Qt.UserRole, float(match.group()))  # Enregistre 18.5 dans Qt.UserRole
                        except ValueError:
                            pass
            # ------------------------------------------------------------------------------------------

                self.tableau.setItem(rows, colonnes, item)

        # Permet de lancer le tableau pleine grandeur en fonction des données json
        # Ajuste en 1er chaque colonne au texte  le plus long
        self.tableau.resizeColumnsToContents()

        # Calcule la largeur totale requise par toutes les colonnes + en-tête de ligne
        largeur_totale = self.tableau.verticalHeader().width() + 50
        for col in range(self.tableau.columnCount()):
            largeur_totale += self.tableau.columnWidth(col)

        # Ajuste la largeur de la fenêtre automatiquement avec une limite pré-établie
        largeur_optimale = max(700, min(largeur_totale, 1400))
        self.resize(largeur_optimale, 600)

        # Agencement des layouts
        # Agencement horizontal
        ligne_entete = QHBoxLayout()
        ligne_entete.addWidget(self.texte_info)
        ligne_entete.addWidget(self.champ_recherche)

        # Agencement vertical
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(ligne_entete)    # entête en haut
        layout_principal.addWidget(self.tableau)    # Tableau en bas

        cadre_principal = QWidget()
        cadre_principal.setObjectName("cadrePrincipal") # Nom du cadre pour le style QSS (créer un id)
        cadre_principal.setLayout(layout_principal)

        # Applique le style visuel
        self.appliquer_style()

        # Assigne le cadre_principal comme widget central de la fenêtre
        self.setCentralWidget(cadre_principal)

    # Change le style visuel pour l'interface
    # Placer les instruction entre triple guillemets """ pour le style QSS (sinon double "" à chaque ligne)
    # Pour commenter à l'intérieur du style QSS, utiliser /* commentaire */
    def appliquer_style(self):
        style_qss = """
            /* Style général de la fenêtre principale et du cadre principal */
            #cadrePrincipal, QMainWindow {
                background-color: #e6f4ea;
            }
            /* Texte en haut à gauche */
            QLabel {
                font-family: 'Roboto', sans-serif;
                font-size: 16px;
                font-weight: bold;
                color: #0f5132;
            }
            /* Champ de recherche */
            QLineEdit {
                font-family: 'Roboto', sans-serif;
                background-color: #f0fdf4;
                border: 1px solid #a7f3d0;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 20px;
                color: #064e3b;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
            }
            /* Contour et grille du tableau */
            QTableWidget {
                font-family: 'Roboto', sans-serif;
                background-color: #f0fdf4;
                gridline-color: #bbf7d0;
                border: 1px solid #86efac;
                border-radius: 8px;
                font-size: 13px;
                color: #064e3b;
            }
            /* Cellules du tableau (pour débloquer le survol) */
            QTableWidget::item {
                background-color: #f0fdf4;
                color: #064e3b;
            }
            /* Survol d'une ligne */
            QTableWidget::item:hover {
                background-color: #dcfce7;
                color: #064e3b;
            }
            /* Ligne sélectionnée */
            QTableWidget::item:selected {
                background-color: #16a34a;
                color: #ffffff;
            }
            /* Ligne sélectionnée & survolée avec la souris */
            QTableWidget::item:selected:hover {
                background-color: #15803d;
                color: #ffffff;
            }
            /* En-têtes de colonnes */
            QHeaderView::section {
                font-family: 'Roboto', sans-serif;
                background-color: #bbf7d0;
                color: #064e3b;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """
        self.setStyleSheet(style_qss)
    
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
