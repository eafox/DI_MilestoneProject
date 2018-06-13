from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

startDate="2017-01-01"
endDate="2017-12-31"
#apiKey=os.environ.get('QUANDL_KEY')

datelist = pd.period_range(startDate,endDate).tolist()
req_params = {"api_key": "-z5FzzicL2ERpgaJrzxs", "ticker": "AAPL" , "qopts.columns": "ticker,date,open,close,adj_open,adj_close"} #, "date": datelist
data_raw = requests.get("https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json", params=req_params)

print(data_raw.status_code)
raw_table=data_raw.json()
data_table=raw_table["datatable"]


data_col=[col['name'] for col in data_table['columns']]
panda_table=pd.DataFrame(data_table['data'],columns=data_col)
