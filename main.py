from functions import *

while True:
    choix = input("Veuillez entrer le numero du test: ")
    tasks = lire_taches_fichier(f"FichiersTest/{choix}.txt")
    print(tasks)

    print("\n===========================================================\n")
    print("Etape 1: Lecture du tableau de contrainte")
    afficher_tableau_contraintes(tasks)

    print("\n===========================================================\n\n")
    print("Etape 2: Affichage de la matrice de valeurs")
    afficher_matrice(tasks)

    print("\n===========================================================\n\n")
    print("Etape 3: Verification des propriétés d'ordonnancement")
    verifier_cycle(tasks)








