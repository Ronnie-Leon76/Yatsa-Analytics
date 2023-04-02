from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


df = pd.read_csv("../Data/merged_df.csv")

daily_avg_distance = df.groupby("created_day")[
    "distance"].mean().sort_index()
weekly_avg_distance = df.groupby("created_week")[
    "distance"].mean().reset_index()
monthly_avg_distance = df.groupby("created_month")[
    "distance"].mean().reset_index()
weekdays_vs_weekends_avg_distance = df.groupby(
    "created_dayofweek")["distance"].mean().reset_index()


# line charts showing the average distance covered by each vehicle in a day, week, month and also weekdays vs weekends basis
daily_avg_fig = px.line(daily_avg_distance, x="created_day", y="distance",
                         title="Average Distance Covered by each vehicle in a day",  labels={"created_day": "Days", "distance": "Distance (m)"})
weekly_avg_fig = px.line(weekly_avg_distance, x="created_week", y="distance",
                          title="Average Distance Covered by each vehicle in a week",  labels={"created_week": "Weeks", "distance": "Distance (m)"})
monthly_avg_fig = px.line(monthly_avg_distance, x="created_month", y="distance",
                           title="Average Distance Covered by each vehicle in a month",  labels={"created_month": "Months", "distance": "Distance (m)"})

weekdays_vs_weekends_bar = px.bar(weekdays_vs_weekends_avg_distance, x="created_dayofweek",
                                  y="distance", title="Average Distance Covered by each vehicle during weekdays vs weekends",  labels={"created_dayofweek": "Weekdays vs Weekends", "distance": "Distance (m)"})




most_common_destination_bar = px.bar(
    df["destination_address"].value_counts().head(10), x=df["destination_address"].value_counts().head(10).index, y=df["destination_address"].value_counts().head(10), title="Most common destination for vehicles and how frequent they travel to the destination", width=1000, height=800, labels={"index": "destination", "destination_address": "Number of trips made"}
)



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
                        "Yatsa is a software company that helps you track and manage your assets better."
                        "This dashboard provides insights into the data collected by Yatsa."
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.H2(children="Average Distance Covered by the vehicles on a daily, weekly, monthly, weekend and weekends basis", className="card-title"),
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
                    children = dcc.Graph(
                        id = "avg_dist_plot",
                        config = {"displayModeBar": False},
                    ),
                    className = "card",
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
                )
            ],
            className = "wrapper",
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
    print(daily_avg_distance)
    app.run_server(debug=True)
