# pylint: disable=C0103
"""
Common shared text strings, formatting defaults and lookup tables.
"""

import os
import plotly.io as pio

# Core page components
title = "Alaska Statewide Temperature Index"
url = "http://accap.uaf.edu/tools/statewide-temperature-index"
preview = "http://accap.uaf.edu/tools/statewide-temperature-index/assets/preview.png"
description = (
    "See if it's unusually hot or cold relative to historical normals for Alaska."
)
index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        <script async defer 
            data-do-not-track="true" 
            data-website-id="3904e4d3-ac89-47f3-8220-4576c671acd5"
            data-domains="accap.uaf.edu"
            src="https://umami.snap.uaf.edu/script.js"
        ></script>        
        {{%metas%}}
        <title>{{%title%}}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Schema.org markup for Google+ -->
        <meta itemprop="name" content="{title}">
        <meta itemprop="description" content="{description}">
        <meta itemprop="image" content="{preview}">

        <!-- Twitter Card data -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="@SNAPandACCAP">
        <meta name="twitter:title" content="{title}">
        <meta name="twitter:description" content="{description}">
        <meta name="twitter:creator" content="@SNAPandACCAP">
        <!-- Twitter summary card with large image must be at least 280x150px -->
        <meta name="twitter:image:src" content="{preview}">

        <!-- Open Graph data -->
        <meta property="og:title" content="{title}" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{url}" />
        <meta property="og:image" content="{preview}" />
        <meta property="og:description" content="{description}" />
        <meta property="og:site_name" content="{title}" />

        <link rel="alternate" hreflang="en" href="{url}" />
        <link rel="canonical" href="{url}"/>
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# Plotly format template
plotly_template = pio.templates["simple_white"]
axis_configs = {
    "automargin": True,
    "showgrid": False,
    "showline": False,
    "ticks": "",
    "title": {"standoff": 0},
    "zeroline": False,
    "fixedrange": True,
}
xaxis_config = {**axis_configs, **{"tickformat": "%B %-d, %Y"}}
plotly_template.layout.xaxis = xaxis_config
plotly_template.layout.yaxis = axis_configs

# Used to make the chart exports nice
fig_download_configs = dict(
    filename="Statewide_Temperature_Index", width="1000", height="650", scale=2
)
fig_configs = dict(
    displayModeBar=True,
    showSendToCloud=False,
    toImageButtonOptions=fig_download_configs,
    modeBarButtonsToRemove=[
        "zoom2d",
        "pan2d",
        "select2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "autoScale2d",
        "resetScale2d",
        "hoverClosestCartesian",
        "hoverCompareCartesian",
        "hoverClosestPie",
        "hoverClosest3d",
        "hoverClosestGl2d",
        "hoverClosestGeo",
        "toggleHover",
        "toggleSpikelines",
    ],
    displaylogo=False,
)

# Colors to reference
colors = ["#405bfe", "#ff3d00"]  # cold  # hot
