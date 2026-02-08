# tools.py
import json
import sqlite3
from datetime import datetime

DB_PATH = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            project TEXT NOT NULL,
            status TEXT DEFAULT 'todo',
            priority TEXT DEFAULT 'normal',
            due_date TEXT,
            description TEXT,
            tags TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_task(title: str, project: str, priority: str = "normal",
             due_date: str = None, description: str = "") -> str: 
    """Add a new task to a project."""
    import uuid
    task_id = str(uuid.uuid4())[:8]
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO tasks (id, title, project, status, priority, due_date, description, created_at) VALUES (?, ?, ?, 'todo', ?, ?, ?, ?)",
        (task_id, title, project, priority, due_date, description, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return json.dumps({"status": "created", "task_id": task_id, "title": title, "project": project})

def list_tasks(project: str = None, status: str = None) -> str:
    """List tasks, optionally filtered by project and/or status."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    if project:
        query += " AND project = ?"
        params.append(project)
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY CASE priority WHEN 'urgent' THEN 1 WHEN 'high' THEN 2 WHEN 'normal' THEN 3 ELSE 4 END"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    tasks = [{"id": r[0], "title": r[1], "project": r[2], "status": r[3], "priority": r[4], "due_date": r[5]} for r in rows]
    return json.dumps(tasks, indent=2)

def update_task(task_id: str, status: str = None, priority: str = None) -> str:
    """Update a task's status or priority."""
    conn = sqlite3.connect(DB_PATH)
    if status:
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    if priority:
        conn.execute("UPDATE tasks SET priority = ? WHERE id = ?", (priority, task_id))
    conn.commit()
    conn.close()
    return json.dumps({"status": "updated", "task_id": task_id})

def get_summary() -> str:
    """Get a summary of tasks across all projects."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT project, status, COUNT(*) FROM tasks
        GROUP BY project, status ORDER BY project
    """).fetchall()
    conn.close()
    summary = {}
    for project, status, count in rows:
        if project not in summary:
            summary[project] = {}
        summary[project][status] = count
    return json.dumps(summary, indent=2)