#!/bin/sh

show_help() {
  echo "Usage: $0 [--unit_test | --api_test | --help]"
  echo ""
  echo "Options:"
  echo "  --unit_test    Run unit tests located in tests/unit_test"
  echo "  --api_test     Run API tests located in tests/api_test"
  echo "  --help         Show this help message"
}

if [ "$1" = "--help" ]; then
  show_help
  exit 0
elif [ "$1" = "--unit_test" ]; then
  TEST_DIR="tests/unit_test"
elif [ "$1" = "--api_test" ]; then
  TEST_DIR="tests/api_test"
else
  echo "Invalid option: $1"
  show_help
  exit 1
fi

sh ./scripts/venv.sh

echo "Running tests in $TEST_DIR"
if ! coverage run -m --source=$TEST_DIR pytest $TEST_DIR --verbose; then
  echo "Tests failed!"
  exit 1
fi

echo "Generating coverage report"
coverage report -m --skip-empty
coverage html

echo "Test finished"
