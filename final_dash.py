# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# successful_df=spacex_df[spacex_df["class"]==1].copy()
# Create a dash application
app = dash.Dash(__name__)
# dropdown_options=  options=[{'label': 'Class', 'value': 'Class'}]
launch_site = list(spacex_df["Launch Site"].unique())
launch_site.append("ALL")
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites

                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': i, 'value': i} for i in launch_site],
                                             placeholder="select launch site"),
                                # html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                dcc.Graph(id='success-pie-chart'),
                                # html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min_payload, max_payload, 1000, id='payload-slider',
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                dcc.Graph(id='success-payload-scatter-chart'),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(sitedropdown):
    if sitedropdown == 'ALL':
        data = spacex_df[spacex_df["class"] == 1].copy()
        fig = px.pie(data, values='class',
                     names='Launch Site',
                     title='title')
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == sitedropdown]
        fig = px.pie(filtered_df,
                     values='Flight Number',
                     names='class',
                     title='title')
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")],
)
def draw_scatter(entered_site, payload):
    print(payload)
    filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] > payload[0]) & (spacex_df["Payload Mass (kg)"] < payload[1])]

    if entered_site == "ALL":
        figure = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return figure
    else:
        df3 = filtered_df[filtered_df["Launch Site"] == entered_site]
        figure = px.scatter(df3, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return figure


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
