import sys
import json

# Vérifie s'il y a fichier JSON d'entré pour l'ouvrir
if len(sys.argv) < 2:
    print("Attention, Aucun fichier JSON de fourni")
    sys.exit(1)

json_path = sys.argv[1]
print(f"<<<< Fichier JSON bien reçu: ''{json_path}'' >>>>")

# Charge le fichier JSON sécuritairement (try / except)avec affichage d'erreur si le fichier n'est pas trouvé
try:
    file = open(json_path, "r", encoding="utf-8")
    donnees = json.load(file)
    file.close()

    print(f"<<<< Chargement complété ! Nombre d'éléments : {len(donnees)} >>>>")

except Exception as e:
    print(f"<<<< Erreur, le fichier n'a pas chargé correctement {json_path} : {e} >>>>")
    sys.exit(1)