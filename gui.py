# pylint: disable=C0103,C0301
"""
GUI for app
"""

import os
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as ddsih
import luts

# For hosting
path_prefix = os.getenv("REQUESTS_PATHNAME_PREFIX") or "/"


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


header = ddsih.DangerouslySetInnerHTML(
    f"""
<div class="container">
<nav class="navbar" role="navigation" aria-label="main navigation">

  <div class="navbar-brand">
    <a class="navbar-item" href="https://uaf-accap.org">
      <img src="{path_prefix}assets/ACCAP_wide.svg">
    </a>

    <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div class="navbar-menu">

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a href="https://uaf-iarc.typeform.com/to/mN7J5cCK#tool=Statewide%20Temperature%20Index" class="button is-link" target="_blank">
            Feedback
          </a>
        </div>
      </div>
    </div>
  </div>
</nav>
</div>
"""
)

about = wrap_in_section(
    [
        ddsih.DangerouslySetInnerHTML(
            f"""
<h1 class="title is-3">Alaska Statewide Temperature Index</h1>
<p>&ldquo;Has it been warmer or colder lately in Alaska?&rdquo; Answer: &ldquo;It&rsquo;s complicated.&rdquo; Why? Alaska is a very large
region with complex geography and sparse data availability. This site presents a statewide temperature index,
a simple indicator that balances accessible information on temperature variation with the complexity of Alaska&rsquo;s climate.</p>
<p>The graph below shows the average temperature across Alaska each day, and compares it to the historical average.  Each dot represents the average temperature across Alaska for that day, and the line marked at 0 represents the average historical temperature.</p>
<ul>
    <li class="camera-icon">Click the <span>
<svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg>
</span> icon in the upper&ndash;right of the chart to download it.</li>
    <li>You can show up to two years of data by adjusting the controls immediately below the main chart.</li>
</ul>
            """
        )
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
        ddsih.DangerouslySetInnerHTML(
            f"""

<ul>
    <li>Red dots indicate &ldquo;warmer than normal&rdquo; temperatures. Blue dots indicate &ldquo;colder than
normal.&rdquo; </li>
    <li>The distance above or below the historical average (where the index is 0) represents the amount of deviation from normal. A
value of +1, for instance, means that the day is warmer than 10% of all above&ndash;normal days.  A value of +2 is warmer
than 20% of all above&ndash;normal days. And a value of +10 is a record high for that day, with a temperature higher than
all other above&ndash;normal days.</li>
    <li>The black line represents a running 30&ndash;day average. This line is less affected by short&ndash;term (1&ndash;3 day)
temperature anomalies.</li>
    <li>Below the chart, a diagram displays the past two years of index data and what portion of that data is
displayed in the larger chart. These boundaries are set to the last 6 months by default. Shift the boundaries in this
box to define the beginning and end dates of the larger chart.</li>
</ul>
"""
        ),
        html.H3("How this graph works", className="title is-4"),
        ddsih.DangerouslySetInnerHTML(
            f"""
This graph compares reliable observations from a network of stations distributed across the state to baseline normals collected and averaged over the three&ndash;decade period from 1981 to 2010. Data is collected from the National Weather Service’s <a href="https://www.weather.gov/asos/">Automated Surface Observing Systems</a> (ASOS). This system includes mean and standard deviations of daily normal temperatures, and covers most of the state.
            """
        ),
        html.Figure(
            children=[
                html.Img(
                    height="480px",
                    width="600px",
                    src=path_prefix + "assets/asos_station_map.png",
                ),
                html.Figcaption(
                    "Map of the ASOS stations used to determine the Statewide Temperature Index"
                ),
            ]
        ),
        ddsih.DangerouslySetInnerHTML(
            f"""
<p>Utilizing this network allows for the geographic and latitudinal variation inherent to the state of Alaska to be
taken into account without a large degree of complexity.</p>
<h5 class="title is-5">Advantages of a daily temperature index</h5>
<ul>
    <li>It is not strongly influenced by occasional missing data points</li>
    <li>It is best at distinguishing moderate anomalies in statewide temperatures.</li>
    <li>A single number is easy to understand and disseminate.</li>
</ul>
<h5 class="title is-5">Other considerations</h5>
<ul>
    <li>A single index number can make the data easy to misunderstand, and makes it challenging to quantify extreme
temperature variations.</li>
    <li>Production of the index using the ASOS system also means that the index has the same gaps in its regional
coverage as that system. The ASOS system is subject to occasional sensor failures, as well as failures in
communication systems. There can be some lag between failure and repair.</li>
</ul>
<p>Source code for this project can be found on <a href="https://github.com/ua-snap/swti">Github</a>.</p>
            """
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
        ddsih.DangerouslySetInnerHTML(
            f"""
<div class="container">
    <div class="wrapper is-size-6">
        <img src="{path_prefix}assets/UAF.svg"/>
        <div class="wrapped">
            <p>The Alaska Statewide Temperature Index was developed by Rick Thoman and Brian Brettschneider from data provided by the National Weather Service ASOS system. This website was developed by the <a href="https://uaf-accap.org/">Alaska Center for Climate Assessment and Policy (ACCAP)</a> and the <a href="https://www.snap.uaf.edu/" title="👍">Scenarios Network for Alaska and Arctic Planning (SNAP)</a>, research groups at the <a href="https://uaf-iarc.org/">International Arctic Research Center (IARC)</a> at the <a href="https://uaf.edu/uaf/">University of Alaska Fairbanks (UAF)</a>.</p>
            <p>Copyright &copy; {current_year} University of Alaska Fairbanks.  All rights reserved.</p>
            <p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.  <a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a></p>
        </div>
    </div>
</div>
            """
        ),
    ],
)

layout = html.Div(children=[header, about, daily_index, tool_info, footer])
