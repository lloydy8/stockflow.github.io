import mercury as mr
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import ipywidgets as widgets
from IPython.display import display
from statistics import mean
import plotly.graph_objs as go

button = mr.Button(label="Refresh", style="success")
start_date = mr.Text(value="01/12/2023", label="What is the start date?")
intervals = mr.Numeric(value=600, min=20,max=900,label='Intervals: ',step=10)
interval = mr.Slider(value=1, min=1, max=7, label="Interval (dt): ", step=6)
demand_coef_perc = mr.Slider(value = 2, min=0, max=30, label="Demand Coefficient (%): ", step=1)
activity_coef_perc = mr.Slider(value = 2, min=0, max=30, label="Activity Coefficient (%): ", step=1)
initial_demand = mr.Numeric(value = 130, min=0, max=500, label="Initial Demand: ", step=10)
initial_activity = mr.Numeric(value = 130, min=0, max=500, label="Initial Activity: ", step=10)
WIP_Start = mr.Numeric(value = 100, min=0, max=500, label="WIP Start: ", step=10)
demand_growth_perc = mr.Slider(value = 2, min=0, max=30, label="Demand Growth on Year (%): ", step=1)
activity_growth_perc = mr.Slider(value = 2, min=0, max=30, label="Activity Growth on Year (%): ", step=1)
weekend_demand = mr.Checkbox(value=True, label='Weekend Demand')
weekend_activity_saturday = mr.Checkbox(value=True, label='Saturday Activity')
weekend_activity_sunday = mr.Checkbox(value=True, label='Sunday Activity')
note = mr.Note(text="**Set Demand & Activity after a date.**")

update_tick_1 = mr.Checkbox(value=False, label='Check the box to Update (1)')
update_1 = mr.Text(value="01/03/2024", label="Date: ")
update_demand_1 = mr.Numeric(value = 130, min=0, max=500, label="Update Demand: ", step=10)
update_activity_1 = mr.Numeric(value = 130, min=0, max=500, label="Update Activity: ", step=10)
update_date_1 = pd.to_datetime(update_1.value, format='%d/%m/%Y')

update_tick_2 = mr.Checkbox(value=False, label='Check the box to Update (2)')
update_2 = mr.Text(value="01/04/2024", label="Date: ")
update_demand_2 = mr.Numeric(value = 130, min=0, max=500, label="Update Demand:", step=10)
update_activity_2 = mr.Numeric(value = 130, min=0, max=500, label="Update Activity:", step=10)
update_date_2 = pd.to_datetime(update_1.value, format='%d/%m/%Y')

update_tick_3 = mr.Checkbox(value=False, label='Check the box to Update (3)')
update_3 = mr.Text(value="01/05/2024", label="Date: ")
update_demand_3 = mr.Numeric(value = 130, min=0, max=500, label="Update Demand:", step=10)
update_activity_3 = mr.Numeric(value = 130, min=0, max=500, label="Update Activity:", step=10)
update_date_3 = pd.to_datetime(update_1.value, format='%d/%m/%Y')

update_tick_4 = mr.Checkbox(value=False, label='Check the box to Update (4)')
update_4 = mr.Text(value="01/06/2024", label="Date: ")
update_demand_4 = mr.Numeric(value = 130, min=0, max=500, label="Update Demand:", step=10)
update_activity_4 = mr.Numeric(value = 130, min=0, max=500, label="Update Activity:", step=10)
update_date_4 = pd.to_datetime(update_1.value, format='%d/%m/%Y')

update_tick_5 = mr.Checkbox(value=False, label='Check the box to Update (5)')
update_5 = mr.Text(value="01/07/2024", label="Date: ")
update_demand_5 = mr.Numeric(value = 130, min=0, max=500, label="Update Demand:", step=10)
update_activity_5 = mr.Numeric(value = 130, min=0, max=500, label="Update Activity:", step=10)
update_date_5 = pd.to_datetime(update_1.value, format='%d/%m/%Y')

#Input Variables
activity_coef = activity_coef_perc.value / 100
demand_coef = demand_coef_perc.value / 100
demand_growth = demand_growth_perc.value / 100
average_growth = activity_growth_perc.value / 100

date_obj = datetime.strptime(start_date.value, '%d/%m/%Y')

date_range_week = pd.date_range(start=date_obj, periods=int(intervals.value), freq='7D')
date_range_day = pd.date_range(start=date_obj, periods=int(intervals.value), freq='1D')

if interval.value == 1:
    df = pd.DataFrame({'Date': date_range_day[::int(intervals.value) // len(date_range_week)]})
    x = 365
else:
    df = pd.DataFrame({'Date': date_range_week})
    x = 52

df['Day'] = df['Date'].dt.day_name()

df['Average Activity'] = initial_activity.value
df['Average Demand'] = initial_demand.value

df['Refresh'] = 1


# Method for updating the Average Demand

#Update 1

if update_tick_1.value == True:
    df.loc[df['Date'] >= str(update_date_1), 'Average Demand'] = update_demand_1.value
    df.loc[df['Date'] >= str(update_date_1), 'Average Activity'] = update_activity_1.value

#Update 2

if update_tick_2.value == True:
    df.loc[df['Date'] >= str(update_date_2), 'Average Demand'] = update_demand_2.value
    df.loc[df['Date'] >= str(update_date_2), 'Average Activity'] = update_activity_2.value

#Update 3

if update_tick_3.value == True:
    df.loc[df['Date'] >= str(update_date_3), 'Average Demand'] = update_demand_3.value
    df.loc[df['Date'] >= str(update_date_3), 'Average Activity'] = update_activity_3.value

#Update 4

if update_tick_4.value == True:
    df.loc[df['Date'] >= str(update_date_4), 'Average Demand'] = update_demand_4.value
    df.loc[df['Date'] >= str(update_date_4), 'Average Activity'] = update_activity_4.value

#Update 5

if update_tick_5.value == True:
    df.loc[df['Date'] >= str(update_date_5), 'Average Demand'] = update_demand_5.value
    df.loc[df['Date'] >= str(update_date_5), 'Average Activity'] = update_activity_5.value


#Formula for Growth over year

average_demand = []
for a in range(1, int(intervals.value) + 1, 1):
    average_demand.append(1+(a/ x) * demand_growth)
    

average_activity = []
for b in range(1, int(intervals.value) + 1, 1):
    average_activity.append(1+(b/ x) * average_growth)
    

df['Average Demand'] = df['Average Demand'] * average_demand
df['Average Activity'] = df['Average Activity'] * average_activity



# Creating the Approximate Demand

std_dev_demand = df['Average Demand'] * demand_coef 
df['Approximate Demand'] = np.random.normal(df['Average Demand'], std_dev_demand)

# Creating the Approximate Activity

st_dev_activity = df['Average Activity'] * activity_coef
df['Approximate Activity'] = np.random.normal(df['Average Activity'], st_dev_activity)


# If Weekend Demand = No

if weekend_demand.value == False:
    if 'Saturday' in df['Day'].values:
        saturday_index = df[df['Day'] == 'Saturday'].index
        df.loc[saturday_index, 'Average Demand'] = 0
        df.loc[saturday_index, 'Approximate Demand'] = 0
    
    if 'Sunday' in df['Day'].values:
        sunday_index = df[df['Day'] == 'Sunday'].index
        df.loc[sunday_index, 'Average Demand'] = 0
        df.loc[sunday_index, 'Approximate Demand'] = 0

if weekend_activity_saturday.value == False:
    if 'Saturday' in df['Day'].values:
        saturday_index = df[df['Day']== 'Saturday'].index
        df.loc[saturday_index, 'Average Activity'] = 0
        df.loc[saturday_index, 'Approximate Activity'] = 0


if weekend_activity_sunday.value == False:
    if 'Sunday' in df['Day'].values:
        sunday_index = df[df['Day']== 'Sunday'].index
        df.loc[sunday_index, 'Average Activity'] = 0
        df.loc[sunday_index, 'Approximate Activity'] = 0
    

# Creating the WIP

df['WIP'] = np.maximum(0, WIP_Start.value + df['Approximate Demand'] - df['Approximate Activity'])

# Calculate subsequent 'WIP' values based on the previous 'WIP' value
for i in range(1, len(df)):
    df.loc[i, 'WIP'] = np.maximum(0, df.loc[i - 1, 'WIP'] + df.loc[i, 'Approximate Demand'] - df.loc[i, 'Approximate Activity'])
    
average_waiting_time = []
a=0

df['Average Waiting Time'] = 1

df.loc[0, 'Average Waiting Time'] = df['WIP'][0] / mean(df['Approximate Demand'][:5])
df.loc[1, 'Average Waiting Time'] = df['WIP'][1] / mean(df['Approximate Demand'][:5])
df.loc[2, 'Average Waiting Time'] = df['WIP'][2] / mean(df['Approximate Demand'][:5])
df.loc[3, 'Average Waiting Time'] = df['WIP'][3] / mean(df['Approximate Demand'][:5])
df.loc[4, 'Average Waiting Time'] = df['WIP'][4] / mean(df['Approximate Demand'][:5])
df.loc[5, 'Average Waiting Time'] = df['WIP'][5] / mean(df['Approximate Demand'][:6])
df.loc[6, 'Average Waiting Time'] = df['WIP'][6] / mean(df['Approximate Demand'][:7])

# Assuming intervals and df are defined elsewhere
a = 1

for i in range(7, int(intervals.value)):
    df.loc[i, 'Average Waiting Time'] = df['WIP'][i] / df['Approximate Demand'].iloc[a:i+1].mean()
    a += 1
    
    
if button.clicked:
    df['Refresh'] = df['Refresh'] * 1


# Create traces for 'Approximate Demand' and 'Approximate Activity'
trace1 = go.Scatter(x=df['Date'], y=df['Approximate Demand'], mode='lines', name='Demand', line=dict(color='blue'))
trace2 = go.Scatter(x=df['Date'], y=df['Approximate Activity'], mode='lines', name='Activity', line=dict(color='red'))

# Create trace for 'WIP' on a secondary y-axis
trace3 = go.Scatter(x=df['Date'], y=df['WIP'], mode='lines', name='WIP', line=dict(color='green'), yaxis='y2')

# Define the layout with secondary y-axis and lower limits set to 0
layout = go.Layout(
    xaxis=dict(title='Date', showgrid=True, tickangle=310),
    yaxis=dict(
        title='<b>No. of Patients Demand & Activity per time interval (dt)</b>',
        showgrid=True,
        range=[0, df[['Approximate Demand', 'Approximate Activity']].values.max()+20],
        showline=True,
        tickfont=dict(size=14, family='Arial', color='black'),
        titlefont=dict(size=18, family='Arial', color='black')
    ),
    yaxis2=dict(
        title='<b>No. of Patients WIP</b>',
        overlaying='y',
        side='right',
        showgrid=False,
        range=[0, df['WIP'].max()+20],
        showline=True,
        tickfont=dict(size=14, family='Arial', color='green'),  # Setting the tick color for the right y-axis
        titlefont=dict(size=18, family='Arial', color='green')  # Setting the title color for the right y-axis
    ),
    hovermode='closest',
    legend=dict(x=0.4, y=-0.22, orientation='h'),  # Position the legend below the chart
    margin=dict(t=20, b=80, l=80, r=80),  
)

# Create the figure with traces and layout
fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)

# Create a second plot for Average Waiting Time
trace_waiting_time = go.Scatter(x=df['Date'], y=df['Average Waiting Time'], mode='lines', name='Average Waiting Time', line=dict(color='orange'))

# Define a new layout for the second plot underneath the first plot
layout_waiting_time = go.Layout(
    xaxis=dict(title='Date', showgrid=True, tickangle=310),
    yaxis=dict(
        title='<b>Average Waiting Time</b>',
        showgrid=True,
        showline=True,
        range=[0, df['Average Waiting Time'].max()],
        tickfont=dict(size=14, family='Arial', color='black'),
        titlefont=dict(size=18, family='Arial', color='black')
    ),
    hovermode='closest',
    legend=dict(x=0.4, y=-0.18, orientation='h'),  # Position the legend below the chart
    height=400,  # Adjust the height for the second plot as needed
    margin=dict(t=20, b=80, l=80, r=80),
)

# Create the figure with the trace for Average Waiting Time and its layout
fig_waiting_time = go.Figure(data=[trace_waiting_time], layout=layout_waiting_time)

# Display both plots
fig.show()
fig_waiting_time.show()
