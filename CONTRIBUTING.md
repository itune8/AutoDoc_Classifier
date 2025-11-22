# AutoDoc Classifier - Contributing Guidelines

Thank you for considering contributing to AutoDoc Classifier!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/AutoDoc_Classifier.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements-dev.txt`

## Code Style

- Follow PEP 8 guidelines
- Use `black` for code formatting: `black app/`
- Run `flake8` for linting: `flake8 app/`
- Sort imports with `isort`: `isort app/`

## Testing

- Write tests for new features
- Run tests: `pytest tests/`
- Check coverage: `pytest --cov=app tests/`
- Aim for >80% code coverage

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Add tests
4. Run the test suite
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## Commit Messages

Follow conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` adding tests
- `refactor:` code refactoring

Example: `feat: add batch processing support`

## Code of Conduct

Be respectful and inclusive. We value diversity and welcome contributions from everyone.
