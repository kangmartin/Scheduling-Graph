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
    print(matrice)
    table = PrettyTable()
    table.field_names = [" "] + [str(i) for i in range(sommets_count)]
    for i in range(sommets_count):
        table.add_row([str(i)] + matrice[i])

    print(table)
    return matrice


def verifier_arcs_negatifs(taches):
    for _, duration, _ in taches:
        if duration < 0:
            print("Il y a un arc négatif.")
            return True  # Indique la présence d'un arc négatif
    print("Il n’y a pas d’arcs négatifs.")
    return False  # Aucun arc négatif détecté


def verifier_circuit(matrice):
    points_entree = [0]
    sommets_restants = []
    for i in range(len(matrice)):
        sommets_restants.append(i)
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
            print("Il y a un cycle")
            return True
        print("Points d'entrée:", points_entree)
        print("Suppression des points d'entrée")
        for val in points_entree:
            if val not in sommets_restants:  # vérifier si le point est dans sommets_restants
                print("Il y a un cycle")
                return True
            sommets_restants.remove(val)
        print("Sommets restant:", sommets_restants)

        if not sommets_restants:  # vérifier si sommets_restants est vide
            print("Il y a pas de cycle")
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
