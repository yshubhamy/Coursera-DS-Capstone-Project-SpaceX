import pandas as pd
from dash import dash, dcc, html, Input, Output
import plotly.express as px


spacex_df = pd.read_csv("dataset_3.csv")
print(spacex_df.columns)
max_payload = spacex_df["PayloadMass"].max()
min_payload = spacex_df["PayloadMass"].min()


app = dash.Dash(__name__)
server = app.server

uniquelaunchsites = spacex_df["LaunchSite"].unique().tolist()
lsites = []
lsites.append({"label": "All Sites", "value": "All Sites"})
for site in uniquelaunchsites:
    lsites.append({"label": site, "value": site})


app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        dcc.Dropdown(
            id="site_dropdown",
            options=lsites,
            placeholder="Select a LaunchSite here",
            searchable=True,
            value="All Sites",
        ),
        html.Br(),
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id="payload_slider",
            min=0,
            max=10000,
            step=1000,
            marks={
                0: "0 kg",
                1000: "1000 kg",
                2000: "2000 kg",
                3000: "3000 kg",
                4000: "4000 kg",
                5000: "5000 kg",
                6000: "6000 kg",
                7000: "7000 kg",
                8000: "8000 kg",
                9000: "9000 kg",
                10000: "10000 kg",
            },
            value=[min_payload, max_payload],
        ),
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    [Input(component_id="site_dropdown", component_property="value")],
)
def update_graph(site_dropdown):
    if site_dropdown == "All Sites":
        df = spacex_df[spacex_df["Class"] == 1]
        fig = px.pie(
            df,
            names="LaunchSite",
            hole=0.3,
            title="Total Success Launches By all sites",
        )
    else:
        df = spacex_df.loc[spacex_df["LaunchSite"] == site_dropdown]
        fig = px.pie(
            df,
            names="Class",
            hole=0.3,
            title="Total Success Launches for site " + site_dropdown,
        )
    return fig


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site_dropdown", component_property="value"),
        Input(component_id="payload_slider", component_property="value"),
    ],
)
def update_scattergraph(site_dropdown, payload_slider):
    if site_dropdown == "All Sites":
        low, high = payload_slider
        df = spacex_df
        mask = (df["PayloadMass"] > low) & (df["PayloadMass"] < high)
        fig = px.scatter(
            df[mask],
            x="PayloadMass",
            y="Class",
            color="BoosterVersion",
            size="PayloadMass",
            hover_data=["PayloadMass"],
        )
    else:
        low, high = payload_slider
        df = spacex_df.loc[spacex_df["LaunchSite"] == site_dropdown]
        mask = (df["PayloadMass"] > low) & (df["PayloadMass"] < high)
        fig = px.scatter(
            df[mask],
            x="PayloadMass",
            y="Class",
            color="BoosterVersion",
            size="PayloadMass",
            hover_data=["PayloadMass"],
        )
    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
