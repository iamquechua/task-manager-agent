from dataclasses import dataclass, field
from datetime import datetime 
from typing import Optional

@dataclass
class Task:
    id: str
    title: str
    project: str  # "AgriTech DB", "Afrinomad", "Senegal Startups", etc.
    status: str  # "todo", "in_progress", "done", "blocked"
    priority: str  # "urgent", "high", "normal", "low"
    due_date: Optional[datetime] = None
    description: str = ""
    tags: list = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    