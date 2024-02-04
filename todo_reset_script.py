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
def print_dict(input):
    for k in input.keys():
        print(f'\'{k}\': [{type(input[k])}] {input[k]}')


def get_next_due_date_str(date_str, days_delta):
    # Convert string to datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Add specified number of days
    new_date_obj = date_obj + timedelta(days=days_delta)

    # Convert back to string
    new_date_str = new_date_obj.strftime("%Y-%m-%d")

    return new_date_str


def update_and_reset_todo_entries(page_obj):
    page_title = page_obj['properties']['Entry']['title'][0]['plain_text']
    print(f'======= UPDATING Page {page_title} =======\n')
    print(f'[Updated Total Mins Spent]')
    print_dict(page_obj['properties']['[Updated Total Mins Spent]'])
    print('')
    print(f'[Updated Total #\'s Completed]')
    print_dict(page_obj['properties']['[Updated Total #\'s Completed]'])
    print('==============================\n')

    P_id = page_obj['id']
    is_task_complete = bool(page_obj['properties']['Status']['status']['name'] == 'Done')

    cur_due_date_str = page_obj['properties']['Due']['date']['start']
    days_to_add = page_obj['properties']['[Repeat in # days]']['number']
    next_due_date_str = get_next_due_date_str(cur_due_date_str, days_to_add)
    
    update_data = {
        # Clear Start timestamps
        '[Time Started]': { 
            'date': None
        },
        # Reset Status
        'Status': { 
            'status': {'name': 'Not started'}
        },
        # Increment 'Due' date by '[Repeat in # days]'
        'Due': { 
            'date': {'start': next_due_date_str}
        }
    }

    if is_task_complete:
        # Clear End timestamps
        update_data['[Time Completed]'] = {'date': None}
        
        # Update running totals data
        update_data['[Total Mins Spent]'] = page_obj['properties']['[Updated Total Mins Spent]']['formula']['number']
        update_data['[Total #\'s Completed]'] = page_obj['properties']['[Updated Total #\'s Completed]']['formula']['number']

    notion.pages.update(page_id=P_id, properties=update_data)


'''
Retrieve information and Update
'''

for item in db:
    # Clean and reset recurring to-do items
    if item['properties']['[Recurring?]']['checkbox'] == True:
        update_and_reset_todo_entries(item)