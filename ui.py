from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()

def show_week(tasks, week):
    console.print(f"\n📅 [bold cyan]{week} Tasks[/bold cyan]")
    completed = sum(1 for t in tasks[week] if t["done"])
    total = len(tasks[week])

    with Progress() as progress:
        progress.add_task("Progress", total=total, completed=completed)

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("No", width=5)
    table.add_column("Task")
    table.add_column("Status", width=10)

    for i, t in enumerate(tasks[week], 1):
        status = "[green]✔️[/green]" if t["done"] else "[red]❌[/red]"
        table.add_row(str(i), t["task"], status)

    console.print(table)

def show_streak(streak):
    console.print(f"\n🔥 Current Streak: [bold yellow]{streak['count']} days[/bold yellow]")
