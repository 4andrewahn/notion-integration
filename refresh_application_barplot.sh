#!/bin/bash
# refresh_application_barplot.sh

# Activate the virtual environment
source /Users/andrew/Documents/Coding/Notion-Integrations/.venv/bin/activate

# Run your Python script to create new plot
python /Users/andrew/Documents/Coding/Notion-Integrations/application_graph_script.py

# Add changes to new Git commit
git add -A

# Add commit message
git commit -m "updated bar-plot"

# Push changes to GitHub
git push origin main

# Deactivate the virtual environment
deactivate