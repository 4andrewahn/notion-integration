''' Main Notion Integration '''
import os
from datetime import datetime
from notion_client import Client
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Define color palette for bar
bar_color_palette = {
    '0': '#ff6176', #red
    '1': '#ffb561', #orange
    '2': '#dfff61', #yellow-green
    '3': '#abff61', #green
    '4': '#61ff81' #vibrant green
}

for k in range(5, highest_y+1):
    bar_color_palette[str(k)] = '#61ffb5' #greenish cyan


barplot_df = pd.DataFrame({
        'Date': last_30_days,
        'Count': num_sent_per_day,
        'ct_str': [str(num) for num in num_sent_per_day]
    }
)

bar_colors = [bar_color_palette[val] for val in barplot_df['ct_str']]

''' Create bar-plot # of Applications Sent per Day [Last 30 Days] '''
fig = px.bar(barplot_df, x='Date', y='Count', color='ct_str',
             color_discrete_map=bar_color_palette,
             hover_data={'ct_str': False}
             )


zeros_bar = []
fig.add_trace(go.Bar(
    x=barplot_df['Date'], 
))

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
    },
    bargap=0.1
)

fig.update_traces(
    hovertemplate="<b>%{y}</b>sent<br><i>%{x}</i>",
    marker_line_width=2
)

fig.update_xaxes(
    title_text = None,
    tickangle = -45,
    tickfont = {
        "family": "Noto Sans, sans-serif"
    }
)

fig.update_yaxes(
    range=[-0.1,highest_y+1],
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