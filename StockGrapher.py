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
        ax.set_ylabel('Close Price')
        plt.title(ticker)

def main():    
    tickers, period  = GetInput(tickers, period)
    data = FetchData(tickers, period)
    clean = CleanData(data)
    CreateVis(clean)


if __name__ == '__main__':
   main()
