# Task Manager Shortcuts

The task manager now supports a **hybrid shortcut system** for faster task management!

## How It Works

The system has two types of shortcuts:

1. **Fast Shortcuts** - Execute instantly without AI processing
2. **AI-Enhanced Shortcuts** - Expand to natural language and leverage AI context

---

## Fast Shortcuts ⚡

These execute immediately without calling the AI agent:

### `/projects`
Lists all your projects with task counts and completion progress bars.

```
You: /projects

📁 Your Projects:

grocery: 2/5 tasks [████░░░░░░░░░░░░░░░░] 40%
work: 5/10 tasks [██████████░░░░░░░░░░] 50%
```

### `/summary`
Shows a comprehensive dashboard of all tasks grouped by project and status.

```
You: /summary

📊 Task Summary:

grocery (5 tasks):
  ⏳ todo: 2
  ✅ done: 2
  🔄 in_progress: 1

work (10 tasks):
  ⏳ todo: 4
  ✅ done: 5
  🚫 blocked: 1
```

### `/urgent`
Lists all tasks with urgent priority across all projects.

```
You: /urgent

Found 3 task(s):

🔴 ⏳ [abc123ef] Fix critical bug (work)
🔴 🔄 [def456gh] Deploy hotfix (work) | Due: 2026-02-09
🔴 ⏳ [ghi789jk] Call client (client-project)
```

### `/today`
Shows all incomplete tasks due today.

```
You: /today

Found 2 task(s):

🟠 🔄 [jkl012mn] Submit report (work) | Due: 2026-02-08
🟢 ⏳ [mno345pq] Buy groceries (personal) | Due: 2026-02-08
```

### `/help`
Displays all available shortcuts and usage examples.

---

## AI-Enhanced Shortcuts 🧠

These shortcuts expand to natural language and use the AI agent for intelligent parsing:

### `/add <text>`
Quick add a task. The AI intelligently parses project name, priority, and description.

**Examples:**
```
You: /add Buy milk for grocery project urgent
→ Expands to: "Add a new task: Buy milk for grocery project urgent.
               Parse the project name, priority, and description intelligently."

You: /add Review PR for work project high priority due tomorrow
→ AI understands project=work, priority=high, and can set due date
```

### `/list <project>`
List all tasks in a specific project.

**Examples:**
```
You: /list grocery
→ Expands to: "List all tasks in the 'grocery' project"

You: /list
→ Expands to: "List all tasks across all projects"
```

### `/done <task_id>`
Mark a task as completed.

**Examples:**
```
You: /done abc123ef
→ Expands to: "Mark task abc123ef as done"
```

### `/delete <task_id>`
Delete a task permanently.

**Examples:**
```
You: /delete abc123ef
→ Expands to: "Delete task abc123ef"
```

### `/search <query>`
Search for tasks by text in title or description.

**Examples:**
```
You: /search meeting
→ Expands to: "Search for tasks containing: meeting"

You: /search urgent client
→ Finds tasks with "urgent" or "client" in title/description
```

---

## Natural Language

You can still use natural language for anything else! The AI agent will understand:

```
You: Show me all blocked tasks in the work project
You: Change the priority of task abc123ef to high
You: What's my progress on the grocery project?
You: Move all done tasks from grocery project to archived status
```

---

## Priority & Status Indicators

### Priority Emojis
- 🔴 Urgent
- 🟠 High
- 🟢 Normal
- 🔵 Low

### Status Emojis
- ⏳ To Do
- 🔄 In Progress
- ✅ Done
- 🚫 Blocked

---

## Tips

1. **Fast shortcuts are instant** - Use them when you want immediate results without AI processing
2. **AI shortcuts are context-aware** - They maintain conversation history
3. **Mix and match** - Use `/projects` to see what you have, then `/list <project>` to drill down
4. **Copy task IDs** - The cyan IDs in brackets can be copy-pasted for `/done` or `/delete`
5. **Type `/help` anytime** - Get a quick reference without leaving the app

---

## Examples Workflow

```bash
# Check what projects you have
You: /projects

# View today's urgent tasks
You: /today

# Add a quick task
You: /add Review document for client project high priority

# List all tasks in a project
You: /list client

# Mark a task done
You: /done abc123ef

# Search for something
You: /search meeting

# Get overall summary
You: /summary
```

---

## Technical Details

- **Fast shortcuts** directly call Python functions (0 API calls)
- **AI shortcuts** expand prompts and use Azure AI Agents (1 API call)
- **Color coding** uses ANSI terminal colors for better readability
- **Error handling** provides helpful messages for incorrect usage

Enjoy your productivity boost! 🚀
