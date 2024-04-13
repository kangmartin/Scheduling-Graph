from functions import *

tasks = lire_taches_fichier("FichiersTest/table 1.txt")

print("Contenu des taches:", tasks)
afficher_tableau_contraintes(tasks)
afficher_matrice(tasks)
print(verifier_cycle(tasks))

