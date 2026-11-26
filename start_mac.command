#!/bin/bash
# Starts your app on macOS. In a terminal in this folder, type:  bash start_mac.command
# (Double-clicking this file also works, unless macOS blocks it: see README.md, section 2.3.)
cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python is not installed. Install it from https://www.python.org/downloads/ and try again."
    read -r -p "Press Enter to close this window."
    exit 1
fi

# A private Python environment for this project, created the first time only
# (and again if the .venv folder was copied from another computer and does not work here).
if ! .venv/bin/python -c "import sys" >/dev/null 2>&1; then
    if [ -e .venv ]; then
        echo "The .venv folder does not work on this computer. Setting up Python again..."
    else
        echo "First start: setting up Python for this project..."
    fi
    python3 -m venv --clear .venv || { read -r -p "Could not create .venv. Press Enter to close."; exit 1; }
fi
if ! .venv/bin/python -c "import flask" >/dev/null 2>&1; then
    .venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt \
        || { read -r -p "Could not install Flask (are you online?). Press Enter to close."; exit 1; }
fi

.venv/bin/python app/app.py "$@"
