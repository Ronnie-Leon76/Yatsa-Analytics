from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


df = pd.read_csv("./merged_df.csv")
df['created'] = pd.to_datetime(df['created'])
df['created_day'] = pd.Categorical(df['created'].dt.day_name(), categories= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
df['created_year'] = df['created'].dt.year
# combine all the values of TUK TUK, tuk tuk and Tuk Tuk into one and let them be one unique value tuk tuk
df['make'] = df['make'].str.lower()


daily_avg_distance = df.groupby("created_day")[
    "distance"].mean().reset_index()
weekly_avg_distance = df.groupby("created_week")[
    "distance"].mean().reset_index()
monthly_avg_distance = df.groupby("created_month")[
    "distance"].mean().reset_index()
weekdays_vs_weekends_avg_distance = df.groupby(
    "created_dayofweek")["distance"].mean().reset_index()
make_distance = df.groupby("make")["distance"].mean().reset_index()

avg_make_speed = df.groupby("make")["average_speed"].mean().reset_index()

average_speed_trend_over_years = df.groupby('created_year')['average_speed'].mean().reset_index()


# line charts showing the average distance covered by each vehicle in a day, week, month and also weekdays vs weekends basis
daily_avg_fig = px.line(daily_avg_distance, x="created_day", y="distance",
                        title="Average Distance Covered by each vehicle in a day",  labels={"created_day": "Days of the week", "distance": "Distance (m)"}).update_traces(opacity=0.9)
weekly_avg_fig = px.line(weekly_avg_distance, x="created_week", y="distance",
                          title="Average Distance Covered by each vehicle in a week",  labels={"created_week": "Weeks of the year", "distance": "Distance (m)"})
monthly_avg_fig = px.line(monthly_avg_distance, x="created_month", y="distance",
                          title="Average Distance Covered by each vehicle in a month",  labels={"created_month": "Months of the year", "distance": "Distance (m)"})
make_distance_bar = px.bar(make_distance, x="make", y="distance", title="Average Distance Covered by each vehicle",  labels={"make": "Vehicle Make", "distance": "Distance (m)"},height=800)
avg_make_speed_bar = px.bar(avg_make_speed, x="make", y="average_speed", title="Average Speed of each vehicle make",  labels={"make": "Vehicle Make", "average_speed": "Average Speed (km/h)"},height=800)

average_speed_trend_fig = px.line(average_speed_trend_over_years, x="created_year", y="average_speed",
                                  title="Average Speed Trend between 2022 and 2023",  labels={"created_year": "Years", "average_speed": "Average Speed (km/h)"})

weekdays_vs_weekends_bar = px.bar(weekdays_vs_weekends_avg_distance, x="created_dayofweek",
                                  y="distance", title="Average Distance Covered by each vehicle during weekdays vs weekends",  labels={"created_dayofweek": "Weekdays vs Weekends", "distance": "Distance (m)"}).update_traces(width = 0.5)


most_common_destination_bar = px.bar(
    df["destination_address"].value_counts().head(10), x=df["destination_address"].value_counts().head(10).index, y=df["destination_address"].value_counts().head(10), title="Most common destination for vehicles and how frequent they travel to the destination", height=800, labels={"index": "Destination", "destination_address": "Frequency"}, color=df['destination_address'].value_counts().head(10).index
)

vehicles_with_most_trips_bar = px.bar(df['make'].value_counts().head(10), x=df['make'].value_counts().head(10).index, y=df['make'].value_counts().head(10), title="Vehicles with most trips", height=800, labels={"index": "Vehicle Make", "make": "Frequency"}, color=df['make'].value_counts().head(10).index)
vehicles_with_less_trips_bar = px.bar(df['make'].value_counts().tail(10), x=df['make'].value_counts().tail(10).index, y=df['make'].value_counts().tail(10), title="Vehicles with less trips", height=800, labels={"index": "Vehicle Make", "make": "Frequency"}, color=df['make'].value_counts().tail(10).index)
vehicles_with_most_trips_bar.update_layout(xaxis_title="Vehicle Make", yaxis_title="Number of Trips")
vehicles_with_less_trips_bar.update_layout(xaxis_title="Vehicle Make", yaxis_title="Number of Trips")
most_common_destination_bar.update_layout(xaxis_title="Destination", yaxis_title="Number of Trips made to these destination")


external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]


app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Yatsa Data Analytics"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🚗", className="header-emoji"),
                html.H1(
                    children="Yatsa Data Analytics", className="header-title"
                ),
                html.P(
                    children=(
                        "YatsaApp is a car tracking solution that provides real-time GPS tracking and monitoring services for vehicles. This dashboard offers valuable insights derived from the data gathered from the Yatsa fleet of vehicles"
                        
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.H2(children="Average distance covered by the vehicles on a daily, weekly, monthly, and weekdays versus weekends basis", className="card-title"),
                dcc.Dropdown(
                    ['Daily', 'Weekly', 'Monthly', 'Weekdays vs Weekends'],
                    'Daily',
                    id="time_frame",
                    className="dropdown",
                ),     
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[
                            dcc.Graph(
                                id = "avg_dist_plot",
                                config = {"displayModeBar": False},
                            ),
                        ],
                    ),
                    className = "card",
                ),
                html.Div(
                    dcc.Markdown(children='''
                                    -  Average distance covered by the vehicles on a daily basis is 11.22 km
                                    -  Average distance covered by the vehicles on a weekly basis is 1038.55 km
                                    -  Average distance covered by the vehicles on a monthly basis is 4500.37 km
                                    -  More distance is covered in the weekend ( 11.52 km ) compared to weekdays ( 11.13 km )
                                 '''
                                ),
                    className = "mardown", 
                ),
            ],
            className = "wrapper",
        ),
        html.Div(
            children=[
                html.H2(children="Distance covered by different vehicle make", className="card-title"),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id = "make_distance",
                        figure = make_distance_bar,
                        config = {"displayModeBar": True},
                    ),
                    className = "card",
                ),
                html.Div(
                    dcc.Markdown(children='''
                                    -  Toyota Hiace and Nissan covers the highest distance ( 26.68 km ) and ( 24.22 km ) respectively
                                    -  Maruti covers the least distance ( 1.26 km )
                                 '''
                                ),
                    className = "mardown", 
                ),
            ],
            className = "wrapper",
        ),
        html.Div(
            children=[
                html.H2(children="Most common destination for vehicles and how frequent they travel to the destination", className="card-title"),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id = "most_common_destination",
                        figure = most_common_destination_bar,
                        config = {"displayModeBar": True},
                    ),
                    className = "card",
                ),
                html.Div(
                    dcc.Markdown(children='''
                                    -  Thika, Kiambu County, Kenya is the most common destination for vehicles and they travel to the destination 466 times
                                 '''
                                ),
                    className = "mardown", 
                ),
            ],
            className = "wrapper",
        ),
        html.Div(
            children=[
                html.H2(children="Average speed of different vehicle makes", className="card-title"),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id = "avg_make_speed",
                        figure = avg_make_speed_bar,
                        config = {"displayModeBar": True},
                    ),
                    className = "card",
                ),
                html.Div(
                    dcc.Markdown(children='''
                                    -  Apart from Lexus nx 300h cvt vehicle, all other vehicles have an average speed below 50km/h
                                    -  Maruti has the least average speed ( 8.6 km/h )
                                 '''
                                ),
                    className = "mardown", 
                ),
            ],
            className = "wrapper",
        ),
        html.Div(
            children=[
                html.H2(children="The trend in average speed of all the assets between 2022 and 2023", className="card-title"),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id = "average_speed_trend",
                        figure = average_speed_trend_fig,
                    ),
                    className = "card",
                ),
                html.Div(
                    dcc.Markdown(children='''
                                    -  Average speed of all the assets has increased from 18.1 km/h in 2022 to 27.93 km/h in 2023
                                 '''
                                ),
                    className = "mardown", 
                ),
            ],
            className = "wrapper",
        ),
        html.Div(
            children=[
                html.H2(children="Vehicles with the most trips", className="card-title"),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id = "most_trips",
                        figure = vehicles_with_most_trips_bar,
                        config = {"displayModeBar": True},
                    ),
                    className = "card",
                ),
                html.Div(
                    dcc.Markdown(children='''
                                    -  tuk tuk, piaggio, car, toyota have the highest number of trips made, 450 trips each
                                 '''
                                ),
                    className = "mardown", 
                ),
            ],
            className = "wrapper",
        ),
        html.Div(
            children=[
                html.H2(children="Vehicles with the less trips", className="card-title"),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id = "less_trips",
                        figure = vehicles_with_less_trips_bar,
                        config = {"displayModeBar": True},
                    ),
                    className = "card",
                ),
                html.Div(
                    dcc.Markdown(children='''
                                    -  Maruti and Honda have the least number of trips made, 3 trips and 1 trip respectively
                                 '''
                                ),
                    className = "mardown", 
                ),
            ],
            className = "wrapper",
        ),
        html.Div(
            children=[
                html.H2(children="Key Takeaways & Recommendations", className="card-title"),
            ]
        ),
        html.Div(
                dcc.Markdown(children='''
                            ## Key Takeaways
                            -  Based on the data regarding the number of trips made and the distance covered per asset make, it can be observed that smaller vehicles tend to have a higher number of trips made compared to larger vehicles.
                            ## Recommendations
                            -  To improve their operations, Yatsa should consider placing greater emphasis on Public Service Vehicles. Our assumption is that smaller vehicles such as tuk-tuks and Piaggios are classified as PSVs therefore it may be beneficial for Yatsa to concentrate their efforts on this caetegory of vehicles as they are covering much distance.
                            -  Yatsa may consider expanding its market to different regions in the country. By exploiting new geographic areas, you can tap into new customer bases and potentially increase your revenue.
                            ## Suggestions
                            -  It may be worth considering providing us with fuel consumption data in the future, as this would allow for more comprehensive insights to be drawn from the data collected from your fleet of vehicles.
                            '''
                        ),
            className = "mardown", 
        ),
        
    ]
)


@app.callback(
    Output("avg_dist_plot", "figure"),
    Input("time_frame", "value"),
)
def update_distance_graph(time_frame):
    if time_frame == "Daily":
        return daily_avg_fig
    elif time_frame == "Weekly":
        return weekly_avg_fig
    elif time_frame == "Monthly":
        return monthly_avg_fig
    elif time_frame == "Weekdays vs Weekends":
        return weekdays_vs_weekends_bar
    else:
        return daily_avg_fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
