from E2_functions import *

while True:
    choix = input("\nVeuillez entrer le numéro du test: ")
    tasks = lire_taches_fichier(f"FichiersTest/E2_{choix}.txt")

    print("===================================================================")
    print("\nEtape 1: Lecture du tableau de contrainte\n")
    afficher_tableau_contraintes(tasks)
    print("\n===================================================================")

    print("\nEtape 2: Affichage de la matrice de valeurs")
    matrice = afficher_matrice(tasks)
    print("\n===================================================================")

    print("\nEtape 3: Verification des propriétés (pas de circuits et pas d'arcs)\n")
    if not (verifier_circuit(matrice)) and not (verifier_arcs_negatifs(tasks)):
        print("\n===================================================================")

        print("\nEtape 4: Calcul des rangs des tâches\n")
        rangs = calculer_rangs(tasks)
        for task_id, rang in rangs.items():
            print(f"Tâche {task_id}: Rang {rang}")
        print("\n===================================================================")

        print("\nEtape 5: Calcul des dates au plus tôt et au plus tard et des marges\n")
        debut_plus_tot, debut_plus_tard = calculer_dates(tasks, rangs)
        marges = calculer_marges(debut_plus_tot, debut_plus_tard)

        print("Dates au plus tôt:")
        for task_id, date in debut_plus_tot.items():
            print(f"Tâche {task_id}: {date}")

        print("\nDates au plus tard:")
        for task_id, date in debut_plus_tard.items():
            print(f"Tâche {task_id}: {date}")
        afficher_marges_par_rang(marges, rangs)
        print("\n===================================================================")
        print("\nEtape 6: Calcul et affichage des chemins critiques:")
        afficher_chemin_critique(marges, rangs)
    else:
        print("\n===================================================================")
        print("Les proprités ne sont pas verifiées (circuits et/ou arcs negatifs), fin du programme.")
    print("===================================================================")