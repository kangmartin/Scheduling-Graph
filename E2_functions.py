from prettytable import PrettyTable
import collections


def lire_taches_fichier(filename):
    tasks = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            # Rajouter une liste s'il y a des prédécesseurs
            if len(parts) > 1:
                task_id = int(parts[0])
                duration = int(parts[1])
                predecessors = [int(x) for x in parts[2:]] if len(parts) > 2 else []
                tasks.append((task_id, duration, predecessors))
    return tasks


def calcul_sommets(tasks):
    # Nombre de tâches + 2 pour les sommets fictifs α (0) et ω (N+1)
    sommets_count = len(tasks) + 2
    return sommets_count


def calcul_arc(tasks):
    arc_count = 0
    has_predecessors = set()
    all_tasks = set()

    # Compter les arcs en fonction des prédécesseurs
    for task_id, _, predecessors in tasks:
        all_tasks.add(task_id)
        if predecessors:
            arc_count += len(predecessors)
            has_predecessors.update(predecessors)
        else:
            # Tâche sans prédécesseur, un arc depuis alpha
            arc_count += 1

    # Ajouter un arc vers ω pour les tâches sans successeurs
    no_successors = all_tasks - has_predecessors
    arc_count += len(no_successors)
    return arc_count


def afficher_tableau_contraintes(tasks):
    table = PrettyTable()
    table.field_names = ["Tâche", "Durée", "Contraintes"]
    print("Le tableau de contrainte contient:\n-", calcul_sommets(tasks), "sommets", "\n-", calcul_arc(tasks), "arcs")
    for task_id, duration, constraints in tasks:
        # Convertir les contraintes en chaîne de caractères ou laisser vide si pas de contraintes
        constraints_str = ', '.join(str(c) for c in constraints) if constraints else ""
        table.add_row([f"Tâche {task_id}", f"{duration}", f"[{constraints_str}]"])

    # Afficher le tableau
    print("\nTableau de contraintes:")
    print(table)
    print("\n* Création du graphe d’ordonnancement :\n")
    pred = []
    for i in tasks:
        pred.append(i[2])
    for j in range(len(pred)):
        if len(pred[j]) == 0:
            print("0 ->", tasks[j][0], "= 0")
        else:
            for z in range(len(pred[j])):
                print(pred[j][z], "->", tasks[j][0], "=", tasks[pred[j][z] - 1][1])

    all_tasks = set(task[0] for task in tasks)
    tasks_with_predecessors = set(pred for task in tasks for pred in task[2])
    tasks_without_successors = all_tasks - tasks_with_predecessors
    omega = max(all_tasks) + 1
    for task in tasks:
        if task[0] in tasks_without_successors:
            print(task[0], "->", omega, "=", task[1])


def afficher_matrice(tasks):
    print("\nMatrice de valeurs: ")
    # Calculer le nombre total de sommets
    sommets_count = len(tasks) + 2  # Inclut α et ω
    omega = sommets_count - 1

    # Initialisation de la matrice avec '*'
    matrice = [['*' for _ in range(sommets_count)] for _ in range(sommets_count)]

    # Remplir la matrice avec les poids des arcs
    for task_id, duration, predecessors in tasks:
        if not predecessors:
            # Arc depuis α vers la tâche sans prédécesseurs
            matrice[0][task_id] = 0
        for pred in predecessors:
            # Arcs depuis les prédécesseurs vers la tâche actuelle
            matrice[pred][task_id] = tasks[pred - 1][1]  # duration of the predecessor
    # Ajouter les arcs vers ω
    all_tasks = set(task[0] for task in tasks)
    tasks_with_predecessors = set(pred for task in tasks for pred in task[2])
    tasks_without_successors = all_tasks - tasks_with_predecessors
    for task_id in tasks_without_successors:
        matrice[task_id][omega] = tasks[task_id - 1][1]  # duration of the task
    table = PrettyTable()
    table.field_names = [" "] + [str(i) for i in range(sommets_count)]
    for i in range(sommets_count):
        table.add_row([str(i)] + matrice[i])

    print(table)
    return matrice


def verifier_arcs_negatifs(taches):
    for _, duration, _ in taches:
        if duration < 0:
            print("-> Il y a un arc négatif.")
            return True  # Indique la présence d'un arc négatif
    print("-> Il n’y a pas d’arcs négatifs.")
    return False  # Aucun arc négatif détecté


def verifier_circuit(matrice):
    points_entree = [0]
    sommets_restants = []
    for i in range(len(matrice)):
        sommets_restants.append(i)
    print("** Détection de circuit\n** Méthode d’élimination des points d’entrée\n")
    print("Points d'entrée: 0")
    print("Suppression des points d'entrée")
    for val in points_entree:
        if val in sommets_restants:
            sommets_restants.remove(val)
    print("Sommets restants:", sommets_restants)
    points_entree = []
    for i in range(len(matrice[0])):
        if not matrice[0][i] == "*":
            points_entree.append(i)

    while True:
        if not points_entree:
            print("-> Il y a un circuit\n")
            return True
        print("Points d'entrée:", points_entree)
        print("Suppression des points d'entrée")
        for val in points_entree:
            if val not in sommets_restants:  # vérifier si le point est dans sommets_restants
                print("-> Il y a un circuit")
                return True
            sommets_restants.remove(val)
        print("Sommets restant:", sommets_restants)

        if not sommets_restants:  # vérifier si sommets_restants est vide
            print("-> Il n'y a pas de circuit")
            return False

        for j in range(len(matrice[0])):
            for i in range(len(matrice)):
                if i in points_entree:  # vérifier si l'index de la ligne est égal à val
                    matrice[i][j] = "*"

        points_entree = []
        for j in range(1, len(matrice[0])):  # itérer sur chaque colonne
            if all(matrice[i][j] == '*' for i in range(len(matrice))):  # vérifier si tous les éléments sont '*'
                points_entree.append(j)  # ajouter l'indice de la colonne à points_entree
        for j in points_entree:
            for i in range(len(matrice)):
                matrice[i][j] = 'X'


def calculer_rangs(taches):
    # Initialisation des rangs
    rangs = {0: 0}  # α initialise à rang 0
    for task_id, _, _ in taches:
        rangs[task_id] = 0  # Initialise à 0 pour éviter les clés manquantes

    # Omega
    omega = len(taches) + 1
    rangs[omega] = 0  # Initialise Omega à 0 temporairement

    # Calcul des rangs en fonction des prédécesseurs
    change = True # Indique si un changement a été effectué
    while change:
        change = False
        for task_id, _, predecessors in taches:
            if predecessors:
                current_max_rang = max(rangs[pred] for pred in predecessors if pred in rangs) + 1 # Rang max des prédécesseurs
                if rangs[task_id] < current_max_rang: # Mettre à jour le rang si nécessaire
                    rangs[task_id] = current_max_rang
                    change = True
            elif task_id != 0 and rangs[task_id] == 0:  # Les tâches sans prédécesseurs autres qu'Alpha
                rangs[task_id] = 1 # Mettre à jour le rang si nécessaire
                change = True

    # Le rang de ω (Omega) doit être le max des rangs + 1
    rangs[omega] = max(rangs.values()) + 1

    # Trier les rangs par ordre croissant des clés pour la présentation
    rangs = collections.OrderedDict(sorted(rangs.items()))

    return rangs


def calculer_dates(tasks, rangs):
    debut_plus_tot = {}
    debut_plus_tard = {}

    # Initialisation avec α
    debut_plus_tot[0] = 0  # α commence à 0

    # Omega, indice du dernier sommet
    omega = len(tasks) + 1

    # Calcul des dates au plus tôt
    # Trier les tâches par rang pour assurer le traitement dans l'ordre correct
    sorted_tasks = sorted(tasks, key=lambda x: rangs[x[0]])
    for task_id, duration, predecessors in sorted_tasks:
        if not predecessors:
            # Si pas de prédécesseurs et pas α, elle commence après α directement
            if task_id != 0:  # Ignorer α puisqu'il est déjà initialisé
                debut_plus_tot[task_id] = debut_plus_tot[0]
        else:
            # Max des fins des prédécesseurs
            max_pred_fin = max(debut_plus_tot[pred] + tasks[pred - 1][1] for pred in predecessors) # Max des fins des prédécesseurs
            debut_plus_tot[task_id] = max_pred_fin # Début après la fin des prédécesseurs

    # La date au plus tôt pour Omega est la max des fins des tâches sans successeurs
    tasks_with_no_successors = [task_id for task_id, _, preds in tasks if not any(task_id in s[2] for s in tasks)] # Tâches sans successeurs
    if tasks_with_no_successors:
        debut_plus_tot[omega] = max(debut_plus_tot[task] + tasks[task - 1][1] for task in tasks_with_no_successors) # Max des fins des tâches sans successeurs

    # Calcul des dates au plus tard en commençant par Omega
    debut_plus_tard[omega] = debut_plus_tot[omega]
    for task_id, duration, _ in sorted_tasks[::-1]:
        successors = [succ for succ, _, preds in tasks if task_id in preds]
        if not successors:
            # Si pas de successeurs et pas Omega, elle doit finir avant Omega
            if task_id != omega:
                debut_plus_tard[task_id] = debut_plus_tard[omega] - duration
        else:
            # Min des débuts des successeurs
            min_succ_start = min(debut_plus_tard[succ] for succ in successors)
            debut_plus_tard[task_id] = min_succ_start - duration

    return debut_plus_tot, debut_plus_tard

def afficher_dates(debut_plus_tot, debut_plus_tard):
    # Créer une instance de PrettyTable
    table = PrettyTable()

    # Définir les en-têtes de colonnes
    table.field_names = ["Tâche", "Début au plus tôt", "Début au plus tard"]

    # Parcourir les tâches et ajouter les dates au tableau
    for task_id in sorted(debut_plus_tot.keys()):
        table.add_row([f"Tâche {task_id}", debut_plus_tot[task_id], debut_plus_tard[task_id]])

    # Afficher le tableau
    print(table)

def calculer_marges(debut_plus_tot, debut_plus_tard):
    marges = {}
    # Trouver toutes les tâches
    all_tasks = set(debut_plus_tot.keys()).union(set(debut_plus_tard.keys())) # Rassembler les dates pour calculer les marges
    for task_id in all_tasks:
        if task_id not in debut_plus_tot:
            debut_plus_tot[task_id] = float('inf')
        if task_id not in debut_plus_tard:
            debut_plus_tard[task_id] = debut_plus_tot[task_id]

        # Calculer la marge
        marges[task_id] = debut_plus_tard[task_id] - debut_plus_tot[task_id]
    return marges


def afficher_marges_par_rang(marges, rangs):
    # Créer une liste de tâches triées par leurs rangs
    taches_triees = sorted(marges.keys(), key=lambda x: rangs.get(x, float('inf')))

    print("\nMarges:")
    for task_id in taches_triees: # Afficher les marges triées par rang
        print(f"Tâche {task_id}: Marge {marges[task_id]}")


def afficher_chemin_critique(marges, rangs):
    # Identifier les tâches qui font partie du chemin critique
    chemin_critique = [task_id for task_id, marge in marges.items() if marge == 0]

    # Trier les tâches du chemin critique par leurs rangs pour une présentation ordonnée
    chemin_critique_sorted = sorted(chemin_critique, key=lambda x: rangs.get(x, float('inf')))

    print("\nChemin Critique:")
    for task_id in chemin_critique_sorted:
        print(f"Tâche {task_id}", end=", ")
    print("\n")