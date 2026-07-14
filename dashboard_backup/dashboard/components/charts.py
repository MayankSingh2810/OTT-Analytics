import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# GLOBAL THEME
# ==========================================================

BACKGROUND = "#0E1117"
CARD = "#161B22"
TEXT = "#FFFFFF"

NETFLIX = "#E50914"
RED2 = "#FF4B4B"
RED3 = "#FF7373"

BLUE = "#1F77FF"
GREEN = "#00C853"
ORANGE = "#FFA726"
PURPLE = "#7E57C2"

FONT = dict(
    family="Inter",
    size=14,
    color=TEXT,
)


def style(fig, height=420):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

        font=FONT,

        height=height,

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )

    )

    return fig

def device_chart(devices):

    fig = px.bar(

        devices,

        x="device",

        y="total_events",

        color="avg_completion",

        text="total_events",

        color_continuous_scale="Reds",

        title="Streaming by Device"

    )

    fig.update_traces(

        textposition="outside",

        marker_line_width=0,

    )

    style(fig)

    fig.update_layout(

        coloraxis_colorbar=dict(

            title="Completion %"

        )

    )

    return fig

def country_chart(countries):

    fig = px.choropleth(

        countries,

        locations="country",

        locationmode="country names",

        color="total_events",

        hover_name="country",

        color_continuous_scale="Reds",

        title="Global Streaming Activity"

    )

    style(fig, 500)

    fig.update_geos(

        bgcolor=BACKGROUND,

        showframe=False,

        showcoastlines=False,

        projection_type="natural earth"

    )

    return fig

def genre_chart(genres):

    genres = genres.sort_values(

        "views",

        ascending=True

    )

    fig = px.bar(

        genres,

        x="views",

        y="genre",

        orientation="h",

        color="avg_rating",

        text="views",

        title="Most Popular Genres",

        color_continuous_scale="Reds"

    )

    fig.update_traces(

        textposition="outside"

    )

    style(fig)

    return fig

def subscription_chart(subscription):

    fig = px.pie(

        subscription,

        names="subscription_plan",

        values="events",

        hole=.62,

        color_discrete_sequence=[

            NETFLIX,

            RED2,

            RED3

        ]

    )

    style(fig)

    fig.update_layout(

        title="Subscription Distribution"

    )

    return fig

def hourly_chart(hourly):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=hourly["hour"],

            y=hourly["events"],

            mode="lines+markers",

            line=dict(

                color=NETFLIX,

                width=4

            ),

            marker=dict(

                size=8

            ),

            fill="tozeroy"

        )

    )

    style(fig)

    fig.update_layout(

        title="Hourly Streaming Activity",

        xaxis_title="Hour",

        yaxis_title="Events"

    )

    return fig

# ==========================================================
# NETWORK QUALITY
# ==========================================================

def network_chart(network):

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=network["avg_buffer_ms"],

            theta=network["network_type"],

            fill="toself",

            line=dict(
                color=NETFLIX,
                width=3
            ),

            fillcolor="rgba(229,9,20,0.35)"
        )

    )

    style(fig)

    fig.update_layout(

        polar=dict(

            bgcolor=BACKGROUND,

            radialaxis=dict(

                visible=True,

                gridcolor="#444"

            ),

            angularaxis=dict(

                gridcolor="#444"

            )

        ),

        title="Network Quality"

    )

    return fig


# ==========================================================
# VIDEO QUALITY
# ==========================================================

def quality_chart(quality):

    fig = px.treemap(

        quality,

        path=["video_quality"],

        values="events",

        color="avg_buffer_ms",

        color_continuous_scale="Reds",

        title="Streaming Quality Distribution"

    )

    style(fig, 500)

    return fig


# ==========================================================
# COMPLETION GAUGE
# ==========================================================

def completion_gauge(summary):

    completion = float(summary["avg_completion"].iloc[0])

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=completion,

            number={

                "suffix": "%",

                "font": dict(

                    size=48,

                    color="white"

                )

            },

            title={

                "text": "Average Completion Rate"

            },

            gauge={

                "axis": {

                    "range": [0,100]

                },

                "bar": {

                    "color": NETFLIX

                },

                "steps":[

                    {"range":[0,40],"color":"#2A2A2A"},

                    {"range":[40,70],"color":"#444444"},

                    {"range":[70,100],"color":"#666666"}

                ]

            }

        )

    )

    style(fig,350)

    return fig


# ==========================================================
# TOP CONTENT
# ==========================================================

def top_content_chart(content):

    top = (

        content

        .sort_values(

            "views",

            ascending=False

        )

        .head(10)

        .sort_values(

            "views"

        )

    )

    fig = px.bar(

        top,

        x="views",

        y="title",

        orientation="h",

        text="views",

        color="views",

        color_continuous_scale="Reds",

        title="Netflix Top 10 Content"

    )

    fig.update_traces(

        textposition="outside"

    )

    style(fig,550)

    return fig


# ==========================================================
# COMPLETION VS RATING
# ==========================================================

def completion_rating_chart(genres):

    fig = px.scatter(

        genres,

        x="completion",

        y="avg_rating",

        size="views",

        color="genre",

        hover_name="genre",

        title="Completion vs Viewer Rating"

    )

    style(fig)

    return fig


# ==========================================================
# DEVICE COMPLETION
# ==========================================================

def device_completion_chart(devices):

    fig = px.bar(

        devices,

        x="device",

        y="avg_completion",

        color="avg_completion",

        color_continuous_scale="Reds",

        title="Completion by Device"

    )

    style(fig)

    return fig


# ==========================================================
# COUNTRY BUFFERING
# ==========================================================

def buffering_chart(countries):

    fig = px.bar(

        countries,

        x="country",

        y="avg_buffer_ms",

        color="avg_buffer_ms",

        color_continuous_scale="Turbo",

        title="Average Buffering Time"

    )

    style(fig)

    return fig


# ==========================================================
# SUBSCRIPTION WATCH TIME
# ==========================================================

def subscription_watchtime(subscription):

    fig = px.bar(

        subscription,

        x="subscription_plan",

        y="avg_watch_seconds",

        color="subscription_plan",

        title="Average Watch Time by Plan"

    )

    style(fig)

    return fig