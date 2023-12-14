''' Main Notion Integration '''
import os
from datetime import datetime
from notion_client import Client
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

print("In Application Graph Script")

NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
APPLICATION_DATABASE_ID = os.environ.get('APPLICATION_DATABASE_ID')

# Initialize the client
notion = Client(auth=NOTION_TOKEN)

# Retrieve the database
db = notion.databases.query(**{'database_id': APPLICATION_DATABASE_ID}).get('results')


''' Parse retrieved Notion database into Pandas dataframe '''

parsed_data = {
    'days_elapsed': [],
    'date_applied': [],
    'status': []
}

for entry in db:
    db_days_elapsed = entry['properties']['days elapsed']['formula']['number']
    db_date_applied = entry['properties']['Date Applied']['date']['start']
    db_status = entry['properties']['Status']['select']['name']

    parsed_data['date_applied'].append(db_date_applied)
    parsed_data['days_elapsed'].append(db_days_elapsed)
    parsed_data['status'].append(db_status)

df = pd.DataFrame(parsed_data)
df['date_applied'] = pd.to_datetime(df['date_applied'])
df = df.sort_values(by='days_elapsed')


''' Generate bar-plot of # of Applications Sent per Day [Last 30 Days] '''

# Generate a list of the last 30 days with today at the end of the list
end_date = datetime.today()
start_date = end_date - pd.Timedelta(days=29)

dates = pd.date_range(start=start_date, end=end_date, freq='D')
dates_list = dates.to_list()

# Generate X and Y values as a list to plot
last_30_days = []
num_sent_per_day = []
for i in range(29, -1, -1):
    ct = 0
    cur_date = dates_list[i].date()

    for j, row in df.iterrows():
        date_applied = row['date_applied'].date()
        if cur_date == date_applied:
            ct += 1
        elif cur_date > date_applied:
            break

    formatted_last_date = cur_date.strftime('%m-%d-%Y')
    last_30_days.append(formatted_last_date)
    num_sent_per_day.append(ct)

last_30_days.reverse()
num_sent_per_day.reverse()

# Create a bar plot
fig = px.bar(x=last_30_days, y=num_sent_per_day, title="# of Applications Sent per Day [Last 30 Days]")

# Save the figure as an HTML file
fig.write_html('/Users/andrew/Documents/Coding/Notion-Integrations/rendered_outputs/num-sent-30-days.html', auto_open=False)
