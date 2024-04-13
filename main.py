from functions import *

tasks = lire_taches_fichier("FichiersTest/test.txt")

print("Contenu des taches:", tasks)
print("Le fichier à:", calcul_sommets(tasks), "sommets")
print("Le fichier à:", calcul_arc(tasks), "arcs")
