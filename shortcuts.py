# shortcuts.py
"""
Hybrid shortcut system for task management agent.
- Fast shortcuts: Execute directly without AI
- AI shortcuts: Expand to natural language and use AI context
"""

import json
from typing import Optional, Tuple
from tools import (
    get_projects, get_summary, list_tasks,
    get_tasks_due_today, delete_task, search_tasks
)

# ANSI color codes for better terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def format_projects(json_str: str) -> str:
    """Format project list for display."""
    projects = json.loads(json_str)
    if not projects:
        return f"{Colors.YELLOW}No projects found.{Colors.END}"

    output = [f"\n{Colors.BOLD}{Colors.BLUE}📁 Your Projects:{Colors.END}\n"]
    for p in projects:
        completion_rate = (p['completed'] / p['total_tasks'] * 100) if p['total_tasks'] > 0 else 0
        bar_length = 20
        filled = int(bar_length * completion_rate / 100)
        bar = '█' * filled + '░' * (bar_length - filled)

        output.append(
            f"{Colors.CYAN}{p['name']}{Colors.END}: "
            f"{p['completed']}/{p['total_tasks']} tasks "
            f"[{bar}] {completion_rate:.0f}%"
        )
    return "\n".join(output) + "\n"


def format_summary(json_str: str) -> str:
    """Format summary for display."""
    summary = json.loads(json_str)
    if not summary:
        return f"{Colors.YELLOW}No tasks found.{Colors.END}"

    output = [f"\n{Colors.BOLD}{Colors.BLUE}📊 Task Summary:{Colors.END}\n"]
    for project, statuses in summary.items():
        total = sum(statuses.values())
        output.append(f"\n{Colors.CYAN}{Colors.BOLD}{project}{Colors.END} ({total} tasks):")
        for status, count in statuses.items():
            emoji = {"todo": "⏳", "in_progress": "🔄", "done": "✅", "blocked": "🚫"}.get(status, "📌")
            output.append(f"  {emoji} {status}: {count}")
    return "\n".join(output) + "\n"


def format_tasks(json_str: str) -> str:
    """Format task list for display."""
    tasks = json.loads(json_str)
    if not tasks:
        return f"{Colors.YELLOW}No tasks found.{Colors.END}"

    output = [f"\n{Colors.BOLD}Found {len(tasks)} task(s):{Colors.END}\n"]
    for task in tasks:
        priority_emoji = {"urgent": "🔴", "high": "🟠", "normal": "🟢", "low": "🔵"}.get(task['priority'], "⚪")
        status_emoji = {"todo": "⏳", "in_progress": "🔄", "done": "✅", "blocked": "🚫"}.get(task['status'], "📌")

        due = f" | Due: {task['due_date']}" if task.get('due_date') else ""
        output.append(
            f"{priority_emoji} {status_emoji} [{Colors.CYAN}{task['id']}{Colors.END}] "
            f"{task['title']} ({Colors.YELLOW}{task['project']}{Colors.END}){due}"
        )
    return "\n".join(output) + "\n"


def show_help() -> str:
    """Display all available shortcuts."""
    help_text = f"""
{Colors.BOLD}{Colors.BLUE}🚀 Task Manager Shortcuts{Colors.END}

{Colors.BOLD}Fast Shortcuts{Colors.END} (instant execution):
  {Colors.GREEN}/projects{Colors.END}        - List all projects with progress
  {Colors.GREEN}/summary{Colors.END}         - Show task summary dashboard
  {Colors.GREEN}/urgent{Colors.END}          - List all urgent priority tasks
  {Colors.GREEN}/today{Colors.END}           - Show tasks due today
  {Colors.GREEN}/help{Colors.END}            - Show this help message

{Colors.BOLD}AI-Enhanced Shortcuts{Colors.END} (natural language):
  {Colors.CYAN}/add{Colors.END} <text>       - Quick add task (AI parses project/priority)
                      Example: /add Buy milk for grocery project urgent
  {Colors.CYAN}/list{Colors.END} <project>   - List tasks in specific project
                      Example: /list grocery
  {Colors.CYAN}/done{Colors.END} <task_id>   - Mark task as completed
                      Example: /done abc123ef
  {Colors.CYAN}/delete{Colors.END} <task_id> - Delete a task
                      Example: /delete abc123ef
  {Colors.CYAN}/search{Colors.END} <query>   - Search tasks by text
                      Example: /search meeting

{Colors.BOLD}Natural Language{Colors.END} (anything else):
  Just type normally and the AI will help!
  Example: "Show me all blocked tasks in the client project"

{Colors.YELLOW}Tip:{Colors.END} Fast shortcuts are instant. AI shortcuts use context for smarter parsing!
"""
    return help_text


# Fast shortcuts - execute directly without AI
FAST_SHORTCUTS = {
    '/projects': lambda args: format_projects(get_projects()),
    '/summary': lambda args: format_summary(get_summary()),
    '/urgent': lambda args: format_tasks(list_tasks(priority='urgent')),
    '/today': lambda args: format_tasks(get_tasks_due_today()),
    '/help': lambda args: show_help(),
}


# AI-enhanced shortcuts - expand to natural language with context
AI_SHORTCUTS = {
    '/add': lambda args: f"Add a new task: {args}. Parse the project name, priority, and description from the text intelligently.",
    '/list': lambda args: f"List all tasks in the '{args}' project" if args else "List all tasks across all projects",
    '/done': lambda args: f"Mark task {args} as done",
    '/delete': lambda args: f"Delete task {args}",
    '/search': lambda args: f"Search for tasks containing: {args}",
}


def process_shortcut(user_input: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Process shortcut commands.

    Returns:
        (response, modified_input)
        - If fast shortcut: (response, None) - display response directly
        - If AI shortcut: (None, expanded_prompt) - send to AI
        - If not a shortcut: (None, original_input) - pass through
    """
    if not user_input.startswith('/'):
        return None, user_input

    # Parse shortcut and arguments
    parts = user_input.split(maxsplit=1)
    shortcut = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    # Check fast shortcuts
    if shortcut in FAST_SHORTCUTS:
        try:
            response = FAST_SHORTCUTS[shortcut](args)
            return response, None
        except Exception as e:
            return f"{Colors.RED}Error executing shortcut: {str(e)}{Colors.END}", None

    # Check AI shortcuts
    if shortcut in AI_SHORTCUTS:
        if not args and shortcut not in ['/list']:
            return f"{Colors.YELLOW}Usage: {shortcut} <arguments>{Colors.END}\nType /help for more info.", None
        expanded = AI_SHORTCUTS[shortcut](args)
        return None, expanded

    # Unknown shortcut
    return f"{Colors.YELLOW}Unknown shortcut: {shortcut}{Colors.END}\nType /help to see available shortcuts.", None
