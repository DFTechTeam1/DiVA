#!/bin/sh

# Check if Poetry is installed
if ! command -v poetry &>/dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "Poetry installed"

    echo "Exporting poetry PATH"
    export PATH="/home/dfactory/.local/bin:$PATH"
else
    echo "Poetry is already installed."
fi


# Check poetry version
poetry --version

# Configure virtual environment location and install dependencies
echo "Configuring virtual environment location and installing dependencies..."
poetry config virtualenvs.in-project true
poetry install --no-root

echo "Setup complete."
