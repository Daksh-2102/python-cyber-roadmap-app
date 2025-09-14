from tasks import load_tasks, mark_task
from streak import load_streak, update_streak
from ui import show_week, show_streak

def main():
    tasks = load_tasks()
    streak = load_streak()

    while True:
        print("\n--- Roadmap Tracker ---")
        print("1. Show Week Tasks")
        print("2. Mark Task Complete")
        print("3. Show Streak")
        print("4. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            week = input("Enter week (Week 1, Week 2...): ")
            if week in tasks:
                show_week(tasks, week)
            else:
                print("❌ Invalid week")
        elif choice == "2":
            week = input("Enter week: ")
            if week in tasks:
                show_week(tasks, week)
                try:
                    num = int(input("Enter task number: "))
                    mark_task(tasks, week, num)
                    update_streak()
                except:
                    print("❌ Invalid number")
            else:
                print("❌ Invalid week")
        elif choice == "3":
            show_streak(streak)
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
