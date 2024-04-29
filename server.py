
from flask import Flask, make_response, render_template, request, jsonify, redirect, url_for
from PIL import Image
import StockGrapher 
from waitress import serve
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html') 
@app.route('/stock', methods=['GET', 'POST'])
def get_Stock():
    image_url = None
    if request.method == 'POST':
        ticker = request.form['ticker']
        period = request.form['period']
        # Redirect to the /stockimages route with the selected ticker and period
        return redirect(url_for('stockimages.html', ticker=ticker, period=period))
    return render_template('stock.html', image_url=image_url)
    

@app.route('/stockimages')
def get_image():
    tickers = request.args.get('ticker')
    per = request.args.get('periods')
    tickers, period  = StockGrapher.GetInput(tickers, per)
    data = StockGrapher.FetchData(tickers, period)
    clean = StockGrapher.CleanData(data)
    fig = StockGrapher.CreateVis(clean)
    plot_buffer = BytesIO()
    fig.savefig(plot_buffer, format='png')
    plt.close(fig)

    # Encode the plot as base64
    plot_encoded = base64.b64encode(plot_buffer.getvalue()).decode('utf-8')

    return render_template('stockimages.html', image_url=plot_encoded, ticker=tickers)

    

                    

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
