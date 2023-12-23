#!/bin/bash

# Log file path
LOG_FILE="/Users/andrew/Scripts/Notion-Integrations/refresh_log.log"

# Start logging
exec > >(/usr/bin/tee -a $LOG_FILE) 2>&1

echo "Starting script at $(/bin/date)"

# Start SSH agent and add key
eval "$(/usr/bin/ssh-agent -s)"
/usr/bin/ssh-add ~/.ssh/id_ed25519

# Configure Git
/usr/bin/git config --global user.name "4andrewahn"
/usr/bin/git config --global user.email "4andrewahn@gmail.com"

# Activate the virtual environment
source /Users/andrew/Scripts/Notion-Integrations/.venv/bin/activate

# Run your Python script to create new plot
/Users/andrew/Scripts/Notion-Integrations/.venv/bin/python /Users/andrew/Scripts/Notion-Integrations/application_graph_script.py

# Change working directory to project directory
cd /Users/andrew/Scripts/Notion-Integrations

# Add changes to new Git commit
/usr/bin/git add -A

# Add commit message
/usr/bin/git commit -m "updated bar-plot"

# Push changes to GitHub
/usr/bin/git push origin main

# Deactivate the virtual environment
source /Users/andrew/Scripts/Notion-Integrations/.venv/bin/deactivate

# Kill the SSH agent
kill $SSH_AGENT_PID

echo "Script completed at $(/bin/date)"