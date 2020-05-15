# pylint: disable=C0103,C0301
"""
GUI for app
"""

import os
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as ddsih
import luts
import data
import charts

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
          <a class="button is-primary">
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
<p class="camera-icon">Click the <span>
<svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg>
</span> icon in the upper&ndash;right of each chart to download it.</p>
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
        ddsih.DangerouslySetInnerHTML(
            """
<div class="content is-size-5">
<p>This chart shows today&rsquo;s Alaska temperatures compared to daily normal temperatures 1981&ndash;2010.</p>
<p>An index value of &plus;X means the day is warmer than X percent of all Above Normal days.</p>
<p>An index value of &minus;X means the day is colder than X percent of all Below Normal days.</p>
<p>The black line indicates the 30-day average.</p>
</div>
    """
        ),
        dcc.Graph(id="daily-index", figure=charts.daily_index, config=luts.fig_configs),
    ],
    section_classes="graph",
)

data = wrap_in_section(
    [
        ddsih.DangerouslySetInnerHTML(
            f"""
<p>Index based on 1981&ndash;2010 daily normals and standard deviations of 25 stations.  A value of +1 means that the day is warmer than 10&#37; of all Above Normal days.  A value of +8 means that the day is warmer than 80&#37; of all Above Normal days, and so on.  The opposite is true for negative numbers.</p>
<p>Data provided by the the <a href="http://www.rcc-acis.org">Applied Climate Information System (ACIS)</a>.</p>
<p>Placeholder, credits & citation.</p>
            """
        )
    ],
    div_classes="content is-size-5",
)

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
                    href="https://uaf.edu/uaf/",
                    children=[html.Img(src=path_prefix + "assets/UAF.svg")],
                ),
            ]
        ),
        ddsih.DangerouslySetInnerHTML(
            """
<p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.
<br><a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a></p>
            """
        ),
    ],
)

layout = html.Div(children=[header, about, daily_index, data, footer])
