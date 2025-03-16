# Contributing to Meeting Sidekick

Thank you for your interest in contributing to Meeting Sidekick! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

1. A clear, descriptive title
2. A detailed description of the issue
3. Steps to reproduce the bug
4. Expected behavior
5. Actual behavior
6. Screenshots (if applicable)
7. Environment information (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for enhancements! Please create an issue with:

1. A clear, descriptive title
2. A detailed description of the proposed enhancement
3. Any relevant examples or mockups
4. Why this enhancement would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Add or update tests as necessary
5. Ensure all tests pass
6. Update documentation as needed
7. Submit a pull request

#### Pull Request Guidelines

- Follow the existing code style
- Include tests for new features
- Update documentation for any changed functionality
- Keep pull requests focused on a single topic
- Reference any related issues in your pull request description

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/meeting-sidekick.git
   cd meeting-sidekick
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt  # (if available)
   ```

4. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

## Testing

Run tests with:
```bash
pytest
```

## Code Style

This project follows PEP 8 style guidelines. Please ensure your code adheres to these standards.

You can check your code style with:
```bash
flake8
```

## Documentation

Please update documentation when making changes:

- Update docstrings for any modified functions or classes
- Update README.md if necessary
- Update ARCHITECTURE.md for significant architectural changes

## Commit Messages

- Use clear, descriptive commit messages
- Start with a short summary line (50 chars or less)
- Optionally followed by a blank line and a more detailed explanation
- Reference issue numbers in the commit message when applicable

## Licensing

By contributing to Meeting Sidekick, you agree that your contributions will be licensed under the project's MIT license.

## Questions?

If you have any questions about contributing, please open an issue with your question. 