#!/bin/bash

echo "===================================="
echo "Sauce Demo Test Automation"
echo "===================================="
echo ""

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Select test suite to run:"
echo "1. All Tests"
echo "2. Smoke Tests"
echo "3. Regression Tests"
echo "4. Login Tests"
echo "5. Inventory Tests"
echo "6. Cart Tests"
echo "7. Checkout Tests"
echo "8. E2E Tests"
echo ""

read -p "Enter your choice (1-8): " choice

case $choice in
    1)
        echo "Running all tests..."
        pytest -v
        ;;
    2)
        echo "Running smoke tests..."
        pytest -m smoke -v
        ;;
    3)
        echo "Running regression tests..."
        pytest -m regression -v
        ;;
    4)
        echo "Running login tests..."
        pytest tests/test_login.py -v
        ;;
    5)
        echo "Running inventory tests..."
        pytest tests/test_inventory.py -v
        ;;
    6)
        echo "Running cart tests..."
        pytest tests/test_cart.py -v
        ;;
    7)
        echo "Running checkout tests..."
        pytest tests/test_checkout.py -v
        ;;
    8)
        echo "Running E2E tests..."
        pytest tests/test_e2e.py -v
        ;;
    *)
        echo "Invalid choice! Running all tests..."
        pytest -v
        ;;
esac

echo ""
echo "===================================="
echo "Test execution completed!"
echo "===================================="
echo ""
echo "Generating Allure report..."
allure serve allure-results

