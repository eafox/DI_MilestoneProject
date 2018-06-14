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

app.vars={}
@app.route('/',methods=['GET','POST'])
def index():
	in_vars = {}
	if request.method == 'POST':
		app.vars['tickerCode']=request.form['ht_tickerCode']
		app.vars['startDate']=request.form['ht_startDate']
		app.vars['endDate']=request.form['ht_endDate']
		
		app.vars['valSets']=request.form.getlist('val-sets')
		
		tempDF = requestData(app.vars)
		tempPlot = plotRequest(tempDF, in_vars)
		
		script, div = components(tempPlot)		
		return render_template('plot.html',tempScript=script,tempDiv=div)
		
	else:
		return render_template('index.html')


#####################
# GET DATA FROM API #
#####################

def requestData(in_params):
	apiKey=os.environ.get('QUANDL_KEY')

	req_params = {"api_key": apiKey, "ticker": in_params['tickerCode'], 
	"qopts.columns": "ticker,date,open,close,adj_open,adj_close", 
	"date.gte": in_params['startDate'], "date.lte": in_params['endDate']} 
	data_raw = requests.get("https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json", params=req_params) #print(data_raw.status_code)


	data_table=data_raw.json()["datatable"]

	data_col=[col['name'] for col in data_table['columns']]
	panda_table=pd.DataFrame(data_table['data'],columns=data_col)
	panda_table['date']=pd.to_datetime(panda_table['date'], format='%Y-%m-%d')
	
	return(panda_table)

###################
# PLOT WITH BOKEH #
###################
def plotRequest(df, in_params):
	source = ColumnDataSource(data=df)

	stockPlot = figure(title= "Stock Prices from Quandl WIKI", 
	plot_height=650, plot_width=800,
	x_axis_label='Date', x_axis_type='datetime',
	y_axis_label='Value (in USD)',
	tools="reset,undo,redo,pan,tap,box_zoom,box_select,hover")

	if 'ht_open' in app.vars['valSets'] or not app.vars['valSets']:
		stockPlot.line(x='date',y='open',source=source,legend="Opening Price",line_width=2,color="darkgreen")
	if 'ht_close' in app.vars['valSets'] or not app.vars['valSets']:
		stockPlot.line(x='date',y='close',source=source,legend="Closing Price",line_width=2,color="darkred")
	if 'ht_open-a' in app.vars['valSets'] or not app.vars['valSets']:
		stockPlot.line(x='date',y='adj_open',source=source,legend="Opening Price (adjusted)",line_width=2,color="limegreen")
	if 'ht_close-a' in app.vars['valSets'] or not app.vars['valSets']:
		stockPlot.line(x='date',y='adj_close',source=source,legend="Closing Price (adjusted)",line_width=2,color="red")
	
	return(stockPlot)

###############
# WRAPPING UP #
###############

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
 

