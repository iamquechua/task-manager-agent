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

def list_tasks(project: str = None, status: str = None, priority: str = None) -> str:
    """List tasks, optionally filtered by project, status, and/or priority."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    if project:
        query += " AND project = ?"
        params.append(project)
    if status:
        query += " AND status = ?"
        params.append(status)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
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

def get_projects() -> str:
    """Get a list of all unique projects with task counts."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT project, COUNT(*) as total,
               SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) as completed
        FROM tasks
        GROUP BY project
        ORDER BY project
    """).fetchall()
    conn.close()
    projects = [{"name": r[0], "total_tasks": r[1], "completed": r[2]} for r in rows]
    return json.dumps(projects, indent=2)

def delete_task(task_id: str) -> str:
    """Delete a task by its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted > 0:
        return json.dumps({"status": "deleted", "task_id": task_id})
    else:
        return json.dumps({"status": "not_found", "task_id": task_id})

def search_tasks(query: str) -> str:
    """Search tasks by text in title or description."""
    conn = sqlite3.connect(DB_PATH)
    search_pattern = f"%{query}%"
    rows = conn.execute("""
        SELECT id, title, project, status, priority, due_date, description
        FROM tasks
        WHERE title LIKE ? OR description LIKE ?
        ORDER BY CASE priority WHEN 'urgent' THEN 1 WHEN 'high' THEN 2 WHEN 'normal' THEN 3 ELSE 4 END
    """, (search_pattern, search_pattern)).fetchall()
    conn.close()
    tasks = [{"id": r[0], "title": r[1], "project": r[2], "status": r[3], "priority": r[4], "due_date": r[5], "description": r[6]} for r in rows]
    return json.dumps(tasks, indent=2)

def get_tasks_due_today() -> str:
    """Get all tasks due today."""
    today = datetime.now().date().isoformat()
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT id, title, project, status, priority, due_date
        FROM tasks
        WHERE due_date = ? AND status != 'done'
        ORDER BY CASE priority WHEN 'urgent' THEN 1 WHEN 'high' THEN 2 WHEN 'normal' THEN 3 ELSE 4 END
    """, (today,)).fetchall()
    conn.close()
    tasks = [{"id": r[0], "title": r[1], "project": r[2], "status": r[3], "priority": r[4], "due_date": r[5]} for r in rows]
    return json.dumps(tasks, indent=2)