# tools/dashboard.py
import json
import os
from rich import print
from rich.table import Table
from config import HISTORY_PATH

def load_projects():
    if not os.path.exists(HISTORY_PATH):
        print("[red]No history.jsonl file found.[/red]")
        return []
    with open(HISTORY_PATH, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def print_summary(projects, min_score=0.0):
    table = Table(title="📚 Research Project Dashboard")
    table.add_column("Index", justify="right")
    table.add_column("Idea", style="cyan", no_wrap=True)
    table.add_column("Score", justify="right")
    table.add_column("Status", style="green")
    table.add_column("Notebook", style="magenta")

    for idx, p in enumerate(projects):
        if p.get("score", {}).get("total", 0) >= min_score:
            table.add_row(
                str(idx),
                p["idea"][:40] + ("..." if len(p["idea"]) > 40 else ""),
                f"{p.get('score', {}).get('total', 0):.1f}",
                p.get("status", "unknown"),
                p.get("notebook_path", "-")
            )
    print(table)

def inspect_project(project):
    print(f"\n[b cyan]📌 Idea:[/b cyan] {project['idea']}")
    print(f"[b green]📊 Score:[/b green] {project.get('score', {}).get('total', 'N/A')}")
    print(f"[b yellow]📦 Dataset:[/b yellow] {project.get('dataset', {}).get('name', 'N/A')}")
    print(f"[b white]🧠 Plan:[/b white]\n{project.get('plan', 'No plan.')}")
    print()

def launch_dashboard():
    projects = load_projects()
    if not projects:
        return
    while True:
        print_summary(projects)
        choice = input("\n🔍 Enter project index to view, or 'q' to quit: ")
        if choice.lower() == 'q':
            break
        try:
            idx = int(choice)
            inspect_project(projects[idx])
        except (ValueError, IndexError):
            print("[red]❌ Invalid input. Try again.[/red]")