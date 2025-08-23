#!/bin/bash

# create new screen
screen -dmS sunset bash -c "
    cd thesunset/detector && \
    source sunset/bin/activate && \
    python3 scheduler.py
"

# Optional: Check if screen session started
if screen -list | grep -q "sunset"; then
    echo "Sunset detector started in screen session 'sunset'"
    echo "To view: screen -r sunset"
    echo "To detach: Ctrl+A then D"
else
    echo "Failed to start screen session"
    exit 1
fi
