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
          <a href="https://uaf-iarc.typeform.com/to/mN7J5cCK#tool=Statewide%20Temperature%20Index" class="button is-primary" target="_blank">
            <strong>Feedback</strong>
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
<h1 class="title is-3">Statewide Temperature Index</h1>
<p>&#34;Has it been cold lately in Alaska?&#34; Answer: &#34;It&#39;s complicated.&#34; Why? Alaska is a very large 
region with complex geography and sparse data availability. This tool develops a statewide temperature index, 
a simple indicator which balances accessible information on temperature variation with the complexity of the data.</p> 
<p>The chart below graphs the average temperature across Alaska each day, and compares it to the historical average.
The line marked at 0 represents the average normal historical temperature. Each dot represents the average
temperature across Alaska for that day.</p>
<ul>
    <li>Red dots indicate &#34;warmer than normal&#34; temperatures. Blue dots indicate “colder than normal.” </li>
    <li>The distance above or below the &#34;normal&#34; line represents the amount of deviation from normal. A value 
of +1, for instance, means that the day is warmer than 10% of all above-normal days.</li> 
    <li>The black line represents a running 30-day average. This line is less affected by short-term (1-3 day)
temperature anomalies.</li>
    <li><p class="camera-icon">Click the <span>
<svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg>
</span> icon in the upper&ndash;right of each chart to download it.</p></li>
</ul>
            """
        )
    ],
    section_classes="lead",
    div_classes="content is-size-5",
)


# Index as a bar chart
daily_index = wrap_in_section(
    [
        html.H3("Statewide temperature index, last 3 months", className="title is-4"),
        dcc.Loading(
            id="loading-1",
            children=[dcc.Graph(id="daily-index", config=luts.fig_configs)],
            type="circle",
            className="loading-circle",
        ),
        dcc.Input(id="cache_check_input", type="text", placeholder="nonce"),
    ],
    section_classes="graph",
)


tool_info = wrap_in_section(
    [
        html.H3("How the Tool Works", className="title is-4"),
        ddsih.DangerouslySetInnerHTML(
            f"""
<p>The tool compares reliable observations from a network of stations distributed across the state to baseline
normals collected and averaged over the three-decade period from 1981 to 2010. Data is collected from the National
Weather Service’s Automated Surface Observing Systems (ASOS). This system includes mean and standard deviations of
daily normal temperatures, and covers most of the state.</p>
<p>Map of the ASOS stations used to determine the Statewide Temperature Index.</p>
            """
        ),
        html.Figure(
            children=[
                html.Img(
                    height="480px",
                    width="600px",
                    src=path_prefix + "assets/asos_station_map.jpg",
                )
            ],
        ),
        ddsih.DangerouslySetInnerHTML(
            f"""
<p>Utilizing this network allows for the geographic and latitudinal variation inherent to the state of Alaska to be
taken into account without a large degree of complexity.</p>
<p>Advantages of a daily temperature index</p>
<ul>
    <li>It is not strongly influenced by occasional missing data points</li>
    <li>It can distinguish moderate anomalies in statewide data. Additionally, a single number is easy to understand and disseminate.</li>
</ul>
<p>Other considerations</p>
<ul>
    <li>A single Index number can make the data easy to misunderstand, and makes it challenging to quantify extreme temperature variations.</li>
    <li>Production of the index using the ASOS system also means that the index has the same gaps in its regional coverage as that system. The ASOS system is subject to occasional sensor failures, as well as failures in communication systems. There can be some lag between failure and repair.</li>
</ul>
            """
        ),
    ],
    div_classes="content is-size-5",
)


credits_section = wrap_in_section(
    [
        html.H3("Credits", className="title is-4"),
        ddsih.DangerouslySetInnerHTML(
            f"""
<p>This tool was created by the <a href="https://uaf-accap.org/">Alaska Center for Climate Assessment and Policy (ACCAP)</a> and the <a href="https://www.snap.uaf.edu/">Scenarios Network for Alaska and Arctic Planning (SNAP)</a>, research groups at the <a href="https://uaf-iarc.org/">International Arctic Research Center (IARC)</a> at the <a href="https://uaf.edu/uaf/">University of Alaska Fairbanks (UAF)</a>. The Alaska Statewide Temperature Index was developed by Rick Thoman and Brian Brettschneider from data provided by the National Weather Service ASOS system.</p>
            """
        ),
    ],
    div_classes="content is-size-5",
)


# Used in copyright date
current_year = datetime.now().year

footer = html.Footer(
    className="footer has-text-centered",
    children=[
        html.Div(
            children=[
                html.A(
                    href="https://uaf-accap.org",
                    className="accap",
                    children=[html.Img(src=path_prefix + "assets/ACCAP_wide.svg")],
                ),
                html.A(
                    href="https://uaf-iarc.org/",
                    children=[html.Img(src=path_prefix + "assets/IARC.svg")],
                ),
                html.A(
                    href="https://uaf.edu/uaf/",
                    children=[html.Img(src=path_prefix + "assets/UAF.svg")],
                ),
            ]
        ),
        ddsih.DangerouslySetInnerHTML(
            f"""
<p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.
<br><a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a></p>
<p class="copyright">Copyright &copy; {current_year} University of Alaska Fairbanks.  All rights reserved.</p>
            """
        ),
    ],
)

layout = html.Div(
    children=[header, about, daily_index, tool_info, credits_section, footer]
)
