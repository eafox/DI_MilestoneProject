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

stockCode=api_key=os.environ.get('QUANDL_KEY')
api_key=-"z5FzzicL2ERpgaJrzxs"
startDate="2017-01-01"
endDate="2018-01-01"

data_raw = "https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?api_key=%s&start_date=%s&end_date=%s" % (stockCode, api_key, startDate, endDate)



