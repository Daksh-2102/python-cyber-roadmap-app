import os, json, datetime

STREAK_FILE = "data/streak.json"

def load_streak():
    return load_json(STREAK_FILE, initialize_streak)

def save_streak(streak):
    with open(STREAK_FILE, "w") as f:
        json.dump(streak, f, indent=4)

def initialize_streak():
    streak = {"count": 0, "last_day": None}
    save_streak(streak)
    return streak

def update_streak():
    streak = load_streak()
    today = str(datetime.date.today())
    if streak["last_day"] == today:
        return streak
    if streak["last_day"] is None:
        streak["count"] = 1
    else:
        last = datetime.datetime.strptime(streak["last_day"], "%Y-%m-%d").date()
        if (datetime.date.today() - last).days == 1:
            streak["count"] += 1
        else:
            streak["count"] = 1
    streak["last_day"] = today
    save_streak(streak)
    return streak

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
