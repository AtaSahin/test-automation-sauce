# Quick Start Guide

This guide will help you get the test automation framework up and running in under 5 minutes.

## Prerequisites Check

Ensure you have these installed:

```bash
python --version
```

Expected output: Python 3.11 or higher

## Step-by-Step Setup

### 1. Clone and Navigate

```bash
git clone <your-repo-url>
cd sauce-test-automation
```

### 2. Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:

- Selenium for browser automation
- Pytest for test framework
- Allure for reporting
- WebDriver Manager for automatic driver management

### 4. Configure Environment

Create `.env` file:

```bash
copy env_template.txt .env
```

The default settings work out of the box:

- Browser: Chrome
- Headless: False (visible browser)
- Timeout: 10 seconds

### 5. Run Your First Test

Run smoke tests:

```bash
pytest -m smoke -v
```

Expected output: Tests start running in Chrome browser

### 6. View Test Report

Generate Allure report:

```bash
allure serve allure-results
```

Browser opens with interactive test report.

## Troubleshooting First Run

### Issue: Chrome driver not found

**Solution:** WebDriver Manager automatically downloads it. If fails:

```bash
pip install webdriver-manager --upgrade
```

### Issue: Tests fail to start

**Solution:** Check if port 4444 is free (used by Selenium):

```bash
netstat -ano | findstr :4444
```

### Issue: Import errors

**Solution:** Ensure virtual environment is activated:

```bash
which python
```

Should show path to venv directory.

## What's Next?

### Run Different Test Suites

All tests:

```bash
pytest -v
```

Specific feature:

```bash
pytest tests/test_login.py -v
```

Regression tests:

```bash
pytest -m regression -v
```

### Run Tests in Parallel

Faster execution with 4 workers:

```bash
pytest -n 4 -v
```

### Change Browser

Edit `.env` file:

```env
BROWSER=firefox
```

Or pass as environment variable:

```bash
BROWSER=edge pytest -v
```

### Headless Mode

For CI/CD or background execution:

```env
HEADLESS=true
```

## Visual Test Execution

Open another terminal and run:

```bash
pytest tests/test_e2e.py::TestE2E::test_complete_purchase_flow -v -s
```

Watch the automated shopping journey!

## Need Help?

- Check [README.md](README.md) for detailed documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for code guidelines
- Open an issue on GitHub for bugs

## Common Commands Cheat Sheet

```bash
pytest -v                          # All tests
pytest -m smoke -v                 # Smoke tests only
pytest -m regression -v            # Regression tests only
pytest tests/test_login.py -v      # Specific file
pytest -k "test_login" -v          # Tests matching pattern
pytest -n 4 -v                     # Parallel execution
pytest --lf -v                     # Run last failed
pytest --tb=short -v               # Short traceback
allure serve allure-results        # View report
```

## Verify Installation

Run this command to verify everything is working:

```bash
pytest tests/test_login.py::TestLogin::test_successful_login_standard_user -v
```

If this test passes, your setup is complete!

---

**Congratulations!** You're ready to run professional test automation. Happy testing!
