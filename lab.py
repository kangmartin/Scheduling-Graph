# Fichiers contenant les fonctions abandonées ou en phase experimentales
import collections

from functions import calcul_sommets, calcul_arc


def afficher_graph(tasks):
    print("Le fichier à:", calcul_sommets(tasks), "sommets")
    print("Le fichier à:", calcul_arc(tasks), "arcs")
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
def verifier_cycle(taches):

    # Construction du graphe d'adjacence et du compteur de prédécesseurs
    graphe = collections.defaultdict(list)
    predecesseurs = collections.Counter()

    # Initialisation du graphe et du compteur
    for tache, _, preds in taches:
        for pred in preds:
            graphe[pred].append(tache)
        predecesseurs[tache] += len(preds)

    # Obtenir tous les sommets (tâches)
    sommets = set(predecesseurs.keys()).union(set(graphe.keys()))

    # Initialisation de la file de traitement avec les tâches sans prédécesseur
    file_traitement = [tache for tache in sommets if predecesseurs[tache] == 0]
    print(f"Points d’entrée : {' '.join(map(str, file_traitement)) if file_traitement else 'Aucun'}")

    traitees = 0

    # Processus de suppression des points d'entrée (tâches sans prédécesseurs)
    while file_traitement:
        print("Suppression des points d’entrée")
        next_file = []
        while file_traitement:
            tache = file_traitement.pop(0)
            traitees += 1
            for suivant in graphe[tache]:
                predecesseurs[suivant] -= 1
                if predecesseurs[suivant] == 0:
                    next_file.append(suivant)

        file_traitement = next_file
        restants = set(sommets) - set(tache for tache, count in predecesseurs.items() if count == 0)
        print(f"Sommets restant : {' '.join(map(str, restants)) if restants else 'Aucun'}")
        if file_traitement:
            print(f"Points d’entrée : {' '.join(map(str, file_traitement))}")

    # Vérification que toutes les tâches ont été traitées
    if traitees == len(sommets):
        print("-> Il n’y a pas de circuit")
        return False  # Aucun cycle détecté
    else:
        print("-> Il y a un circuit")
        return True  # Présence d'un cycle