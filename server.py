from flask import Flask, make_response, render_template, request
import StockGrapher 
from waitress import serve


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html') 
@app.route('/stock')
def get_Stock():
    tickers = request.args.get('ticker')
    per = request.args.get('periods')
    tickers, period  = StockGrapher.GetInput(tickers, per)
    data = StockGrapher.FetchData(tickers, period)
    clean = StockGrapher.CleanData(data)
    plot_buffer = StockGrapher.save_plot_to_memory(clean)
    
    # Create a Flask response object
    response = make_response(plot_buffer.getvalue())
    
    # Set the appropriate content type and headers
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'inline; filename=plot.png'
    
    return response


                    

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
