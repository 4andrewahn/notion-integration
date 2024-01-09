''' Main Notion Integration '''
import os
from datetime import datetime
from notion_client import Client
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
APPLICATION_DATABASE_ID = os.environ.get('APPLICATION_DATABASE_ID')

# Initialize the client
notion = Client(auth=NOTION_TOKEN)

# Retrieve the database
db = notion.databases.query(**{'database_id': APPLICATION_DATABASE_ID}).get('results')


''' Parse retrieved Notion database into Pandas dataframe '''

parsed_data = {
    'days_elapsed': [],
    'date_applied': []
    # 'status': [] # now changed to 'multi_select'
}

for entry in db:
    db_days_elapsed = entry['properties']['days elapsed']['formula']['number']
    db_date_applied = entry['properties']['Date Applied']['date']['start']
    # db_status = entry['properties']['Status']['select']['name']

    parsed_data['date_applied'].append(db_date_applied)
    parsed_data['days_elapsed'].append(db_days_elapsed)
    # parsed_data['status'].append(db_status)

df = pd.DataFrame(parsed_data)
df['date_applied'] = pd.to_datetime(df['date_applied'])
df = df.sort_values(by='days_elapsed')


''' Generate bar-plot data for # of Applications Sent per Day [Last 30 Days] '''
# Define color palette for bar
'''
10-color Temperature Gradient
{ 
    0: '#f77772',
    1: '#f78072',
    2: '#f78972',
    3: '#f79272',
    4: '#f79b72',
    5: '#ea9b7f',
    6: '#cf929a',
    7: '#b589b4',
    8: '#9a80cf',
    9: '#7f77ea'
}
'''

bar_color_palette = {
    0: '#f72585',
    1: '#7209b7',
    2: '#3a0ca3',
    3: '#4361ee',
    4: '#4cc9f0'
}

# Generate a list of the last 30 days with today at the end of the list
end_date = datetime.today()
start_date = end_date - pd.Timedelta(days=29)

dates = pd.date_range(start=start_date, end=end_date, freq='D')
dates_list = dates.to_list()

# Generate X and Y values as a list to plot
highest_y = 0
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

    if ct > highest_y: 
        highest_y = ct
    formatted_last_date = cur_date.strftime('%b %-d')
    last_30_days.append(formatted_last_date)
    num_sent_per_day.append(ct)

last_30_days.reverse()
num_sent_per_day.reverse()

x_vals = last_30_days
y_vals = num_sent_per_day
for i in range(30):
    print(f"x={x_vals[i]}, y={y_vals[i]}")

print(f"{len(x_vals)} x-values")
print(f"{len(y_vals)} y-values")

bar_colors = [] # Stores colors for each bar according to y-value
for y in y_vals:
    cur_color = bar_color_palette.get(y, None)
    if cur_color is not None:
        bar_colors.append(cur_color)
    else:
        bar_colors.append('#80ffdb')

print(f"{len(bar_colors)} colors in bar-colors")

''' Create bar-plot # of Applications Sent per Day [Last 30 Days] '''
fig = px.bar(df, x=x_vals, y=y_vals,
             color=bar_colors,
             hover_name=y_vals)

# Customize the theme of the plot 
fig.update_layout(
    showlegend = False,
    paper_bgcolor='#191919', # Figure background color
    plot_bgcolor='#232425', # Plot background color
    font = { # Global font style 
        "family": "Noto Sans, sans-serif",
        "color": "#dee4ed"
    },
    title = {
        'text': "# of Applications Sent per Day [Last 30 Days]",
        "font_size": 24
    },
    hoverlabel = {
        "bgcolor": "#191919",
        "font_size": 14
    }
)
fig.update_traces(
    marker_color = bar_colors,
    marker_line_color = bar_colors,
    marker_line_width = 5
)

fig.update_xaxes(
    title_text = None,
    tickangle = -45,
    tickfont = {
        "family": "Noto Sans, sans-serif"
    }
)

fig.update_yaxes(
    title_text = None,
    tickvals = [_ for _ in range(1, highest_y + 1)],
    ticktext = [f"{tval}  " for tval in range(1, highest_y + 1)],
    tickfont = {
        "family": "Noto Sans, sans-serif",
        "color": "#dee4ed"
    }
)

fig.show()


# Save the figure as an HTML file
# fig.write_html('/Users/andrew/Scripts/Notion-Integrations/docs/index.html', auto_open=False)