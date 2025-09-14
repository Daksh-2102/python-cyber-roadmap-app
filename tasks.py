import os, json
from roadmap import ROADMAP

TASK_FILE = "data/tasks.json"

def load_tasks():
    return load_json(TASK_FILE, initialize_tasks)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def initialize_tasks():
    tasks = {}
    for week, week_tasks in ROADMAP.items():
        tasks[week] = [{"task": t, "done": False} for t in week_tasks]
    save_tasks(tasks)
    return tasks

def mark_task(tasks, week, task_no):
    tasks[week][task_no - 1]["done"] = True
    save_tasks(tasks)

# Robust JSON loader
def load_json(file_path, init_function):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                if not data:  # empty file
                    raise ValueError
                return data
        else:
            return init_function()
    except (json.JSONDecodeError, ValueError):
        # If file is empty or corrupted
        return init_function()
