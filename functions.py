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
