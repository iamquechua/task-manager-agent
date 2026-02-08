# Task Manager Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

An interactive AI-powered task management system built with Azure AI Agents. This application allows you to manage tasks across multiple projects using natural language commands through an intelligent conversational agent.

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/iamquechua/task-manager-agent.git
cd task-manager-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your PROJECT_ENDPOINT

# 4. Authenticate with Azure
az login

# 5. Run the application
python main.py
```

Then try: `Add a task "Review documentation" to my project with high priority`

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Commands](#available-commands)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Natural Language Interface**: Interact with your task manager using conversational language
- **Persistent Conversation**: Maintains context throughout your session
- **Multi-Project Support**: Organize tasks across different projects
- **Priority Management**: Set and update task priorities (urgent, high, normal, low)
- **Status Tracking**: Track task status (todo, in_progress, done, blocked)
- **Due Date Management**: Set and track task deadlines
- **Task Summaries**: Get dashboard-style summaries across all projects
- **SQLite Database**: Local persistent storage for all your tasks

## Architecture

The system uses:
- **Azure AI Agents**: Provides intelligent conversation and tool orchestration
- **Function Tools**: Automatically converts Python functions into callable tools for the agent
- **Persistent Thread**: Maintains conversation context across multiple interactions
- **SQLite Database**: Stores task data locally in `tasks.db`

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.8+** installed
2. **Azure Account** with:
   - An Azure AI Project created
   - Proper permissions configured
3. **Azure CLI** installed and authenticated
4. **Required Python packages** (see Installation)

## Installation

### 1. Clone or navigate to the project directory

```bash
cd /path/to/task-manager-agent
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install required packages

```bash
pip install azure-ai-projects azure-identity python-dotenv requests
```

### 4. Set up Azure Authentication

```bash
az login
```

This configures `DefaultAzureCredential` to authenticate with Azure.

## Configuration

### 1. Create a `.env` file in the project root:

```bash
touch .env
```

### 2. Add your Azure AI Project endpoint:

```env
# Required: Your Azure AI Project Endpoint
PROJECT_ENDPOINT=https://your-project-name.your-region.api.azureml.ms

# Optional: For weather functionality (if using agent.py separately)
WEATHER_API_KEY=your_weather_api_key
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
```

### 3. Get your PROJECT_ENDPOINT:

- Go to [Azure AI Studio](https://ai.azure.com)
- Select your project
- Navigate to "Settings" or "Overview"
- Copy the "Project Endpoint" URL

## Usage

### Starting the Application

Run the main script:

```bash
python main.py
```

You should see:

```
Created agent, agent ID: asst_xxxxxxxxxxxxx
Created thread, thread ID: thread_xxxxxxxxxxxxx
🗂️  Task Manager Agent Ready. Type 'quit' to exit.

You:
```

### Example Interactions

#### Adding Tasks

```
You: Add a task "Implement user authentication" to the AgriTech DB project with high priority

Agent: I've added the task "Implement user authentication" to the AgriTech DB project with high priority. The task ID is abc12345.
```

#### Listing Tasks

```
You: Show me all tasks for AgriTech DB

Agent: Here are the tasks for AgriTech DB:
1. [abc12345] Implement user authentication - Status: todo, Priority: high
2. [def67890] Set up database schema - Status: in_progress, Priority: normal
```

#### Updating Tasks

```
You: Mark task abc12345 as in progress

Agent: I've updated task abc12345 to in_progress status.
```

#### Getting Summaries

```
You: Give me a summary of all my tasks

Agent: Here's your task summary:
AgriTech DB: 3 todo, 2 in_progress, 5 done
Afrinomad: 1 todo, 1 done
Senegal Startups: 2 todo, 3 done
```

#### Context-Aware Conversations

```
You: Add a task "Write API documentation" to AgriTech DB

Agent: I've added the task "Write API documentation" to AgriTech DB.

You: Make it urgent

Agent: I've updated the task to urgent priority.
```

### Exiting the Application

Type `quit` to exit:

```
You: quit
Deleted agent
```

The agent is automatically cleaned up when you exit.

## Available Commands

The agent understands natural language, but here are the core functions it can perform:

### add_task
Add a new task to a project.

**Parameters:**
- `title` (required): Task title
- `project` (required): Project name
- `priority` (optional): urgent, high, normal, low (default: normal)
- `due_date` (optional): Date in YYYY-MM-DD format
- `description` (optional): Task description

**Example:** "Add a task 'Fix login bug' to AgriTech DB with urgent priority, due on 2026-02-15"

### list_tasks
List tasks with optional filtering.

**Parameters:**
- `project` (optional): Filter by project name
- `status` (optional): Filter by status (todo, in_progress, done, blocked)

**Examples:**
- "Show all tasks"
- "List tasks for AgriTech DB"
- "Show me all in_progress tasks"

### update_task
Update a task's status or priority.

**Parameters:**
- `task_id` (required): The task ID (shown when listing tasks)
- `status` (optional): New status (todo, in_progress, done, blocked)
- `priority` (optional): New priority (urgent, high, normal, low)

**Examples:**
- "Mark task abc12345 as done"
- "Change task abc12345 priority to urgent"

### get_summary
Get a summary of all tasks across projects.

**No parameters required.**

**Example:** "Give me a summary" or "Show dashboard"

## Project Structure

```
task-manager-agent/
├── main.py           # Main interactive application (USE THIS)
├── agent.py          # Alternative single-agent setup (legacy)
├── tools.py          # Task management functions and database operations
├── tasks.db          # SQLite database (created automatically)
├── .env              # Environment configuration (create this)
└── README.md         # This file
```

### File Descriptions

#### main.py
The primary application file. Contains:
- Interactive loop for continuous conversation
- Azure AI Agent initialization with persistent thread
- Proper cleanup on exit
- Error handling for failed runs

**Key Features:**
- Creates agent and thread once at startup
- Maintains conversation context throughout session
- Uses `FunctionTool` for automatic tool schema generation
- Properly handles `MessageTextContent` types

#### tools.py
Contains all task management functions:
- `init_db()`: Initialize SQLite database
- `add_task()`: Create new tasks
- `list_tasks()`: Query and filter tasks
- `update_task()`: Modify existing tasks
- `get_summary()`: Generate task summaries

#### agent.py
Legacy file with manual tool definitions. Not needed for main.py functionality, but kept for reference or alternative usage patterns.

## Troubleshooting

### Common Issues

#### 1. Authentication Errors

**Error:** `DefaultAzureCredential failed to retrieve a token`

**Solution:**
```bash
az login
az account show  # Verify you're logged in
```

#### 2. Missing PROJECT_ENDPOINT

**Error:** `KeyError: 'PROJECT_ENDPOINT'`

**Solution:**
- Ensure `.env` file exists in the project root
- Verify `PROJECT_ENDPOINT` is set correctly
- Check the endpoint URL format (should start with `https://`)

#### 3. Agent Creation Fails

**Error:** `Failed to create agent` or rate limit errors

**Solution:**
- Check your Azure AI quota and limits
- Verify your project has the necessary model deployments
- Ensure you have proper permissions in the Azure AI Project

#### 4. Message Content Access Error

**Error:** `Cannot access attribute "text"`

**Solution:**
This has been fixed in the latest version by:
- Importing `MessageTextContent` type
- Using `isinstance()` check before accessing `.text.value`
- Fallback to string conversion if content type is unexpected

#### 5. Database Lock Errors

**Error:** `database is locked`

**Solution:**
- Ensure only one instance of the application is running
- Close the application properly using `quit` command
- If needed, delete `tasks.db` to start fresh (you'll lose data)

### Debugging Tips

1. **Enable Verbose Logging:**
   Add print statements to see what's happening:
   ```python
   print(f"[DEBUG] Run status: {run.status}")
   print(f"[DEBUG] Message count: {len(messages)}")
   ```

2. **Check Database Contents:**
   ```bash
   sqlite3 tasks.db "SELECT * FROM tasks;"
   ```

3. **Verify Azure Connection:**
   ```python
   # Test in Python REPL
   from azure.ai.projects import AIProjectClient
   from azure.identity import DefaultAzureCredential
   import os

   client = AIProjectClient(
       credential=DefaultAzureCredential(),
       endpoint=os.environ["PROJECT_ENDPOINT"]
   )
   print("Connection successful!")
   ```

## Technical Details

### Code Improvements Made

**Fixed Issues:**
1. **Line 56**: Removed unused `message` variable assignment
2. **Line 75-78**: Added proper type handling for `MessageTextContent` with isinstance check

**Implementation Pattern:**
```python
# Proper message content access
message_content = messages[0].content[0]
if isinstance(message_content, MessageTextContent):
    agent_response = message_content.text.value
else:
    agent_response = str(message_content)
```

### Why This Approach?

- **Persistent Thread**: All messages in one thread maintains conversation context
- **FunctionTool vs Manual Schemas**: `FunctionTool` automatically generates schemas from Python function signatures and docstrings
- **Auto Function Calls**: `enable_auto_function_calls()` allows the agent to automatically execute tools without manual handling
- **Try/Finally**: Ensures agent cleanup even if errors occur

### Security Considerations

1. **Credentials**: Never commit `.env` file to version control
2. **Database**: `tasks.db` contains your data - back it up regularly
3. **Azure Access**: Use least-privilege principles for Azure permissions
4. **API Keys**: Keep `WEATHER_API_KEY` and other sensitive data in `.env`

### Performance Notes

- First message may take longer (agent initialization)
- Subsequent messages use existing thread (faster)
- Database queries are optimized with indexes on priority
- Agent cleanup happens automatically on exit

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and test thoroughly
4. **Commit your changes** (`git commit -m 'Add amazing feature'`)
5. **Push to the branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

Please ensure:
- Code follows existing style conventions
- All tests pass (if applicable)
- Documentation is updated for new features
- Commit messages are clear and descriptive

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review [Azure AI Agents documentation](https://learn.microsoft.com/en-us/azure/ai-studio/)
3. Open an issue on GitHub
4. Verify your Azure AI Project configuration

## Acknowledgments

- Built with [Azure AI Agents](https://azure.microsoft.com/en-us/products/ai-services/)
- Inspired by modern task management needs

---

**Version:** 1.0.0
**Last Updated:** 2026-02-08
**Python Version:** 3.8+
**License:** MIT
