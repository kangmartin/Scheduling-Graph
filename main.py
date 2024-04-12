def read_tasks_from_file(filename):
    tasks = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) > 1:
                task_id = int(parts[0])
                duration = int(parts[1])
                predecessors = [int(x) for x in parts[2:]] if len(parts) > 2 else []
                tasks.append((task_id, duration, predecessors))
    return tasks

