from functions import *

tasks = lire_taches_fichier("FichiersTest/test.txt")

print("Contenu des taches:", tasks)
afficher_graph(tasks)
creer_matrice(tasks)
