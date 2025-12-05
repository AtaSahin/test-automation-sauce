# Sauce Demo Test Automation Framework

Professional end-to-end test automation framework for [SauceDemo](https://www.saucedemo.com) e-commerce application built with Python, Selenium, and Pytest.

## Architecture

This framework follows industry best practices including:

- **Page Object Model (POM)** for maintainable test code
- **Explicit Waits** instead of hard-coded sleeps for reliability
- **Type Hinting** for better code quality and IDE support
- **Allure Reporting** for comprehensive test reports
- **Parallel Execution** support for faster test runs
- **CI/CD Integration** with Jenkins and GitHub Actions
- **Docker Support** for consistent test environments

## Project Structure

```
sauce-test-automation/
├── pages/                   # Page Object classes
│   ├── base_page.py        # Base class with common methods
│   ├── login_page.py       # Login page object
│   ├── inventory_page.py   # Product inventory page object
│   ├── cart_page.py        # Shopping cart page object
│   └── checkout_page.py    # Checkout process page object
├── tests/                   # Test suites
│   ├── test_login.py       # Authentication tests
│   ├── test_inventory.py   # Product catalog tests
│   ├── test_cart.py        # Shopping cart tests
│   ├── test_checkout.py    # Checkout flow tests
│   └── test_e2e.py         # End-to-end scenarios
├── utils/                   # Helper utilities
│   ├── helpers.py          # Common helper functions
│   ├── logger.py           # Test logging setup
│   └── test_data.py        # Test data management
├── .github/workflows/       # GitHub Actions CI/CD
├── config.py               # Configuration management
├── conftest.py             # Pytest fixtures
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
├── Jenkinsfile             # Jenkins pipeline
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker orchestration
└── README.md               # This file
```

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git
- Chrome/Firefox/Edge browser

## Installation

### Quick Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd sauce-test-automation
```

2. Create virtual environment:

```bash
python -m venv venv
```

3. Activate virtual environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create `.env` file from template:

```bash
cp env_template.txt .env
```

Edit `.env` with your preferred settings.

## Configuration

Configuration is managed through environment variables in `.env` file:

```env
BASE_URL=https://www.saucedemo.com
BROWSER=chrome
HEADLESS=false
TIMEOUT=10
SCREENSHOT_ON_FAILURE=true

STANDARD_USER=standard_user
LOCKED_OUT_USER=locked_out_user
PROBLEM_USER=problem_user
PERFORMANCE_GLITCH_USER=performance_glitch_user
PASSWORD=secret_sauce
```

## Running Tests

### Command Line

Run all tests:

```bash
pytest -v
```

Run specific test suite:

```bash
pytest tests/test_login.py -v
```

Run by marker:

```bash
pytest -m smoke -v
pytest -m regression -v
```

Run with parallel execution:

```bash
pytest -n 4 -v
```

### Using Scripts

**Windows:**

```bash
run_tests.bat
```

**Linux/Mac:**

```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Docker Execution

Build and run tests in Docker:

```bash
docker-compose up --build
```

Run specific service:

```bash
docker-compose run test-runner pytest -m smoke -v
```

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.smoke` - Critical functionality tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.login` - Authentication tests
- `@pytest.mark.cart` - Shopping cart tests
- `@pytest.mark.checkout` - Checkout flow tests

## Reporting

### Allure Reports

Generate and view Allure report:

```bash
allure serve allure-results
```

Generate report to directory:

```bash
allure generate allure-results -o allure-report --clean
```

### HTML Reports

HTML reports are automatically generated in `test-results/report.html`

## CI/CD Integration

### Jenkins

1. Install Jenkins plugins:

   - Allure Jenkins Plugin
   - Pipeline Plugin
   - Git Plugin

2. Create new Pipeline job

3. Configure SCM with repository URL

4. Set Pipeline script path to `Jenkinsfile`

5. Run with parameters:
   - Browser selection (chrome/firefox/edge)
   - Test suite selection
   - Headless mode toggle

### GitHub Actions

Workflow automatically triggers on:

- Push to main/develop branches
- Pull requests
- Daily scheduled runs (2 AM)
- Manual workflow dispatch

View results in Actions tab of GitHub repository.

## Framework Features

### Page Object Model

Each page is represented by a class with locators and methods:

```python
class LoginPage(BasePage):
    _USERNAME_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")

    def login(self, username: str, password: str) -> None:
        self.send_keys(self._USERNAME_INPUT, username)
        self.send_keys(self._PASSWORD_INPUT, password)
        self.click(self._LOGIN_BUTTON)
```

### Explicit Waits

All interactions use WebDriverWait for reliability:

```python
def click(self, locator: Tuple[str, str]) -> None:
    element = self.wait.until(
        EC.element_to_be_clickable(locator)
    )
    element.click()
```

### Type Hinting

Modern Python type annotations throughout:

```python
def find_element(self, locator: Tuple[str, str]) -> WebElement:
    return self.wait.until(
        EC.visibility_of_element_located(locator)
    )
```

### Fixtures

Reusable test fixtures in `conftest.py`:

```python
@pytest.fixture
def authenticated_user(login_page, inventory_page):
    login_page.navigate()
    login_page.login_with_user_type("standard")
    return inventory_page
```

## Best Practices Applied

1. **No Hard-Coded Waits** - All waits are explicit and condition-based
2. **DRY Principle** - Reusable components reduce duplication
3. **Single Responsibility** - Each class/method has one clear purpose
4. **Configuration Management** - Environment-specific settings externalized
5. **Comprehensive Logging** - All actions logged for debugging
6. **Screenshot on Failure** - Automatic visual evidence of failures
7. **Descriptive Naming** - Clear, self-documenting code
8. **Docstrings** - Professional documentation for all public methods

## Test Coverage

### Core Functionality (46 tests)

- **Login Tests** (8) - Valid/invalid credentials, locked users, form validation
- **Inventory Tests** (11) - Product display, sorting, cart operations
- **Cart Tests** (11) - Add/remove items, price calculations, navigation
- **Checkout Tests** (9) - Form validation, price verification, order completion
- **E2E Tests** (6) - Complete user journeys from login to purchase

### Advanced Scenarios (19 tests)

- **Advanced Tests** (11) - Complex business logic, price calculations, data integrity
- **Performance Tests** (4) - Response time validation, load testing
- **Complex Workflows** (5) - Multi-step user journeys, comparison shopping

**Total: 65 Professional Test Cases**

## Troubleshooting

### WebDriver Issues

If webdriver-manager fails, manually install driver:

```bash
pip install webdriver-manager --upgrade
```

### Allure Not Found

Install Allure command-line tool:

**Windows (Scoop):**

```bash
scoop install allure
```

**Mac (Homebrew):**

```bash
brew install allure
```

**Linux:**

```bash
wget https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz
tar -zxvf allure-2.24.0.tgz -C /opt/
ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure
```

### Python Version Issues

Ensure Python 3.11+ is installed:

```bash
python --version
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is created for educational and portfolio purposes.

## Author

Created as a professional portfolio project demonstrating senior-level test automation expertise.

## Contact

For questions or collaboration opportunities, please reach out through GitHub.

---

**Note:** This framework showcases professional software testing practices suitable for enterprise environments.
