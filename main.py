from functions import *

tasks = lire_taches_fichier("FichiersTest/table 2.txt")

print("Contenu des taches:", tasks)
afficher_tableau_contraintes(tasks)
creer_matrice(tasks)
print(verifier_proprietes_ordo(tasks))

