#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 06:12:13 2022

@author: kaleb
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_table
from dash.exceptions import PreventUpdate
import sqlite3

#%%
app = dash.Dash()
con = sqlite3.connect("scenarios.sqlite")
df = pd.read_sql_query("SELECT scenario_name from scenarios", con)

app.layout = html.Div([
    html.H1([], style = {'backgroundColor': 'rgb(0,123,255)', 'width': '100%', 'height': 40, 'marginTop': '0px'}),
    html.Div([
        html.Div([
            html.Div([        
                html.Div(['Return of Investment Inputs:'], style = {'color': 'rgb(0,123,255)', 'fontSize': 25, 'fontFamily': 'Arial'}),
                html.Table([
                    html.Tr([html.Td("Scenario Name:", className = 'lined', style = {'width': '50%'}),
                             html.Td(dcc.Input(id = 'scenarioName', type = 'string', style = {'fontSize': 15, 'fontFamily': 'Arial', 'float': 'right'}))]),
                    
                    html.Tr([html.Td("Total Hits:", className = 'lined', style = {'width': '50%'}),
                             html.Td(dcc.Input(id = 'totalHits', type = 'number', value = 1000000, style = {'fontSize': 15, 'fontFamily': 'Arial', 'float': 'right'}))]),
                    
                    html.Tr([html.Td("Conversion Rate:", className = 'lined', style = {'width': '50%'}),
                             html.Td(dcc.Input(id = 'conversionRate', type = 'number', value = 60, style = {'fontSize': 15, 'fontFamily': 'Arial', 'float': 'right'}))]),
                    
                    html.Tr([html.Td("Revenue Per Purchase (PhP):", className = 'lined', style = {'width': '50%'}),
                             html.Td(dcc.Input(id = 'revenuePerPurchase', type = 'number', value = 50, style = {'fontSize': 15, 'fontFamily': 'Arial', 'float': 'right'}))]),
                    
                    html.Tr([html.Td("Number of Times of Purchase per Converted User Per Year:", className = 'lined', style = {'width': '50%'}),
                             html.Td(dcc.Input(id = 'ntpcupy', type = 'number', value = 2, style = {'fontSize': 15, 'fontFamily': 'Arial', 'float': 'right'}))]),
                    
                    html.Tr([html.Td("Total Cost of Sampling (PhP):", className = 'lined', style = {'width': '50%'}),
                             html.Td(dcc.Input(id = 'samplingCost', type = 'number', value = 25000000, style = {'fontSize': 15, 'fontFamily': 'Arial', 'float': 'right'}))]),
                    
                    html.Tr([html.Td("% of Potential Revenue You are Willing to allocate for sampling:", className = 'lined', style = {'width': '50%'}),
                             html.Td(dcc.Input(id = 'potentialRevenue', type = 'number', value = 50, style = {'fontSize': 15, 'fontFamily': 'Arial', 'float': 'right'}))])
                    ])
            ], style = {'width': '100%'}),
            html.Hr(),
            html.Button(id = 'submitButton', children = 'Calculate ROI', n_clicks = 0, className = 'btn btn-primary btn',
                        style = {'fontSize': '15px', 'color': 'white', 'backgroundColor': 'rgb(0,123,255)', 'float': 'left', 'borderRadius': '5px', 'border': '5px', 'padding': '5px'}),
            html.Br(),
            html.Br(),
            html.Hr(),
            html.Div([
                html.Table([
                    html.Tr([html.Td("Select Scenario:", style = {'fontSize': 15, 'fontFamily': 'Arial', 'float': 'left'}),
                             html.Td(dcc.Dropdown(id = 'selected_scenario', options = []), style = {'width' : '60%'})]),
                    
                    html.Tr([html.Td(html.Button(id = 'saveButton', children = 'Save Settings', n_clicks = 0, className = 'btn btn-primary btn',
                                                 style = {'fontSize': '15px', 'color': 'white', 'backgroundColor': 'rgb(0,123,255)', 'float': 'left', 'borderRadius': '5px', 'border': '5px', 'padding': '5px'})),
                             html.Td(dcc.Checklist(id = "mode", options=[{'label': 'Edit Mode', 'value': 1}], value=[], labelStyle={'display': 'inline-block'}))]),
                    
                    html.Button(id = 'deleteScenario', children = 'Delete This Scenario', n_clicks = 0, className = 'btn btn-primary btn',
                                style = {'fontSize': '15px', 'color': 'white', 'backgroundColor': 'rgb(0,123,255)', 'float': 'left', 'borderRadius': '5px', 'border': '5px', 'padding': '5px'}),
                    html.Div([dcc.Input(id = 'submitmode')], style={'display':'none'})])])
            ], style = {'width': '30%', 'display': 'inline-block', 'float': 'left', 'marginTop': '0px'}),
        
        html.Div([
            html.Div(['Investment/Income Breakdown'], style = {'color': 'rgb(0,123,255)', 'textAlign': 'center', 'fontSize': 25, 'fontFamily': 'Arial'}),
            dcc.Graph(id = 'donut'),
            
            html.Div([
                html.Div(['ROI Parameters Computed:'], style = {'color': 'rgb(0,123,255)', 'textAlign': 'center', 'fontSize': 25, 'fontFamily': 'Arial'}),
                html.Table([
                    html.Tr([html.Td("Total Potential Revenue:", style = {'border': '1px solid black'}), html.Td(id = 'totalPotentialRevenue', style = {'textAlign': 'right', 'border': '1px solid black'})]),
                    html.Tr([html.Td("Unconverted Opportunity Revenue:", style = {'border': '1px solid black'}), html.Td(id = 'unconvertedOpportunityRevenue', style = {'textAlign': 'right', 'border': '1px solid black'})]),
                    html.Tr([html.Td("Converted Revenue:", style = {'border': '1px solid black'}), html.Td(id = 'convertedRevenue', style = {'textAlign': 'right', 'border': '1px solid black'})]),
                    html.Tr([html.Td("Maximum Allowable Spend:", style = {'border': '1px solid black'}), html.Td(id = 'maximumAllowableSpend', style = {'textAlign': 'right', 'border': '1px solid black'})]),
                    html.Tr([html.Td("Maximum Spend per Hit:", style = {'border': '1px solid black'}), html.Td(id = 'maximumSpendperHit', style = {'textAlign': 'right', 'border': '1px solid black'})])
                ], style = {'width': '100%'})
            ], style = {'fontSize': 15, 'fontFamily': 'Arial'}),
            
            html.Div([
                html.Div(['Estimated Net Profit from Sampling:'], style = {'color': 'rgb(0,123,255)', 'textAlign': 'center', 'fontSize': 25, 'fontFamily': 'Arial'}),
                html.Table([
                    html.Tr([html.Td("Net Profit", style = {'border': '1px solid black'}), html.Td(id = 'netProfit', style = {'textAlign': 'right', 'border': '1px solid black', 'border-collapse': 'collapse'})])
                ], style = {'width': '100%'})
            ], style = {'fontSize': 15, 'fontFamily': 'Arial', 'marginTop': '20px'})
        ], style = {'width': '35%', 'display': 'inline-block', 'float': 'middle', 'marginTop': '0px'}),
        
        html.Div([
            html.Div(['Waterfall Chart'], style = {'color': 'rgb(0,123,255)', 'textAlign': 'center', 'fontSize': 25, 'fontFamily': 'Arial'}), 
            dcc.Graph(id = 'waterfall')
        ], style = {'width': '35%', 'display': 'inline-block', 'float': 'right', 'marginTop': '0px'})
    ]),
    
    html.Div([
        dash_table.DataTable(id = 'firstdatatable')
    ])
])

@app.callback(
    [Output('totalPotentialRevenue', 'children'),
     Output('unconvertedOpportunityRevenue', 'children'),
     Output('convertedRevenue', 'children'),
     Output('maximumAllowableSpend', 'children'),
     Output('maximumSpendperHit', 'children'),
     Output('netProfit', 'children'),
     Output('donut', 'figure'),
     Output('waterfall', 'figure')],
    [Input('submitButton', 'n_clicks')],
    [State('totalHits', 'value'),
     State('conversionRate', 'value'),
     State('revenuePerPurchase', 'value'),
     State('ntpcupy', 'value'),
     State('samplingCost', 'value'),
     State('potentialRevenue', 'value')])

def caculateROI(n_clicks, totalHits, conversionRate, revenuePerPurchase, ntpcupy, samplingCost, potentialRevenue):
    if n_clicks > 0:
        totalPotentialRevenue = totalHits * revenuePerPurchase * ntpcupy
        unconvertedOpportunityRevenue = (1 - conversionRate/100) * totalPotentialRevenue
        convertedRevenue = (conversionRate/100) * totalPotentialRevenue
        netProfit = convertedRevenue - samplingCost
        netProfitNotforSampling = (1 - potentialRevenue/100) * netProfit
        maximumAllowableSpend = potentialRevenue/100 * netProfit
        maximumSpendperHit = maximumAllowableSpend/totalHits
        
        donut_labels = ['Unconverted Revenue, PhP', 'Net Profit Not For Sampling, PhP', 'Max Allowable Spend, PhP', 'Sampling Cost, Php']
        donut_values = [unconvertedOpportunityRevenue, netProfitNotforSampling, maximumAllowableSpend, samplingCost]
        donut_colors = ['rgb(242,217,187)','rgb(255,59,60)','rgb(134,169,189)','rgb(44,82,103)']
    
        donut_fig = go.Figure(data = go.Pie(labels = donut_labels, values = donut_values, hole = 0.4, marker = dict(colors = donut_colors, line = dict(color = '#000000', width = 2)),
                                                      textinfo='label+value', textposition = 'outside', showlegend = False))
    
        waterfall_fig = go.Figure(go.Waterfall(orientation = "v",
                                           measure = ["relative", "relative", "total", "relative", "total", "relative", "total"],
                                           x = ["Total Potential Annual Revenue", "Unconverted Opportunity Revenue", "Converted Revenue", "Sampling Cost", "Net Profit", "Net Profit Not for Sampling", "Max Allowable Spend"],
                                           y = [totalPotentialRevenue, -unconvertedOpportunityRevenue, convertedRevenue, -samplingCost, netProfit, -netProfitNotforSampling, maximumAllowableSpend],
                                           decreasing = {'marker':{'color':'rgb(255, 59, 60, 0.7)'}},
                                           increasing = {'marker':{'color':'rgb(44, 82, 103, 0.7)'}},
                                           totals = {'marker':{'color':'rgb(44, 82, 103, 0.7)'}},
                                           connector = {'mode':'between', 'line':{'width': 0, 'color':'rgb(0, 0, 0)', 'dash': 'solid'}}))
    
        waterfall_fig.update_layout(xaxis_title = "ROI Parameters")
    
        return [totalPotentialRevenue, unconvertedOpportunityRevenue, convertedRevenue, maximumAllowableSpend, maximumSpendperHit, netProfit, donut_fig, waterfall_fig]

@app.callback(
    [Output('firstdatatable', 'data'),
     Output('firstdatatable', 'columns'),
     Output('submitmode','value')],
    [Input('submitButton', 'n_clicks'),
     Input('saveButton', 'n_clicks'),
     Input('deleteScenario', 'n_clicks'),
     Input('mode', 'value')],
    [State('scenarioName', 'value'),
     State('totalHits', 'value'),
     State('conversionRate', 'value'),
     State('revenuePerPurchase', 'value'),
     State('ntpcupy', 'value'),
     State('samplingCost', 'value'),
     State('potentialRevenue', 'value'),
     State('selected_scenario', 'value'),
     State('firstdatatable', 'data')])

def output(submit_button, save_button, delete_button, mode, scenario_name, total_hits, conversion_rate, revenue_per_purchase, ntpcuy, total_sampling_cost, potential_revenue, selected_scenario, dashtabledata):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid == "submitButton":
           sql = "SELECT * FROM scenarios"
           df = querydatafromdatabase(sql,[],["scenario_name", "total_hits", "conversion_rate", "revenue_per_purchase", "ntpcuy", "total_sampling_cost", "potential_revenue"])
           columns=[{"name": i, "id": i} for i in df.columns]
           data=df.to_dict("rows")
           return [data, columns, 2]
       elif eventid == "saveButton":
           if 1 not in mode: #add mode
               if not scenario_name or not total_hits or not conversion_rate or not revenue_per_purchase or not ntpcuy or not total_sampling_cost or not potential_revenue:
                   pass
               else:
                   #sql = "SELECT max(id) as scenario_id FROM scnearios"
                   #df = querydatafromdatabase(sql, [], ["scenario_id"])
                   #scenario_id = int(df['scenario_id'][0])+1
                   sqlinsert = "INSERT INTO scenarios(scenario_name, total_hits, conversion_rate, revenue_per_purchase, ntpcuy, total_sampling_cost, potential_revenue) VALUES(?, ?, ?, ?, ?, ?, ?)"
                   modifydatabase(sqlinsert, [scenario_name, total_hits, conversion_rate, revenue_per_purchase, ntpcuy, total_sampling_cost, potential_revenue])
                   sql = "SELECT * FROM scenarios"
                   df = querydatafromdatabase(sql,[],["scenario_name", "total_hits", "conversion_rate", "revenue_per_purchase", "ntpcuy", "total_sampling_cost", "potential_revenue"])
                   columns = [{"name": i, "id": i} for i in df.columns]
                   data=df.to_dict("rows")      
                   return [data, columns, 0]
           else:
               scenario_name = dashtabledata[selected_scenario[0]]['scenario_name']
               sqlinsert = "UPDATE scenarios SET total_hits = ?, conversion_rate = ?, revenue_per_purchase = ?, ntpcuy = ?, total_sampling_cost = ?, potential_revenue = ? WHERE scenario_name = ?"
               modifydatabase(sqlinsert, [total_hits, conversion_rate, revenue_per_purchase, ntpcuy, total_sampling_cost, potential_revenue])
               sql = "SELECT * FROM scenarios"
               df = querydatafromdatabase(sql, [], ["total_hits", "conversion_rate", "revenue_per_purchase", "ntpcuy", "total_sampling_cost", "potential_revenue"])
               columns = [{"name": i, "id": i} for i in df.columns]
               data = df.to_dict("rows")      
               return [data, columns, 0]
               
       elif eventid == "deleteScenario":
           scenario_name = dashtabledata[selected_scenario[0]]['scenario_name']
           sqlinsert = "DELETE FROM scenarios WHERE scenario_name = ?"
           modifydatabase(sqlinsert, [scenario_name, total_hits, conversion_rate, revenue_per_purchase, ntpcuy, total_sampling_cost, potential_revenue])
           sql = "SELECT * FROM scenarios"
           df = querydatafromdatabase(sql, [], ["scenario_name", "total_hits", "conversion_rate", "revenue_per_purchase", "ntpcuy", "total_sampling_cost", "potential_revenue"])
           columns = [{"name": i, "id": i} for i in df.columns]
           data = df.to_dict("rows")      
           return [data, columns, 0]
        
       elif eventid == "mode":
           sql = "SELECT * FROM scenarios"
           df = querydatafromdatabase(sql, [], ["scenario_name", "total_hits", "conversion_rate", "revenue_per_purchase", "ntpcuy", "total_sampling_cost", "potential_revenue"])
           columns = [{"name": i, "id": i} for i in df.columns]
           data = df.to_dict("rows")          
           return [data, columns, 2]
   else:
      raise PreventUpdate


@app.callback(
    [Output('scenario_name', 'value'),
     Output('total_hits', 'value'),
     Output('conversion_rate', 'value'),
     Output('revenue_per_purchase', 'value'),
     Output('ntpcuy', 'value'),
     Output('total_sampling_cost', 'value'),
     Output('potential_revenue', 'value')],
    [Input('submitmode', 'value'),
     Input('selected_scenario', 'value')],
    [State('scenario_name', 'value'),
     State('total_hits', 'value'),
     State('conversion_rate', 'value'),
     State('revenue_per_purchase', 'value'),
     State('ntpcuy', 'value'),
     State('total_sampling_cost', 'value'),
     State('potential_revenue', 'value'),
     State('firstdatatable', 'data')])

def clear(submitmode, selected_scenario, scenario_name, total_hits, conversion_rate, revenue_per_purchase, ntpcuy, total_sampling_cost, potential_revenue, data):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid == "submitmode" :
          if submitmode == 0:
              update_options(selected_scenario)
              return ["", "", "", "", "", "", ""]   
          elif submitmode == 1:
              update_options(selected_scenario)
              return [scenario_name, total_hits, conversion_rate, revenue_per_purchase, ntpcuy, total_sampling_cost, potential_revenue]
          elif submitmode == 2:
              if selected_scenario:
                update_options(selected_scenario)
                sql = "SELECT * FROM scenarios WHERE scenario_name = ?"
                df = querydatafromdatabase(sql, [data[selected_scenario[0]]['scenario_name']], ["scenario_name", "total_hits", "conversion_rate", "revenue_per_purchase", "ntpcuy", "total_sampling_cost", "potential_revenue"])
                return [df['scenario_name'][0], df['total_hits'][0], df['conversion_rate'][0], df['revenue_per_purchase'][0], df['ntpcuy'][0], df['total_sampling_cost'][0], df['potential_revenue'][0]]          
              else:
                return ["", "", "", "", "", "", ""]   
       elif eventid == "selected_scenario":
           if selected_scenario:
               update_options(selected_scenario)
               sql = "SELECT * FROM scenarios WHERE scenario_name =?"
               df = querydatafromdatabase(sql,[data[selected_scenario[0]]['scenario_name']],["scenario_name", "total_hits", "conversion_rate", "revenue_per_purchase", "ntpcuy", "total_sampling_cost", "potential_revenue"])              
               return [df['scenario_name'][0], df['total_hits'][0], df['conversion_rate'][0], df['revenue_per_purchase'][0], df['ntpcuy'][0], df['total_sampling_cost'][0], df['potential_revenue'][0]]         
           else:
               update_options(selected_scenario)
               return ["", "", "", "", "", "", ""]      
   else:
      raise PreventUpdate

def querydatafromdatabase(sql, values, dbcolumns):
    db = sqlite3.connect('scenarios.sqlite')
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns = dbcolumns)
    db.close()
    return rows

def modifydatabase(sqlcommand, values):
    db = sqlite3.connect('scenarios.sqlite')
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    db.commit()
    db.close()
    
    
@app.callback(
    Output('selected_scenario', 'options'),
    [Input('selected_scenario', 'value')]
)
def group_dropdown_BuildOptions(df_for_dropdown):  
    return data_group_options_build()

def update_options(options):
    if options:
        con = sqlite3.connect("scenarios.sqlite")
        df = pd.read_sql_query("SELECT scenario_name from scenarios", con)
        lst = [{'label': i, 'value': i} for i in df['scenario_name'].tolist()]
        return lst
    else:
        return []

def data_group_options_build():
    OptionList = [{'label': i, 'value': i} for i in df['scenario_name'].tolist()]
    return OptionList

    
if __name__ == '__main__':
    app.run_server()
    