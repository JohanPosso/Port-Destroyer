# Contributing to PortDestroyer

First off, thank you for considering contributing to PortDestroyer! This project is made better by contributions from developers like you.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **System information** (OS, Python version)
- **Screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use case**: Why would this be useful?
- **Proposed solution**: How should it work?
- **Alternatives**: What other solutions have you considered?

### Pull Requests

1. **Fork** the repository at https://github.com/JohanPosso/port-destroyer
2. **Create a branch** from `main`
3. **Make your changes** with clear, descriptive commits
4. **Test** your changes thoroughly
5. **Update documentation** if needed
6. **Submit a pull request**

#### Pull Request Guidelines

- Follow the existing code style (PEP 8 for Python)
- Write clear commit messages
- Include tests for new features
- Update CHANGELOG.md
- Keep PRs focused on a single feature/fix

## Development Setup

```bash
# Clone your fork
git clone https://github.com/JohanPosso/port-destroyer.git
cd port-destroyer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x start_tray.sh port_destroyer.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable names

## Testing

Before submitting a PR, test on:
- [ ] macOS (if available)
- [ ] Linux (if available)
- [ ] Different Python versions (3.7+)

## Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add entries to CHANGELOG.md

## Commit Messages

Use clear, descriptive commit messages:

```
Add feature: Brief description

Detailed explanation of what changed and why.
```

Examples:
- `Add support for Windows platform`
- `Fix memory leak in process monitoring`
- `Update documentation for CLI usage`

## Project Structure

```
port-destroyer/
├── assets/           # Static resources (icons, etc)
├── port_destroyer.py # Core logic and CLI
├── port_destroyer_tray.py # System tray GUI
└── tests/           # Test files (when added)
```

## Questions?

Feel free to open an issue for questions or reach out to the maintainer.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Author**: Jesus Posso
**Contact**: Open an issue on GitHub


