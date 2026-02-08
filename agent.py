import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()  # Load .env file

project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ['PROJECT_ENDPOINT']
)

# Define tools the agent can use
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to a specific project",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "project": {"type": "string", "description": "Project name (e.g., AgriTech DB, Afrinomad, Senegal Startups, 54 Startups)"},
                    "priority": {"type": "string", "enum": ["urgent", "high", "normal", "low"]},
                    "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"},
                    "description": {"type": "string", "description": "Task description"}
                },
                "required": ["title", "project"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks filtered by project and/or status",
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {"type": "string"},
                    "status": {"type": "string", "enum": ["todo", "in_progress", "done", "blocked"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's status or priority",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["todo", "in_progress", "done", "blocked"]},
                    "priority": {"type": "string", "enum": ["urgent", "high", "normal", "low"]}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_summary",
            "description": "Get a dashboard summary of all tasks across projects",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]

# Create the agent
agent = project_client.agents.create_agent(
    model=os.environ['MODEL_DEPLOYMENT_NAME'],
    name="Task Manager",
    instructions="""You are Douno's personal task management assistant. You help manage tasks across multiple projects: AgriTech DB, Afrinomad, Senegal Startups, 54 Startups, and Azure AI Certification.
    
    When asked to add tasks, always confirm the project. When listing tasks, prioritize urgent items. Provide brief, actionable summaries. Communicate in English by default but can switch to French if asked.""",
    tools=tools
)