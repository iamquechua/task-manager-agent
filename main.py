# main.py
import os
from dotenv import load_dotenv
from typing import Any, Callable, Set

load_dotenv()  # Load .env file

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FunctionTool, ToolSet, MessageTextContent

from tools import (
    add_task, list_tasks, update_task, get_summary, init_db,
    get_projects, delete_task, search_tasks, get_tasks_due_today
)
from shortcuts import process_shortcut


def main():
    # Initialize database
    init_db()

    # Create Azure AI Project Client
    project_client = AIProjectClient(
        credential=DefaultAzureCredential(),
        endpoint=os.environ["PROJECT_ENDPOINT"],
    )

    # Collect user functions to be used as tools
    user_functions: Set[Callable[..., Any]] = {
        add_task, list_tasks, update_task, get_summary,
        get_projects, delete_task, search_tasks, get_tasks_due_today
    }

    # Create toolset with custom functions
    functions = FunctionTool(user_functions)
    toolset = ToolSet()
    toolset.add(functions)
    project_client.agents.enable_auto_function_calls(toolset)

    # Create the Azure AI Agent with specified configurations
    agent = project_client.agents.create_agent(
        model="gpt-4o-mini",
        name="task-manager-agent",
        instructions="You are a helpful task management assistant. You can add, list, update tasks, and provide summaries across projects. Be concise and helpful.",
        toolset=toolset,
    )
    print(f"Created agent, agent ID: {agent.id}")

    # Create a thread for the conversation
    thread = project_client.agents.threads.create()
    print(f"Created thread, thread ID: {thread.id}")
    print("🗂️  Task Manager Agent Ready. Type 'quit' to exit.")
    print("💡 Tip: Type '/help' to see available shortcuts!\n")

    try:
        # Interactive loop
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "quit":
                break

            # Process shortcuts
            fast_response, modified_input = process_shortcut(user_input)

            # If it's a fast shortcut, display result directly
            if fast_response is not None:
                print(f"{fast_response}")
                continue

            # Use modified input (either expanded AI shortcut or original input)
            # Create a message in the thread
            project_client.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=modified_input,
            )

            # Run the agent on the thread
            run = project_client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent.id
            )

            if run.status == "failed":
                print(f"Run failed: {run.last_error}")
                continue

            # Get the latest messages from the thread
            messages = list(project_client.agents.messages.list(thread_id=thread.id))
            # The most recent message is first (index 0)
            # Access the text content properly from MessageTextContent
            message_content = messages[0].content[0]
            if isinstance(message_content, MessageTextContent):
                agent_response = message_content.text.value
            else:
                agent_response = str(message_content)
            print(f"\nAgent: {agent_response}\n")

    finally:
        # Delete the agent when done
        project_client.agents.delete_agent(agent.id)
        print("Deleted agent")


if __name__ == "__main__":
    main()