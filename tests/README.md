# Test directory for the Harmonica Tabs application

This directory contains unit and integration tests for the Flask application.

## Test Structure

- `conftest.py` - Pytest configuration and fixtures
- `test_app.py` - Application route and functionality tests
- `test_models.py` - Database model tests

## Running Tests

### Install test dependencies:
```bash
pip install pytest pytest-flask pytest-cov
```

### Run all tests:
```bash
pytest
```

### Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

### Run specific test file:
```bash
pytest tests/test_models.py
```

### Run with markers:
```bash
pytest -m unit          # Run only unit tests
pytest -m integration    # Run only integration tests
pytest -m "not slow"    # Skip slow tests
```

## Test Coverage

The test suite aims for >80% code coverage. Coverage reports are generated in:
- Terminal output (with --cov-report=term)
- HTML report (with --cov-report=html)

## Test Categories

### Unit Tests
- Model validation and relationships
- Form validation
- Individual route functionality

### Integration Tests
- Full user workflows
- Database operations
- Authentication flows

## Fixtures

Key test fixtures available:
- `app` - Flask application instance
- `client` - Test client for requests
- `runner` - CLI test runner
- `sample_user` - Test user instance
- `sample_tab` - Test tab instance

## Best Practices

1. **Test one thing per test**: Each test should verify a single behavior
2. **Use descriptive names**: Test function names should clearly state what they test
3. **Arrange-Act-Assert**: Structure tests with setup, action, and verification
4. **Mock external services**: Don't test external APIs in unit tests
5. **Clean up**: Ensure tests don't interfere with each other
