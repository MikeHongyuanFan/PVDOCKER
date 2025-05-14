#!/bin/bash

# Run tests with coverage and generate reports
# Usage: ./run_tests.sh [unit|integration|all]

set -e

# Default to running all tests
TEST_TYPE=${1:-all}

# Create directory for coverage reports
mkdir -p coverage_reports

echo "Running $TEST_TYPE tests with coverage..."

if [ "$TEST_TYPE" = "unit" ] || [ "$TEST_TYPE" = "all" ]; then
    echo "Running unit tests..."
    python -m pytest tests/unit/ --cov=. --cov-report=term --cov-report=html:coverage_reports/unit/ -v
    
    if [ "$TEST_TYPE" = "unit" ]; then
        echo "Unit test coverage report generated in coverage_reports/unit/"
    fi
fi

if [ "$TEST_TYPE" = "integration" ] || [ "$TEST_TYPE" = "all" ]; then
    echo "Running integration tests..."
    python -m pytest tests/integration/ --cov=. --cov-report=term --cov-report=html:coverage_reports/integration/ -v
    
    if [ "$TEST_TYPE" = "integration" ]; then
        echo "Integration test coverage report generated in coverage_reports/integration/"
    fi
fi

if [ "$TEST_TYPE" = "all" ]; then
    echo "Combining coverage reports..."
    coverage combine .coverage
    coverage report
    coverage html -d coverage_reports/combined/
    echo "Combined coverage report generated in coverage_reports/combined/"
fi

echo "Tests completed."
