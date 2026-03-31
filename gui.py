# pylint: disable=C0103,C0301
"""
GUI for app
"""

import os
from datetime import datetime
from dash import dcc, html
import luts

# For hosting
path_prefix = os.getenv("DASH_REQUESTS_PATHNAME_PREFIX") or "/"


# Helper functions
def wrap_in_section(content, section_classes="", container_classes="", div_classes=""):
    """
    Helper function to wrap sections.
    Accepts an array of children which will be assigned within
    this structure:
    <section class="section">
        <div class="container">
            <div>[children]...
    """
    return html.Section(
        className="section " + section_classes,
        children=[
            html.Div(
                className="container " + container_classes,
                children=[html.Div(className=div_classes, children=content)],
            )
        ],
    )


header = html.Div(
    className="container",
    children=[
        html.Nav(
            className="navbar",
            role="navigation",
            **{"aria-label": "main navigation"},
            children=[
                html.Div(
                    className="navbar-brand",
                    children=[
                        html.A(
                            className="navbar-item",
                            href="https://uaf-accap.org",
                            children=[
                                html.Img(
                                    src=f"{path_prefix}assets/ACCAP_wide.svg",
                                    alt="Alaska Center for Climate Assessment and Preparedness (ACCAP)",
                                )
                            ],
                        )
                    ],
                )
            ],
        )
    ],
)

about = wrap_in_section(
    [
        html.H1("Alaska Statewide Temperature Index", className="title is-3"),
        html.P(
            '"Has it been warmer or colder lately in Alaska?" Answer: "It\'s complicated." Why? Alaska is a very large '
            "region with complex geography and sparse data availability. This site presents a statewide temperature index, "
            "a simple indicator that balances accessible information on temperature variation with the complexity of Alaska's climate."
        ),
        html.P(
            "The graph below shows the average temperature across Alaska each day, and compares it to the historical average. "
            "Each dot represents the average temperature across Alaska for that day, and the line marked at 0 represents the average historical temperature."
        ),
        html.Ul(
            [
                html.Li(
                    [
                        "Click the ",
                        html.Img(
                            src=f"{path_prefix}assets/camera.svg",
                            alt="camera",
                            className="icon",
                            style={
                                "height": "1em",
                                "width": "1em",
                                "display": "inline-block",
                                "verticalAlign": "middle",
                            },
                        ),
                        " icon in the upper-right of the chart to download it.",
                    ],
                    className="camera-icon",
                ),
                html.Li(
                    "You can show up to two years of data by adjusting the controls immediately below the main chart."
                ),
            ]
        ),
    ],
    section_classes="lead",
    div_classes="content is-size-5",
)


# Index as a scatter chart
daily_index = wrap_in_section(
    [
        dcc.Loading(
            id="loading-1",
            children=[dcc.Graph(id="daily-index", config=luts.fig_configs)],
            type="circle",
            className="loading-circle",
        ),
        html.Div(
            className="buttons is-right",
            children=[
                html.A(
                    "Download data",
                    className="button is-link",
                    href="statewide-temperature-index/downloads/statewide_temperature_daily_index.csv",
                )
            ],
        ),
        dcc.Input(id="cache_check_input", type="text", placeholder="nonce"),
    ],
    section_classes="graph",
)


tool_info = wrap_in_section(
    [
        html.H3("About this graph", className="title is-4"),
        html.Ul(
            [
                html.Li(
                    'Red dots indicate "warmer than normal" temperatures. Blue dots indicate "colder than normal."'
                ),
                html.Li(
                    "The distance above or below the historical average (where the index is 0) represents the amount of deviation from normal. A "
                    "value of +1, for instance, means that the day is warmer than 10% of all above-normal days. A value of +2 is warmer "
                    "than 20% of all above-normal days. And a value of +10 is a record high for that day, with a temperature higher than "
                    "all other above-normal days."
                ),
                html.Li(
                    "The black line represents a running 30-day average. This line is less affected by short-term (1-3 day) "
                    "temperature anomalies."
                ),
                html.Li(
                    "Below the chart, a diagram displays the past two years of index data and what portion of that data is "
                    "displayed in the larger chart. These boundaries are set to the last 6 months by default. Shift the boundaries in this "
                    "box to define the beginning and end dates of the larger chart."
                ),
            ]
        ),
        html.H3("How this graph works", className="title is-4"),
        html.P(
            [
                "This graph compares reliable observations from a network of stations distributed across the state to baseline normals collected and averaged over the three-decade period from 1991 to 2020. Data is collected from the National Weather Service's ",
                html.A(
                    "Automated Surface Observing Systems",
                    href="https://www.weather.gov/asos/",
                ),
                " (ASOS). This system includes mean and standard deviations of daily normal temperatures, and covers most of the state.",
            ]
        ),
        html.Figure(
            children=[
                html.Img(
                    height="480px",
                    width="600px",
                    src=path_prefix + "assets/asos_station_map.png",
                    alt="Map of the ASOS stations used to determine the Statewide Temperature Index",
                ),
                html.Figcaption(
                    "Map of the ASOS stations used to determine the Statewide Temperature Index"
                ),
            ]
        ),
        html.P(
            "Utilizing this network allows for the geographic and latitudinal variation inherent to the state of Alaska to be "
            "taken into account without a large degree of complexity."
        ),
        html.H5("Advantages of a daily temperature index", className="title is-5"),
        html.Ul(
            [
                html.Li(
                    "It is not strongly influenced by occasional missing data points"
                ),
                html.Li(
                    "It is best at distinguishing moderate anomalies in statewide temperatures."
                ),
                html.Li("A single number is easy to understand and disseminate."),
            ]
        ),
        html.H5("Other considerations", className="title is-5"),
        html.Ul(
            [
                html.Li(
                    "A single index number can make the data easy to misunderstand, and makes it challenging to quantify extreme "
                    "temperature variations."
                ),
                html.Li(
                    "Production of the index using the ASOS system also means that the index has the same gaps in its regional "
                    "coverage as that system. The ASOS system is subject to occasional sensor failures, as well as failures in "
                    "communication systems. There can be some lag between failure and repair."
                ),
            ]
        ),
        html.P(
            [
                "Source code for this project can be found on ",
                html.A("Github", href="https://github.com/ua-snap/swti"),
                ".",
            ]
        ),
    ],
    section_classes="explainer",
    div_classes="content is-size-5",
)


# Used in copyright date
current_year = datetime.now().year

footer = html.Footer(
    className="footer",
    children=[
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="wrapper is-size-6",
                    children=[
                        html.Img(
                            src=f"{path_prefix}assets/UAF.svg",
                            alt="University of Alaska Fairbanks (UAF)",
                        ),
                        html.Div(
                            className="wrapped",
                            children=[
                                html.P(
                                    [
                                        "The Alaska Statewide Temperature Index was developed by Rick Thoman and Brian Brettschneider from data provided by the National Weather Service ASOS system. This website was developed by the ",
                                        html.A(
                                            "Alaska Center for Climate Assessment and Preparedness (ACCAP)",
                                            href="https://uaf-accap.org/",
                                        ),
                                        " and the ",
                                        html.A(
                                            "Scenarios Network for Alaska and Arctic Planning (SNAP)",
                                            href="https://www.snap.uaf.edu/",
                                            title="👍",
                                        ),
                                        ", research groups at the ",
                                        html.A(
                                            "International Arctic Research Center (IARC)",
                                            href="https://uaf-iarc.org/",
                                        ),
                                        " at the ",
                                        html.A(
                                            "University of Alaska Fairbanks (UAF)",
                                            href="https://uaf.edu/uaf/",
                                        ),
                                        ".",
                                    ]
                                ),
                                html.P(
                                    f"Copyright © {current_year} University of Alaska Fairbanks. All rights reserved."
                                ),
                                html.P(
                                    [
                                        "The ",
                                        html.A(
                                            "University of Alaska",
                                            href="https://www.alaska.edu/",
                                        ),
                                        " is an Equal Opportunity/Equal Access Employer and Educational Institution. The University is committed to a ",
                                        html.A(
                                            "policy of non-discrimination",
                                            href="https://www.alaska.edu/nondiscrimination/",
                                        ),
                                        " against individuals on the basis of any legally protected status.",
                                    ]
                                ),
                                html.P(
                                    [
                                        "UA is committed to providing accessible websites. ",
                                        html.A(
                                            "Learn more about UA's notice of web accessibility",
                                            href="https://www.alaska.edu/webaccessibility/",
                                        ),
                                        ". If we can help you access this website's content, ",
                                        html.A(
                                            "email us!",
                                            href="mailto:uaf-snap-data-tools@alaska.edu",
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )
    ],
)

layout = html.Div(children=[header, about, daily_index, tool_info, footer])
