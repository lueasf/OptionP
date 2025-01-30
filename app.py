from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use('Agg')  # Backend non graphique
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
from bs_model import *
from report_generator import generate_pdf

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

POPULAR_TICKERS = [
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "GOOGL", # Alphabet (Google)
    "AMZN",  # Amazon
    "TSLA",  # Tesla
    "SPY",   # ETF S&P 500
    "BTC-USD", # Bitcoin
    "ETH-USD", # Ethereum
    "NVDA",  # NVIDIA
    "META",  # Meta (Facebook)
    "BRK-B", # Berkshire Hathaway
    "V",     # Visa
    "JNJ",   # Johnson & Johnson
    "WMT",   # Walmart
    "IBM",   # IBM   
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        use_yfinance = 'use_yfinance' in request.form
        ticker = request.form.get('ticker', 'AAPL') 
        S0 = float(request.form.get('S0', 100))
        K = float(request.form.get('K', 100))
        T = float(request.form.get('T', 1))
        r = float(request.form.get('r', 0.05))
        sigma = float(request.form.get('sigma', 0.2))
        option_type = request.form.get('option_type', 'call')
        
        if use_yfinance:
            S0, sigma = get_stock_data(ticker)
        
        # Calculations
        bs_price = black_scholes(S0, K, T, r, sigma, option_type)
        greeks = calculate_greeks(S0, K, T, r, sigma)
        mc_price = monte_carlo(S0, K, T, r, sigma, option_type=option_type)
        
        #Graphs generation
        plt.figure(figsize=(10, 6)) # Create a new figure
        simulations = [100, 500, 1000, 5000, 10000]
        mc_prices = [monte_carlo(S0, K, T, r, sigma, n, option_type) for n in simulations]
        plt.plot(simulations, mc_prices, 'b-', label='Monte Carlo')
        plt.axhline(bs_price, color='r', linestyle='--', label='Black-Scholes')
        plt.xlabel('Nombre de simulations')
        plt.ylabel('Prix')
        plt.legend()
        plt.savefig('static/plots/mc_convergence.png')
        plt.close('all')  # close all figures
        
        # PDF generation
        pdf_buffer = generate_pdf({
            'S0': S0,
            'K': K,
            'T': T,
            'r': r,
            'sigma': sigma,
            'option_type': option_type,
            'bs_price': bs_price,
            'mc_price': mc_price,
            'greeks': greeks,
            'ticker': ticker if use_yfinance else None
        })
        
        return render_template('results.html', 
                             bs_price=round(bs_price, 5),
                             mc_price=round(mc_price, 5),
                             greeks=greeks,
                             ticker=ticker if use_yfinance else None,
                            option_type=option_type)
    
    return render_template('index.html', tickers=POPULAR_TICKERS)

@app.route('/download_pdf')
def download_pdf():
    return send_file('static/report.pdf', as_attachment=True)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)