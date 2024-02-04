''' To-Do's Database Nightly Clean/Reset Integration '''
import os
from datetime import datetime, timedelta
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
TODO_DATABASE_ID = os.environ.get('TODO_DATABASE_ID')

# Initialize the client
notion = Client(auth=NOTION_TOKEN)

# Retrieve the database
db = notion.databases.query(**{'database_id': TODO_DATABASE_ID}).get('results')

'''
Helper Functions
'''
def get_next_due_date_str(date_str, days_delta):
    # Convert string to datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Add specified number of days
    new_date_obj = date_obj + timedelta(days=days_delta)

    # Convert back to string
    new_date_str = new_date_obj.strftime("%Y-%m-%d")

    return new_date_str


def update_and_reset_todo_entries(page_obj):
    P_id = page_obj['id']

    cur_due_date_str = page_obj['properties']['Due']['date']['start']
    days_to_add = page_obj['properties']['[Repeat in # days]']['number']
    next_due_date_str = get_next_due_date_str(cur_due_date_str, days_to_add)
    
    update_data = {
        '[Total Mins Spent]': { # Update running totals data
            'number': page_obj['properties']['[Updated Total Mins Spent]']['formula']['number']
        },
        '[Total #\'s Completed]': {
            'number': page_obj['properties']['[Updated Total #\'s Completed]']['formula']['number']
        },
        '[Time Started]': { # Clear Start and End timestamps
            'date': None
        },
        'Status': { # Reset Status
            'status': {
                'name': 'Not started'
            }
        },
        'Due': { # Increment 'Due' date by '[Repeat in # days]'
            'date': {
                'start': next_due_date_str
            }
        }
    }

    notion.pages.update(page_id=P_id, properties=update_data)

'''
Retrieve information and Update
'''

for item in db:
    # Clean and reset recurring to-do items
    if item['properties']['[Recurring?]']['checkbox'] == True:
        update_and_reset_todo_entries(item)