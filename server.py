import matplotlib.pyplot as plt
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


@app.route('/stock', methods=['GET','POST'])
def get_Stock():

    tickers = request.args.get('ticker')
    per = request.args.get('periods')
    tickers, period  = StockGrapher.GetInput(tickers, per)
    result = []
    for t in tickers:
        try:
            stats = StockGrapher.get_stats(t)
            result.append(stats)
        except Exception as e:
            print(f"Error retrieving stats for {t}: {e}")
            result.append("no data available")
    for r in result:
        clean_html = StockGrapher.remove_newlines(r)
    # Redirect to the /stockimages route with the selected ticker and period and stats
    return render_template('statsimages.html', ticker=tickers ,period=period, result=clean_html)

    

@app.route('/statsimages')
def get_image():
    tickers = request.args.get('ticker')
    per = request.args.get('period')
    
    tickers, period  = StockGrapher.GetInput(tickers, per)
    data = StockGrapher.FetchData(tickers, period)
    clean = StockGrapher.CleanData(data)
    plot_buffer = StockGrapher.save_plot_to_memory(clean)
    plt.close()
    response = make_response(plot_buffer.getvalue())
    # Set the appropriate content type and headers
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'inline; filename=plot.png'
    return response

    

                    

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=8000)
    # host='0.0.0.0', port=8000
