#!/bin/bash

# Log file path
LOG_FILE="/Users/andrew/Scripts/Notion-Integrations/application_refresh_log.log"

# Start logging
exec > >(/usr/bin/tee -a $LOG_FILE) 2>&1

# Log script execution start
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
/Users/andrew/Scripts/Notion-Integrations/.venv/bin/python /Users/andrew/Scripts/Notion-Integrations/application_barplot_script.py

# Change working directory to project directory
cd /Users/andrew/Scripts/Notion-Integrations

# Add changes to new Git commit
/usr/bin/git add -A

# Add commit message
/usr/bin/git commit -m "updated barplot"

# Push changes to GitHub
/usr/bin/git push origin main

# Kill the SSH agent
kill $SSH_AGENT_PID

# Log script execution end with additional line for readability 
echo "Script completed at $(/bin/date)"
echo ""

# Note: virtual environment automatically deactivated after execution by `launchctl`