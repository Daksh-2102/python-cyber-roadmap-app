import streamlit as st
from tasks import load_tasks, save_tasks
from streak import load_streak, update_streak
from roadmap import ROADMAP
import datetime

st.set_page_config(page_title="Roadmap Dashboard", layout="wide")

# -----------------------
# Load data
# -----------------------
tasks = load_tasks()
streak = load_streak()
today = datetime.date.today()

# -----------------------
# Sidebar: Streak + Today's Tasks + Add Task
# -----------------------
st.sidebar.title("🔥 Your Streak")
st.sidebar.metric("Current Streak", streak["count"])

st.sidebar.header("📌 Today's Tasks")
for week, week_tasks in tasks.items():
    day_index = today.weekday()  # Monday=0
    daily_tasks = week_tasks[day_index::7]
    for t in daily_tasks:
        key = f"{week}-daily-{t['task']}"
        checked = st.sidebar.checkbox(f"{week}: {t['task']}", value=t["done"], key=key)
        if checked != t["done"]:
            t["done"] = checked
            # Add 'done_date' if completed today
            t["done_date"] = str(today)
            save_tasks(tasks)
            update_streak()
            streak = load_streak()

# Add custom task
st.sidebar.header("➕ Add Custom Task")
custom_week = st.sidebar.selectbox("Week", list(tasks.keys()))
custom_task = st.sidebar.text_input("Task Name")
if st.sidebar.button("Add Task"):
    if custom_task.strip() != "":
        tasks[custom_week].append({"task": custom_task.strip(), "done": False})
        save_tasks(tasks)
        st.sidebar.success(f"Task added to {custom_week}")
    else:
        st.sidebar.error("Task name cannot be empty")

# -----------------------
# Main Dashboard
# -----------------------
st.title("📚 Python + Cybersecurity Roadmap Dashboard")

# Weekly Progress Overview
st.write("### Weekly Progress Overview")
for week, week_tasks in tasks.items():
    completed = sum(1 for t in week_tasks if t["done"])
    total = len(week_tasks)
    st.write(f"**{week}**: {completed}/{total} tasks completed")
    st.progress(completed / total)

# Weekly Task Details
st.write("### Detailed Tasks")
selected_week = st.selectbox("Select Week to View/Edit Tasks", list(tasks.keys()))
for i, t in enumerate(tasks[selected_week]):
    key = f"{selected_week}-{i}"
    checked = st.checkbox(t["task"], value=t["done"], key=key)
    if checked != t["done"]:
        t["done"] = checked
        if checked:
            t["done_date"] = str(today)
        save_tasks(tasks)
        update_streak()
        streak = load_streak()

# -----------------------
# Streak Tracker + GitHub-style Calendar
# -----------------------
st.write("### Streak Tracker")
st.write(f"You have a streak of **{streak['count']} days**")
st.write("✅ Complete at least one task every day to maintain your streak!")

# GitHub-style 30-day streak calendar
st.write("### Streak Calendar (Last 30 Days)")
start_day = today - datetime.timedelta(days=29)
dates = [start_day + datetime.timedelta(days=i) for i in range(30)]
calendar_row = ""
for d in dates:
    completed_any = False
    day_str = str(d)
    for week_tasks in tasks.values():
        for t in week_tasks:
            if t.get("done_date", "") == day_str:
                completed_any = True
                break
    calendar_row += "🟩" if completed_any else "⬜"
st.text(calendar_row)
