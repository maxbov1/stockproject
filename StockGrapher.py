import os
import matplotlib
import requests
from pprint import pprint
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import Response

import yfinance as yf
import pandas as pd

def get_stats(ticker):
    Ticker = yf.Ticker(ticker)
    df = pd.DataFrame(Ticker.upgrades_downgrades).head(5)
    df2 = pd.DataFrame(Ticker.recommendations).head(5)    
    df = df.drop(columns=["FromGrade"])
    
    def convert_period(period_str):
        num_months = int(period_str.replace('m', ''))
        
        abs_months = abs(num_months)
        
        if num_months == 0:
            return 'current month'
        elif num_months == -1:
            return '1 month ago'
        else:
            return f'{abs_months} months ago'

    if 'period' in df2.columns:
        df2['period'] = df2['period'].apply(convert_period)   
    
    def highlight_action(val):
        color = {
            'main': 'lightblue',
            'up': 'lightgreen',
            'reit': 'lightyellow',
            '': 'white'  
        }.get(val, 'white')
        return f'background-color: {color}; color: black;'
    
    def highlight_grade(val):
        color = {
            'Outperform': 'darkgreen',
            'Buy': 'lightgreen',
            'hold': 'gray',
            'sell': 'lightred',
            'Underperform': 'green',
            'Underweight': 'red',
            'Overweight': 'darkred',
        }.get(val, 'white')
        return f'background-color: {color}; color: black;'
    
    def apply_gradient_styles(df):
        numeric_columns = ['strongBuy', 'buy', 'hold', 'sell', 'strongSell']
        styled_df2 = df.style.background_gradient(subset=numeric_columns, cmap='BuGn')
        return styled_df2.to_html()

    def apply_styles(df):
        if 'Action' in df.columns:
            styled_df = df.style.applymap(highlight_action, subset=['Action'])
        if 'ToGrade' in df.columns:    
            styled_df = styled_df.applymap(highlight_grade, subset=['ToGrade'])
            
        return styled_df.to_html()
    
    result = apply_styles(df)
    result2 = apply_gradient_styles(df2)
    
    list_of_tables = [result, result2]
    
    
    return list_of_tables


def remove_newlines(l_of_t):
    for html in l_of_t:
        for item in html:
            item.strip('\n')
    return l_of_t



def IsValid(ticks):
  ValidFrame = pd.Dataframe("nasdaq-listed.csv")
  ValidTickers = ValidFrame.Symbol
  for t in ticks:
    if t not in ValidTickers:

      raise ValueError(f'Symbol {t} is invalid')


def GetInput(tickers,period):
  ListofTicks =  tickers.split(',')
  ListofTicks = [t.strip() for t in ListofTicks]
  try:
    IsValid(ListofTicks)
  except :
    pass
  p = period.strip()

  return ListofTicks, p

def FetchData(tickers, per ):
  stock_info = {}
  if per == '3mo' or per == '1mo':
    intv = '1d'
  else:
    intv = '30m'
  for t in tickers:
     data = yf.download(f"{t}", period=f"{per}", interval=f'{intv}')
     stock_info[t] = data
  return stock_info

def CleanData(stockDoc):
  for k, v in stockDoc.items():
    close_ser = v['Close']
    stockDoc[k] = close_ser
  return stockDoc



def CreateVis(stockdict):
    sns.set_style("dark")
    matplotlib.use('Agg')
    fig, ax = plt.subplots()
    for ticker, dataframe in stockdict.items():
        start_date = dataframe.index[0]
        end_date = dataframe.index[-1]
        min_close = dataframe.min()
        max_close = dataframe.max()
        dataframe.plot(ax=ax)
        ax.set_xlim(start_date - pd.Timedelta(days=1) / 4, end_date + pd.Timedelta(days=1) / 4)
        ax.set_ylim(min_close * 0.9, max_close * 1.1)
        ax.set_xlabel('Dates')
        ax.set_ylabel('Close Price($)')
        plt.title(ticker)
def save_plot_to_memory(stockdict):
        buffer = io.BytesIO()  # Create a buffer to hold the PNG image
        CreateVis(stockdict)  # Generate the plot
        plt.savefig(buffer, format='png')  # Save the plot to the buffer in PNG format
        plt.close()  # Close the plot to release memory
        buffer.seek(0)  # Reset the buffer position to the beginning
        return buffer
def main():    
    tickers, period  = GetInput(tickers, period)
    data = FetchData(tickers, period)
    clean = CleanData(data)
    CreateVis(clean)


if __name__ == '__main__':
   main()
