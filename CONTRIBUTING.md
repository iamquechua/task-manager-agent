# Contributing to Task Manager Agent

Thank you for your interest in contributing to Task Manager Agent! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected behavior vs actual behavior
- Your environment (OS, Python version, Azure SDK version)
- Any relevant error messages or logs

### Suggesting Features

Feature suggestions are welcome! Please:
- Check if the feature has already been requested
- Clearly describe the feature and its use case
- Explain why this feature would be useful to most users

### Pull Requests

#### Before You Start

1. **Check existing issues** - Someone might already be working on it
2. **Create an issue first** - Discuss major changes before coding
3. **Fork the repository** - Work on your own copy

#### Development Process

1. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/task-manager-agent.git
   cd task-manager-agent
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Make your changes**
   - Follow existing code style and conventions
   - Add docstrings to new functions
   - Keep changes focused on a single issue
   - Test your changes thoroughly

5. **Test your changes**
   ```bash
   # Ensure the application runs
   python main.py

   # Test the specific functionality you changed
   # Add test cases if applicable
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

   Commit message prefixes:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements to existing features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template with:
     - Description of changes
     - Related issue number (if applicable)
     - Testing performed
     - Screenshots (if UI changes)

#### Pull Request Guidelines

- **Keep it focused** - One feature/fix per PR
- **Update documentation** - If you change functionality, update README.md
- **Add comments** - Explain complex logic
- **Follow style** - Match the existing code style
- **Test thoroughly** - Ensure nothing breaks

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add type hints where appropriate
- Keep functions focused and small
- Document complex logic with comments

Example:
```python
def add_task(title: str, project: str, priority: str = "normal",
             due_date: str = None, description: str = "") -> str:
    """
    Add a new task to a project.

    Args:
        title: Task title
        project: Project name
        priority: Task priority (urgent, high, normal, low)
        due_date: Due date in YYYY-MM-DD format
        description: Task description

    Returns:
        JSON string with task creation status
    """
    # Implementation
```

### Testing

- Test your changes with the Azure AI Agent
- Verify database operations work correctly
- Check error handling for edge cases
- Test with different input variations

### Documentation

When adding features:
- Update README.md with new functionality
- Add usage examples
- Update troubleshooting section if needed
- Document any new environment variables

## Project Structure

```
task-manager-agent/
├── main.py           # Main application - interactive loop
├── tools.py          # Task management functions
├── agent.py          # Alternative agent setup (legacy)
├── requirements.txt  # Python dependencies
├── .env.example      # Environment template
├── README.md         # User documentation
└── CONTRIBUTING.md   # This file
```

## Development Guidelines

### Adding New Tools/Functions

When adding new task management functions:

1. Add the function to `tools.py`
2. Include proper docstring
3. Add it to the `user_functions` set in `main.py`
4. Update README.md with usage examples
5. Test with the Azure AI Agent

### Database Changes

If modifying the database schema:
1. Update the `init_db()` function
2. Consider migration for existing databases
3. Document the schema changes
4. Test with fresh and existing databases

### Azure AI Integration

When modifying agent behavior:
- Test with Azure AI Project endpoint
- Verify tool calls work correctly
- Check error handling for API failures
- Ensure cleanup happens properly

## Questions or Need Help?

- Open an issue for questions
- Tag issues with appropriate labels
- Be patient - maintainers are volunteers

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Future CONTRIBUTORS.md file
- Release notes for significant contributions

Thank you for contributing to Task Manager Agent! 🎉
