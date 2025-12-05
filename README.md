# 🧪 SauceDemo Test Automation Framework

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/sauce-test-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/sauce-test-automation/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.x-green)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Test Coverage](https://img.shields.io/badge/tests-125%2B-success)](tests/)

> **Professional end-to-end test automation framework** for [SauceDemo](https://www.saucedemo.com) e-commerce application, demonstrating advanced QA automation skills including accessibility testing, security validation, state management, and CI/CD integration.

---

## 📊 Test Execution Report

![Allure Report Overview](docs/images/allure-report-overview.png)
*Example test execution report with detailed metrics, trends, and failure analysis*

---

## ✨ Key Features

### 🏗️ **Architecture & Design Patterns**
- ✅ **Page Object Model (POM)** - Maintainable and scalable test structure
- ✅ **Explicit Waits** - Reliable synchronization without hard-coded sleeps
- ✅ **Type Hinting** - Enhanced code quality and IDE support
- ✅ **Fixture-based Setup** - Efficient resource management with pytest

### 🧪 **Comprehensive Test Coverage (125+ Tests)**
- ✅ **User Type Testing** - All 6 user personas (standard, locked, problem, performance, error, visual)
- ✅ **Accessibility Testing** - WCAG compliance, keyboard navigation, screen reader support
- ✅ **Security Testing** - SQL injection, XSS prevention, session management
- ✅ **State Management** - Cart persistence, browser navigation, multi-tab behavior
- ✅ **UI/UX Validation** - Responsive design, mobile/tablet viewports
- ✅ **Data Integrity** - Price calculations, tax validation, cart totals

### 📈 **Reporting & Monitoring**
- ✅ **Allure Reports** - Rich, interactive HTML reports with screenshots
- ✅ **Real-time Logging** - Detailed execution logs with timestamps
- ✅ **Failure Screenshots** - Automatic capture on test failures
- ✅ **Test Metrics** - Execution time, pass/fail rates, trends

### 🚀 **CI/CD & DevOps**
- ✅ **GitHub Actions** - Automated testing on every push
- ✅ **Docker Support** - Containerized test execution
- ✅ **Parallel Execution** - Faster test runs with pytest-xdist
- ✅ **Scheduled Runs** - Daily automated test execution

---

## 📁 Project Structure

```
sauce-test-automation/
├── .github/
│   └── workflows/
│       └── tests.yml           # GitHub Actions CI/CD pipeline
├── pages/                       # Page Object Model classes
│   ├── base_page.py            # Base class with reusable methods
│   ├── login_page.py           # Login page interactions
│   ├── inventory_page.py       # Product catalog operations
│   ├── cart_page.py            # Shopping cart management
│   └── checkout_page.py        # Checkout flow handling
├── tests/                       # Test suites organized by feature
│   ├── test_login.py           # Authentication & authorization
│   ├── test_inventory.py       # Product browsing & filtering
│   ├── test_cart.py            # Cart operations
│   ├── test_checkout.py        # Purchase flow
│   ├── test_e2e.py             # End-to-end scenarios
│   ├── test_advanced.py        # Complex business logic
│   ├── test_performance.py     # Performance benchmarks
│   ├── test_user_types.py      # User persona testing ⭐ NEW
│   ├── test_accessibility_ui.py # Accessibility & UI/UX ⭐ NEW
│   ├── test_security_validation.py # Security testing ⭐ NEW
│   └── test_state_browser.py   # State & browser behavior ⭐ NEW
├── config.py                    # Centralized configuration
├── conftest.py                  # Pytest fixtures & hooks
├── pytest.ini                   # Pytest configuration
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Multi-container orchestration
└── README.md                    # This file
```

---

## 🚀 Quick Start

### **Option 1: Local Setup**

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/sauce-test-automation.git
cd sauce-test-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Generate Allure report
allure serve allure-results
```

### **Option 2: Docker (Recommended for CI/CD)**

```bash
# Build Docker image
docker build -t saucedemo-tests .

# Run tests in container
docker run --rm saucedemo-tests

# Or use Docker Compose for full setup
docker-compose up

# View Allure report at http://localhost:5050
```

---

## 🧪 Running Tests

### **By Test Category**

```bash
# Smoke tests (critical functionality)
pytest tests/ -m smoke -v

# Regression suite (all tests)
pytest tests/ -m regression -v

# Security tests
pytest tests/test_security_validation.py -v

# Accessibility tests
pytest tests/test_accessibility_ui.py -v

# User type tests
pytest tests/test_user_types.py -v

# State management tests
pytest tests/test_state_browser.py -v
```

### **By User Type**

```bash
# Test with specific user
pytest tests/ -v --user-type=standard
pytest tests/ -v --user-type=problem
pytest tests/ -v --user-type=performance_glitch
```

### **Parallel Execution**

```bash
# Run tests in parallel (4 workers)
pytest tests/ -n 4 -v
```

### **With Allure Reporting**

```bash
# Run tests and generate Allure report
pytest tests/ -v --alluredir=allure-results
allure serve allure-results
```

---

## 📊 Test Categories & Coverage

| Category | Tests | Description |
|----------|-------|-------------|
| **Authentication** | 12 | Login, logout, session management |
| **Product Catalog** | 15 | Browsing, filtering, sorting |
| **Shopping Cart** | 18 | Add/remove items, cart persistence |
| **Checkout** | 20 | Purchase flow, form validation |
| **User Types** | 16 | All 6 user personas |
| **Accessibility** | 18 | WCAG, keyboard navigation, responsive |
| **Security** | 18 | SQL injection, XSS, session security |
| **State Management** | 15 | Cart persistence, browser navigation |
| **Performance** | 8 | Load times, response benchmarks |
| **E2E Scenarios** | 10 | Complete user journeys |

**Total: 125+ comprehensive test cases**

---

## 🔧 Configuration

### **Environment Variables**

Create a `.env` file in the project root:

```env
# Application
BASE_URL=https://www.saucedemo.com

# Browser Settings
BROWSER=chrome
HEADLESS=false
TIMEOUT=10

# Test Users
STANDARD_USER=standard_user
LOCKED_OUT_USER=locked_out_user
PROBLEM_USER=problem_user
PERFORMANCE_GLITCH_USER=performance_glitch_user
ERROR_USER=error_user
VISUAL_USER=visual_user
PASSWORD=secret_sauce

# Reporting
SCREENSHOT_ON_FAILURE=true
ALLURE_RESULTS_DIR=allure-results
```

### **Browser Configuration**

Supported browsers:
- ✅ Chrome (default)
- ✅ Firefox
- ✅ Edge
- ✅ Safari (macOS only)

---

## 📈 CI/CD Pipeline

### **GitHub Actions Workflow**

The project includes a comprehensive CI/CD pipeline that:

1. **Runs on every push** to main/master branches
2. **Tests multiple Python versions** (3.11, 3.12)
3. **Executes smoke tests** first for fast feedback
4. **Runs full regression suite** for comprehensive coverage
5. **Generates Allure reports** automatically
6. **Deploys reports to GitHub Pages** for easy access
7. **Runs daily scheduled tests** at 2 AM UTC

**View live test results:** `https://YOUR_USERNAME.github.io/sauce-test-automation/`

### **Pipeline Status**

![CI/CD Pipeline](https://github.com/YOUR_USERNAME/sauce-test-automation/actions/workflows/tests.yml/badge.svg)

---

## 🐳 Docker Support

### **Why Docker?**

- ✅ **Consistent Environment** - Same setup across all machines
- ✅ **No Local Dependencies** - Chrome, ChromeDriver included
- ✅ **CI/CD Ready** - Perfect for automated pipelines
- ✅ **Isolated Execution** - No conflicts with local setup

### **Docker Commands**

```bash
# Build image
docker build -t saucedemo-tests .

# Run all tests
docker run --rm saucedemo-tests

# Run specific test suite
docker run --rm saucedemo-tests pytest tests/test_login.py -v

# Run with custom environment
docker run --rm -e HEADLESS=true -e BROWSER=chrome saucedemo-tests

# Mount local directory for live results
docker run --rm -v $(pwd)/allure-results:/app/allure-results saucedemo-tests
```

### **Docker Compose**

```bash
# Start all services (tests + Allure server)
docker-compose up

# Run tests only
docker-compose up test-runner

# View Allure report
# Open browser: http://localhost:5050

# Clean up
docker-compose down
```

---

## 📸 Test Reports

### **Allure Report Features**

- 📊 **Overview Dashboard** - Test execution summary with graphs
- 📈 **Trends** - Historical test results and stability metrics
- 🔍 **Detailed Steps** - Step-by-step test execution with screenshots
- 🐛 **Failure Analysis** - Categorized failures with stack traces
- ⏱️ **Timeline** - Execution timeline for performance analysis
- 📦 **Test Suites** - Organized by features and stories

### **Sample Report**

![Allure Report](docs/images/allure-report-overview.png)

---

## 🎯 Advanced Features

### **1. Parametrized Testing**

```python
@pytest.mark.parametrize("user_type", ["standard", "problem", "performance_glitch"])
def test_all_users_can_login(user_type):
    # Test runs 3 times with different users
    pass
```

### **2. Custom Markers**

```python
@pytest.mark.smoke
@pytest.mark.critical
def test_login():
    pass
```

### **3. Automatic Screenshots on Failure**

```python
# Configured in conftest.py
# Screenshots automatically attached to Allure reports
```

### **4. Browser Console Error Detection**

```python
# Checks for JavaScript errors in browser console
logs = driver.get_log('browser')
severe_errors = [log for log in logs if log['level'] == 'SEVERE']
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Best Practices Implemented

- ✅ **DRY Principle** - No code duplication
- ✅ **SOLID Principles** - Clean, maintainable code
- ✅ **Explicit Waits** - No `time.sleep()` calls
- ✅ **Page Object Model** - Separation of concerns
- ✅ **Type Hints** - Better code documentation
- ✅ **Comprehensive Logging** - Detailed execution logs
- ✅ **Error Handling** - Graceful failure management
- ✅ **Test Independence** - Tests can run in any order
- ✅ **Data-Driven Testing** - External test data management

---

## 🏆 Skills Demonstrated

This project showcases expertise in:

- ✅ **Test Automation** - Selenium WebDriver, Pytest
- ✅ **Page Object Model** - Design patterns
- ✅ **CI/CD** - GitHub Actions, Docker
- ✅ **Accessibility Testing** - WCAG compliance
- ✅ **Security Testing** - SQL injection, XSS prevention
- ✅ **Performance Testing** - Load time benchmarks
- ✅ **API Testing** - REST API validation (if applicable)
- ✅ **DevOps** - Docker, containerization
- ✅ **Reporting** - Allure, HTML reports
- ✅ **Version Control** - Git, GitHub

---

## 📞 Contact

**Your Name**  
📧 Email: your.email@example.com  
💼 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)  
🐙 GitHub: [github.com/yourusername](https://github.com/yourusername)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [SauceDemo](https://www.saucedemo.com) - Test application
- [Selenium](https://www.selenium.dev/) - Browser automation
- [Pytest](https://pytest.org/) - Testing framework
- [Allure](https://docs.qameta.io/allure/) - Reporting framework

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

Made with ❤️ by a passionate QA Engineer

</div>
