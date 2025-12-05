# Contributing Guidelines

Thank you for your interest in contributing to this project!

## Code Style

### Python Style Guide

This project follows PEP 8 with these key principles:

1. **Type Hints** - All function parameters and return types should be annotated
2. **Docstrings** - All public methods must have descriptive docstrings
3. **Naming Conventions**:
   - Classes: PascalCase (e.g., `LoginPage`)
   - Functions/Methods: snake_case (e.g., `login_with_credentials`)
   - Constants: UPPER_CASE (e.g., `TIMEOUT`)
   - Private attributes: \_leading_underscore (e.g., `_USERNAME_INPUT`)

### Example Code Structure

```python
from typing import Tuple
from selenium.webdriver.remote.webelement import WebElement

class ExamplePage(BasePage):
    """
    Brief description of page purpose.

    Detailed explanation of what this page handles,
    including any important context for maintainers.
    """

    _LOCATOR_NAME = (By.ID, "element-id")

    def method_name(self, param: str) -> bool:
        """
        Brief method description.

        Args:
            param: Description of parameter

        Returns:
            Description of return value

        Raises:
            ExceptionType: When this exception occurs
        """
        pass
```

## Adding New Tests

1. Create test file in `tests/` directory
2. Name file `test_<feature>.py`
3. Use descriptive test names: `test_<action>_<expected_result>`
4. Add appropriate markers (@pytest.mark.smoke, etc.)
5. Include Allure decorations for reporting

## Adding New Page Objects

1. Create page class in `pages/` directory
2. Inherit from `BasePage`
3. Define locators as class-level constants
4. Implement page-specific methods
5. Add comprehensive docstrings

## Pull Request Process

1. Update tests for any new functionality
2. Ensure all tests pass locally
3. Update documentation if needed
4. Submit PR with clear description
5. Link related issues

## Testing Your Changes

Before submitting PR, run:

```bash
pytest -v
pytest -m smoke
```

Ensure no new linter warnings:

```bash
pylint pages tests utils
```

## Questions?

Feel free to open an issue for discussion.
