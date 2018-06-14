###########
# IMPORTS #
###########

from flask import Flask, render_template, request, redirect
import os
import requests
import pandas as pd
import simplejson as json
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.embed import components

###################
# FLASK FRAMEWORK #
###################

app = Flask(__name__)

@app.route('/')
def index():
	in_params = {}
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

#####################
# GET DATA FROM API #
#####################

def requestData(in_params):
	apiKey="-z5FzzicL2ERpgaJrzxs" #os.environ.get('QUANDL_KEY')
	startDate="2017-01-01" #in_params['startDate']
	endDate="2017-12-31" #in_params['endDate']

	req_params = {"api_key": apiKey, "ticker": "AAPL" , "qopts.columns": "ticker,date,open,close,adj_open,adj_close", "date.gte": startDate , "date.lte": endDate} 
	data_raw = requests.get("https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json", params=req_params) #print(data_raw.status_code)


	data_table=data_raw.json()["datatable"]

	data_col=[col['name'] for col in data_table['columns']]
	panda_table=pd.DataFrame(data_table['data'],columns=data_col)
	panda_table['date']=pd.to_datetime(panda_table['date'], format='%Y-%m-%d')

###################
# PLOT WITH BOKEH #
###################
def plotRequest(df, in_params):
	source = ColumnDataSource(data=panda_table)

	p = figure(title= "Stock Prices from Quandl WIKI", 
	plot_height=650, plot_width=800,
	x_axis_label='Date', x_axis_type='datetime',
	y_axis_label='Value (in USD)',
	tools="reset,undo,redo,pan,tap,box_zoom,box_select,hover")

	p.line(x='date',y='open',source=source,legend="Opening Price",line_width=2,color="darkgreen")
	p.line(x='date',y='close',source=source,legend="Closing Price",line_width=2,color="darkred")
	p.line(x='date',y='adj_open',source=source,legend="Opening Price (adjusted)",line_width=2,color="limegreen")
	p.line(x='date',y='adj_close',source=source,legend="Closing Price (adjusted)",line_width=2,color="red")


