import sys # Load les modules interpréteur Python / ligne de commande
import json # Load le module JSON
import os # Load le module Operating System interactions avec ton ordinateur / Windows (fichiers, dossiers, chemins d'accès)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem
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
    nom_fichier = os.path.basename(json_path) # Extrait le nom du fichier
    taille_octets = os.path.getsize(json_path)
    taille_ko = round(taille_octets / 1024, 2) # Convertit en Ko divise par 1024 et garde 2 décimales
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

