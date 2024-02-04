#!/bin/bash

# Log file path
LOG_FILE="/Users/andrew/Scripts/Notion-Integrations/todo_update_log.log"

# Start logging
exec > >(/usr/bin/tee -a $LOG_FILE) 2>&1

# Log script execution start
echo "Starting script at $(/bin/date)"

# Activate the virtual environment
source /Users/andrew/Scripts/Notion-Integrations/.venv/bin/activate

# Run your Python script to create new plot
/Users/andrew/Scripts/Notion-Integrations/.venv/bin/python /Users/andrew/Scripts/Notion-Integrations/todo_reset_script.py

# Log script execution end with additional line for readability 
echo "Script completed at $(/bin/date)"
echo ""

# Note: virtual environment automatically deactivated after execution by `launchctl`