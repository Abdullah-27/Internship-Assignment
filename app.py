#import os
import  pandas as pd
import numpy as np
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import urllib
from dash.dependencies import Input, Output, State
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame

#Import dataset from github raw directory

url = "https://github.com/Abdullah-27/Internship-Assignment/blob/cdc558121853356d29720fd8d942ecbfa267e9d1/BQ-Assignment-Data-Analytics.xlsx?raw=true"
df = pd.read_excel(url)

#Data Manipulation

data = df
data["Date"]= pd.to_datetime(df["Date"], yearfirst=True)

Jan =data[data["Date"].dt.month == 1]
Feb = data[data["Date"].dt.month == 2]
March = data[data["Date"].dt.month == 3]
April = data[data["Date"].dt.month == 4]
May = data[data["Date"].dt.month == 5]

Jan_indexed = Jan.set_index(["Item Type", "Item", "Item Sort Order"])
Feb_indexed = Feb.set_index(["Item Type", "Item", "Item Sort Order"])
March_indexed = March.set_index(["Item Type", "Item", "Item Sort Order"])
April_indexed = April.set_index(["Item Type", "Item", "Item Sort Order"])
May_indexed = May.set_index(["Item Type", "Item", "Item Sort Order"])

Table_1 = pd.DataFrame()
Table_1["Apr 20"] = April_indexed["Sales"]
Table_1["Feb 20"] = Feb_indexed["Sales"]
Table_1["Jan 20"] = Jan_indexed["Sales"]
Table_1["Mar 20"] = March_indexed["Sales"]
Table_1["May 20"] = May_indexed["Sales"]

Table_x=Table_1
Table_x = Table_x.reset_index(level=["Item Type", "Item", "Item Sort Order"])

#Creating an Interactive Dashboard

app = dash.Dash(__name__)

server = app.server
# server.secret_key = os.environ.get(‘SECRET_KEY’, ‘my-secret-key’)

Main_Table = Table_x
Fruit_table = Main_Table[Main_Table["Item Type"] == "Fruit"]
Vege_table = Main_Table[Main_Table["Item Type"] == "Vegetable"]

app.layout = html.Div([
    html.Div(id  = "filter-export-container", children=[
        html.Div([
            html.H3("Select Items:", style={"margin":"5px 10px"}),
            html.Br(),
            dcc.Checklist(
                id="filter-container",
                options=[
                    {'label': 'Select all', 'value': 'all'},
                    {'label': 'Fruit', 'value': 'Fruit'},
                    {'label': 'Vegetable', 'value': 'Vegetable'}
                ],
                value =["all", "Fruit", "Vegetable"],
                className="my_container",
                style={"display":"block"},

                inputClassName="input",
                inputStyle={"cursor":"pointer"},

                labelClassName="input",
                labelStyle={"width" : "80%", "display":"block", "background":"Grey", "marginLeft": "10px", "borderRadius":"5px"},
            )

        ]),
        html.Br(),
        html.Div(id = "Export-container",children=[
            html.Div(id="text", children=[html.H3("Press Download to Export current table")],
                    style={"display": "flex", "flexWrap": "wrap"}),
            html.Div([
                html.Button("Export in xlsx", id="save-button",
                            style={"margin": "0px auto", "padding": "5px 10px", "position": "relative"}),
                Download(id="download")])

        ],
        style={"display" : "block", "margin": "20px 10px"}
        )
    ],style={'width': '20%', "float": "left", 'display': 'inline-block',
             "marginTop":"50px",
            "borderStyle": "solid", "borderColor":"Grey","borderRadius":"20px"}),

    html.Div(id="Table", style={'width': '70%',"float":"right", 'display': 'inline-block', "marginTop":"25px",})
])


def filter_table(options_chosen):
    if ("all" in options_chosen) or (("Fruit" in options_chosen) and ("Vegetable" in options_chosen)):
        dff = Main_Table
        return dff
    else:
        if "Fruit" in options_chosen:
            dff =  Fruit_table
            return dff
        elif "Vegetable" in options_chosen:
            dff =  Vege_table
            return dff

@app.callback(
    dash.dependencies.Output(component_id="Table", component_property ="children"),
    [dash.dependencies.Input(component_id="filter-container", component_property ="value")])
def update_table(options_chosen):
    if not options_chosen:
        Error = "Enter Filter Value"
        return Error
    else:
            Filtered_table = filter_table(options_chosen)

    return [dash_table.DataTable(
                id = "Main-table-container",
                data = Filtered_table.to_dict("records"),
                columns=[
                    {"id" : "Item", "name": "Item"},
                    {"id" : "Item Sort Order", "name": "Item Sort Order"},
                    {"id" : "Apr 20", "name": "Apr 20"},
                    {"id" : "Feb 20", "name": "Feb 20"},
                    {"id" : "Jan 20", "name": "Jan 20"},
                    {"id" : "Mar 20", "name": "Mar 20"},
                    {"id" : "May 20", "name": "May 20"}
                ],
                editable = False
    )]

@app.callback(
    dash.dependencies.Output(component_id="download", component_property ='data'),
    [dash.dependencies.Input(component_id="save-button", component_property ="n_clicks")],
    [dash.dependencies.State(component_id='filter-container', component_property ='value')],
    prevent_initial_call=True)
def generate_excel(n_clicks, options_chosen):
    df = filter_table(options_chosen)
#     file =  df.to_excel(index = False, header=True, encoding='utf-8')
    return send_data_frame(df.to_excel, filename="mydf.xlsx")


if __name__ == '__main__':
    app.run_server()
