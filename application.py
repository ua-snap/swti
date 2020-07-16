# pylint: disable=C0103,C0301,E0401
"""
Template for SNAP Dash apps.
"""
import os
import datetime
import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from gui import layout
from data import fetch_data
import luts

app = dash.Dash(__name__)

# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server
app.index_string = luts.index_string
app.title = luts.title
app.layout = layout

# Input value added to allow for cache to be refreshed after becoming
# invalid from the number of seconds indicated in data.py. This is set to
# 43200 seconds by default.
@app.callback(
    Output("daily-index", "figure"), [Input("cache_check_input", "value")],
)
def update_daily_index(nonce):  # deliberate unused arg
    """ Generate precipitation scatter chart """
    # Get date start/end ranges for default window into data.
    start_date = (datetime.date.today() + datetime.timedelta(days=-90)).strftime(
        "%Y-%m-%d"
    )
    end_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(
        "%Y-%m-%d"
    )

    di = fetch_data()
    above = di[di.daily_index > 0]
    below = di[di.daily_index <= 0]

    return go.Figure(
        data=[
            go.Scatter(
                x=di["date"],
                y=di["daily_index"],
                showlegend=False,
                name="Above Average",
                mode="lines",
                fill="tozeroy",
                hoverinfo="none",
                line=dict(shape="spline", width=0.5, color="#ccc"),
            ),
            go.Scatter(
                x=above["date"],
                y=above["daily_index"],
                showlegend=True,
                marker_color=luts.colors[1],
                name="Above Average",
                mode="markers",
                hovertemplate="<b>Date:</b> %{x} <br><b>Daily Index:</b> %{y}",
            ),
            go.Scatter(
                x=below["date"],
                y=below["daily_index"],
                showlegend=True,
                marker_color=luts.colors[0],
                name="Below Average",
                mode="markers",
                hovertemplate="<b>Date:</b> %{x} <br><b>Daily Index:</b> %{y}",
            ),
            go.Scatter(
                x=di["date"],
                y=di["daily_index"].rolling(30).mean().round(2),
                name="30-day average",
                hovertemplate="<b>Date:</b> %{x} <br><b>30-day Average:</b> %{y}",
                line=dict(shape="spline", color="#333"),
            ),
        ],
        layout=go.Layout(
            template=luts.plotly_template,
            title=dict(text="Alaska Statewide Temperature Index"),
            yaxis=dict(showgrid=True, zeroline=True, title=dict(text="Index")),
            xaxis=dict(
                showgrid=True,
                type="date",
                range=[start_date, end_date],
                rangeslider=dict(visible=True),
            ),
        ),
    )


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
