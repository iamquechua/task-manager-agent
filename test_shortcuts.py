# test_shortcuts.py
"""
Quick test script for the shortcut system
"""

from tools import init_db, add_task
from shortcuts import process_shortcut
import json

def setup_test_data():
    """Add some test tasks to the database"""
    init_db()

    # Add test tasks
    tasks = [
        ("Fix critical bug", "work", "urgent", "2026-02-09", "Production issue"),
        ("Buy milk", "grocery", "normal", None, ""),
        ("Buy eggs", "grocery", "normal", None, ""),
        ("Review PR", "work", "high", "2026-02-08", "Code review"),
        ("Deploy hotfix", "work", "urgent", "2026-02-08", "Emergency deploy"),
        ("Call client", "client-project", "urgent", None, "Urgent call"),
        ("Write report", "work", "normal", "2026-02-10", "Monthly report"),
    ]

    print("Setting up test data...")
    for title, project, priority, due_date, description in tasks:
        result = add_task(title, project, priority, due_date, description)
        data = json.loads(result)
        print(f"  ✓ Added: {title} [{data['task_id']}]")

    print("\nTest data setup complete!\n")


def test_fast_shortcuts():
    """Test fast shortcuts"""
    print("=" * 60)
    print("TESTING FAST SHORTCUTS")
    print("=" * 60)

    shortcuts_to_test = [
        "/projects",
        "/summary",
        "/urgent",
        "/today",
        "/help"
    ]

    for shortcut in shortcuts_to_test:
        print(f"\n{'='*60}")
        print(f"Testing: {shortcut}")
        print(f"{'='*60}")
        response, modified_input = process_shortcut(shortcut)
        if response:
            print(response)
        else:
            print(f"Modified input: {modified_input}")


def test_ai_shortcuts():
    """Test AI shortcut expansion"""
    print("\n" + "=" * 60)
    print("TESTING AI SHORTCUTS (expansion only)")
    print("=" * 60)

    shortcuts_to_test = [
        "/add Buy bread for grocery project",
        "/list work",
        "/done abc123ef",
        "/delete xyz789",
        "/search meeting",
    ]

    for shortcut in shortcuts_to_test:
        print(f"\nInput: {shortcut}")
        response, modified_input = process_shortcut(shortcut)
        if response:
            print(f"Direct response: {response}")
        else:
            print(f"Expanded to: {modified_input}")


def test_unknown_shortcuts():
    """Test unknown shortcuts"""
    print("\n" + "=" * 60)
    print("TESTING UNKNOWN SHORTCUTS")
    print("=" * 60)

    shortcuts_to_test = [
        "/unknown",
        "/invalid",
    ]

    for shortcut in shortcuts_to_test:
        print(f"\nInput: {shortcut}")
        response, modified_input = process_shortcut(shortcut)
        print(f"Response: {response}")


if __name__ == "__main__":
    print("\n🧪 SHORTCUT SYSTEM TEST SUITE\n")

    # Setup test data
    setup_test_data()

    # Run tests
    test_fast_shortcuts()
    test_ai_shortcuts()
    test_unknown_shortcuts()

    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 60)
    print("\nNote: AI shortcuts only show expansion (they need Azure AI to execute)")
    print("Run 'python main.py' to test AI shortcuts end-to-end\n")
