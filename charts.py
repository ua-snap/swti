"""
Configuration for static charts
that don't react to user inputs!
"""
# pylint: disable=C0103

import datetime
import plotly.graph_objs as go
import luts
from data import fetch_data

# di = daily index dataframe
di = fetch_data()

# Get date start/end ranges for default window into data.
start_date = (datetime.date.today() + datetime.timedelta(days=-90)).strftime("%Y-%m-%d")
end_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

daily_index = go.Figure(
    data=[go.Bar(x=di["date"], y=di["daily_index"], marker_color=di["color"])],
    layout=go.Layout(
        template=luts.plotly_template,
        title=dict(text="Alaska Statewide Temperature Index"),
        xaxis=dict(type="date", range=[start_date, end_date], rangeslider=dict(visible=True)),
    ),
)
