from functions import *

while True:
    choix = input("Veuillez entrer le numéro du test: ")
    tasks = lire_taches_fichier(f"FichiersTest/{choix}.txt")

    print("\nEtape 1: Lecture du tableau de contrainte")
    afficher_tableau_contraintes(tasks)

    print("\nEtape 2: Affichage de la matrice de valeurs")
    matrice = afficher_matrice(tasks)

    if not (verifier_circuit(matrice)) and not (verifier_arcs_negatifs(tasks)):
        print("Les propriétés sont vérifiées !")
        print("\nEtape 4: Calcul des rangs des tâches")
        rangs = calculer_rangs(tasks)
        for task_id, rang in rangs.items():
            print(f"Tâche {task_id}: Rang {rang}")

        print("\nEtape 5: Calcul des dates au plus tôt et au plus tard")
        debut_plus_tot, debut_plus_tard = calculer_dates(tasks, rangs)
        marges = calculer_marges(debut_plus_tot, debut_plus_tard)

        print("Dates au plus tôt:")
        for task_id, date in debut_plus_tot.items():
            print(f"Tâche {task_id}: Début au plus tôt {date}")

        print("\nDates au plus tard:")
        for task_id, date in debut_plus_tard.items():
            print(f"Tâche {task_id}: Début au plus tard {date}")

        afficher_marges_par_rang(marges, rangs)
        afficher_chemin_critique(marges, rangs)
    else:
        print("Les propriétés ne sont pas vérifiées\nProgramme terminé")