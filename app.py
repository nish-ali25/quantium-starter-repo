import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# 1. Load and prepare the data
df = pd.read_csv('data/formatted_daily_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

# 2. Initialize the Dash app
app = dash.Dash(__name__)

# 3. Define a custom color palette for our CSS styling
colors = {
    'background': '#F4F4F9',      # Light grey/blue background
    'text': '#333333',            # Dark grey text for readability
    'primary': '#E36488',         # "Pink Morsel" thematic pink
    'card_bg': '#FFFFFF'          # White background for components
}

# 4. Define the layout of the app with inline CSS styling
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '40px', 'fontFamily': 'Arial, sans-serif', 'minHeight': '100vh'}, children=[
    
    # Header element
    html.H1(
        children='Soul Foods: Pink Morsel Sales Visualizer',
        style={
            'textAlign': 'center',
            'color': colors['primary'],
            'fontWeight': 'bold',
            'marginBottom': '10px'
        }
    ),
    
    # Subheader / Description
    html.Div(
        children='Analyzing sales before and after the price increase on Jan 15, 2021.',
        style={
            'textAlign': 'center', 
            'color': colors['text'], 
            'marginBottom': '40px',
            'fontSize': '18px'
        }
    ),

    # Container for the Radio Buttons
    html.Div([
        html.Label('Filter by Region:', style={'fontWeight': 'bold', 'marginRight': '15px', 'fontSize': '16px'}),
        dcc.RadioItems(
            id='region-selector',
            options=[
                {'label': ' North ', 'value': 'north'},
                {'label': ' East ', 'value': 'east'},
                {'label': ' South ', 'value': 'south'},
                {'label': ' West ', 'value': 'west'},
                {'label': ' All Regions ', 'value': 'all'}
            ],
            value='all', # Set default value to 'all'
            inline=True,
            style={'display': 'inline-block', 'color': colors['text']}
        )
    ], style={
        'textAlign': 'center', 
        'marginBottom': '30px', 
        'padding': '20px', 
        'backgroundColor': colors['card_bg'], 
        'borderRadius': '10px', 
        'boxShadow': '0px 4px 6px rgba(0,0,0,0.05)',
        'width': '60%',
        'margin': '0 auto 30px auto' # Centers the box
    }),

    # Container for the Graph
    html.Div([
        dcc.Graph(id='sales-line-chart')
    ], style={
        'backgroundColor': colors['card_bg'], 
        'padding': '20px', 
        'borderRadius': '10px', 
        'boxShadow': '0px 4px 6px rgba(0,0,0,0.05)'
    })
])

# 5. Define the callback to update the graph based on the radio button selection
@app.callback(
    Output('sales-line-chart', 'figure'),  # The output is the figure property of the graph
    Input('region-selector', 'value')      # The input is the value property of the radio buttons
)
def update_graph(selected_region):
    # Filter the dataframe based on the selected region
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['Region'] == selected_region]
        
    # Group by Date to get total daily sales across the selected scope
    grouped_df = filtered_df.groupby('Date')['Sales'].sum().reset_index()

    # Create the line chart
    fig = px.line(
        grouped_df, 
        x='Date', 
        y='Sales', 
        title=f'Pink Morsel Sales Over Time ({selected_region.capitalize()})',
        labels={'Sales': 'Total Sales ($)', 'Date': 'Date'}
    )
    
    # Add the vertical line marking the price increase
    target_date = pd.Timestamp('2021-01-15').timestamp() * 1000
    fig.add_vline(x=target_date, line_dash="dash", line_color="red", annotation_text="Price Increase")
    
    # Update figure layout to match our CSS theme
    fig.update_layout(
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['card_bg'],
        font_color=colors['text'],
        title_x=0.5, # Center the title
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    # Update the line color
    fig.update_traces(line_color=colors['primary'])

    return fig

# 6. Run the app
if __name__ == '__main__':
    app.run(debug=True)