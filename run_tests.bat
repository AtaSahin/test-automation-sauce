@echo off
REM Batch script for running tests on Windows

echo ====================================
echo Sauce Demo Test Automation
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Select test suite to run:
echo 1. All Tests
echo 2. Smoke Tests
echo 3. Regression Tests
echo 4. Login Tests
echo 5. Inventory Tests
echo 6. Cart Tests
echo 7. Checkout Tests
echo 8. E2E Tests
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" (
    echo Running all tests...
    pytest -v
) else if "%choice%"=="2" (
    echo Running smoke tests...
    pytest -m smoke -v
) else if "%choice%"=="3" (
    echo Running regression tests...
    pytest -m regression -v
) else if "%choice%"=="4" (
    echo Running login tests...
    pytest tests/test_login.py -v
) else if "%choice%"=="5" (
    echo Running inventory tests...
    pytest tests/test_inventory.py -v
) else if "%choice%"=="6" (
    echo Running cart tests...
    pytest tests/test_cart.py -v
) else if "%choice%"=="7" (
    echo Running checkout tests...
    pytest tests/test_checkout.py -v
) else if "%choice%"=="8" (
    echo Running E2E tests...
    pytest tests/test_e2e.py -v
) else (
    echo Invalid choice! Running all tests...
    pytest -v
)

echo.
echo ====================================
echo Test execution completed!
echo ====================================
echo.
echo Generating Allure report...
allure serve allure-results

pause

