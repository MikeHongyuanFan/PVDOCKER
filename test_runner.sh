#!/bin/bash
# test_runner.sh - Run tests and generate coverage report

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to the Django project directory
cd backenddjango

# Function to run tests with coverage
run_tests() {
    local test_type=$1
    local test_path=$2
    local coverage_file=$3
    
    echo -e "\n${YELLOW}=======================================${NC}"
    echo -e "${YELLOW}Running $test_type tests with coverage...${NC}"
    echo -e "${YELLOW}=======================================${NC}"
    
    docker exec -it lianv3-501a294797023b7f3fa802ddb963f1a4b1577785-backend-1 coverage run --source='.' --data-file=$coverage_file manage.py test $test_path
    
    # Check if tests passed
    if [ $? -ne 0 ]; then
        echo -e "${RED}$test_type tests failed!${NC}"
        return 1
    fi
    
    echo -e "${GREEN}$test_type tests passed!${NC}"
    return 0
}

# Run integration tests
run_tests "integration" "tests.integration" ".coverage.integration"
integration_result=$?

# Run unit tests if they exist
if [ -d "tests/unit" ]; then
    run_tests "unit" "tests.unit" ".coverage.unit"
    unit_result=$?
else
    echo -e "\n${BLUE}No unit tests directory found. Skipping unit tests.${NC}"
    unit_result=0
fi

# Check if any tests failed
if [ $integration_result -ne 0 ] || [ $unit_result -ne 0 ]; then
    echo -e "\n${RED}Some tests failed. See above for details.${NC}"
    exit 1
fi

echo -e "\n${YELLOW}=======================================${NC}"
echo -e "${YELLOW}Combining coverage data...${NC}"
echo -e "${YELLOW}=======================================${NC}"

# Combine coverage data if both types of tests were run
if [ -d "tests/unit" ]; then
    docker exec -it lianv3-501a294797023b7f3fa802ddb963f1a4b1577785-backend-1 coverage combine .coverage.integration .coverage.unit
else
    docker exec -it lianv3-501a294797023b7f3fa802ddb963f1a4b1577785-backend-1 cp .coverage.integration .coverage
fi

echo -e "\n${YELLOW}=======================================${NC}"
echo -e "${YELLOW}Generating combined coverage report...${NC}"
echo -e "${YELLOW}=======================================${NC}"

# Generate coverage report
docker exec -it lianv3-501a294797023b7f3fa802ddb963f1a4b1577785-backend-1 coverage report

# Generate HTML coverage report
docker exec -it lianv3-501a294797023b7f3fa802ddb963f1a4b1577785-backend-1 coverage html

echo -e "\n${GREEN}Test coverage report generated in htmlcov/${NC}"
echo -e "${GREEN}To view the report, open backenddjango/htmlcov/index.html in your browser${NC}"

# Return to the original directory
cd ..

echo -e "\n${GREEN}All tests passed successfully!${NC}"
exit 0
