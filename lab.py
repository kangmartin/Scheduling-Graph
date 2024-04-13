# Fichiers contenant les fonctions abandonées ou en phase experimentales
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
