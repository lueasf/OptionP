import numpy as np
from scipy.stats import norm # Normal distribution
import yfinance as yf

# Normal distribution
# norm.cdf() for the cumulative distribution function
# norm.pdf() for the probability density function

# function that get the stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker) # Get stock ticker
    hist = stock.history(period="1y") # Get stock history for the last year
    S0 = hist['Close'][-1] # Get the last stock price
    volatility = hist['Close'].pct_change().std() * np.sqrt(252) # Calculate the stock volatility with 252 being the number of trading days in a year.
    return S0, volatility
    # std() for the standard deviation (écarts-types)
    # pct_change() for the percentage change between the current and a prior element.

# formula to calculate the Black-Scholes price
def black_scholes(S0, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S0/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    if option_type == 'call':
        price = S0 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2) # call price
    else:
        price = K * np.exp(-r*T) * norm.cdf(-d2) - S0 * norm.cdf(-d1) # put price
    return price

# function to calculate the greeks
def calculate_greeks(S0, K, T, r, sigma):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Delta
    delta_call = norm.cdf(d1)
    delta_put = norm.cdf(d1) - 1
    
    # Gamma (identique pour Call et Put)
    gamma = norm.pdf(d1) / (S0 * sigma * np.sqrt(T))
    
    # Vega (identique pour Call et Put)
    vega = S0 * norm.pdf(d1) * np.sqrt(T)
    
    # Theta
    theta_call = (- (S0 * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))) - r * K * np.exp(-r * T) * norm.cdf(d2)
    theta_put = (- (S0 * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))) + r * K * np.exp(-r * T) * norm.cdf(-d2)
    
    # Rho
    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2)
    rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2)

    return {
        'delta_call': delta_call,
        'delta_put': delta_put,
        'gamma': gamma,
        'vega': vega,
        'theta_call': theta_call,
        'theta_put': theta_put,
        'rho_call': rho_call,
        'rho_put': rho_put
    }

# function to calculate the price of an option using the Monte Carlo method
def monte_carlo(S0, K, T, r, sigma, n_simulations=10000, option_type='call'):
    dt = T
    np.random.seed(42) 
    stock_price = S0 * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*np.random.randn(n_simulations)) # Stock price at time T
    
    if option_type == 'call':
        payoff = np.maximum(stock_price - K, 0)
    else:
        payoff = np.maximum(K - stock_price, 0)
    
    price = np.exp(-r*T) * np.mean(payoff)
    return price