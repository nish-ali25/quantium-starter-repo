import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# 1. Load the data you generated in the previous step
df = pd.read_csv('data/formatted_daily_sales.csv')

# 2. Convert the 'Date' column to datetime objects so it sorts chronologically, not alphabetically
df['Date'] = pd.to_datetime(df['Date'])

# 3. Sort the dataframe by date
df = df.sort_values(by='Date')

# 4. Create the line chart using Plotly Express
fig = px.line(
    df, 
    x='Date', 
    y='Sales', 
    title='Pink Morsel Sales Over Time',
    labels={'Sales': 'Total Sales ($)', 'Date': 'Date'} # Customizing axis labels
)

# Convert the date string into milliseconds
target_date = pd.Timestamp('2021-01-15').timestamp() * 1000

fig.add_vline(x=target_date, line_dash="dash", line_color="red", annotation_text="Price Increase")
# 5. Initialize the Dash app
app = dash.Dash(__name__)

# 6. Define the layout of the app
app.layout = html.Div(children=[
    # Header element
    html.H1(
        children='Soul Foods: Pink Morsel Sales Visualizer',
        style={'textAlign': 'center'}
    ),
    
    # Subheader / Description
    html.Div(
        children='Analyzing sales before and after the price increase on Jan 15, 2021.',
        style={'textAlign': 'center', 'marginBottom': '20px'}
    ),

    # The Graph element
    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

# 7. Run the app
if __name__ == '__main__':
    app.run(debug=True)