''' To-Do's Database Nightly Clean/Reset Integration '''
import os
from datetime import datetime
from notion_client import Client
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
TODO_DATABASE_ID = os.environ.get('TODO_DATABASE_ID')

# Initialize the client
notion = Client(auth=NOTION_TOKEN)

# Retrieve the database
db = notion.databases.query(**{'database_id': TODO_DATABASE_ID}).get('results')