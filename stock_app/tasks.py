from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from django.core.mail import send_mail
from datetime import datetime
import datetime as dt
from .models import Stock, Strategy, Account, FedFundRate
from dateutil.relativedelta import relativedelta
from .other_functions import send_email_func, stock_split_func

FINANCIAL_MODELING_API_KEY = 'caf440df50e719f644d53cb01165d5d3'
today = datetime.today().strftime('%Y-%m-%d')


@shared_task
def get_eod_data():
    symbol_list = Stock.objects.distinct('ticker').values_list('ticker')
    ticker_number = 0
    check_date = '2023-01-01'
    c_date = datetime.strptime(check_date, '%Y-%m-%d').date()
    for symbol_1 in symbol_list:
        ticker_number += 1
        symbol = symbol_1[0]
        print(ticker_number)
        
        get_market_cap = requests.get(f'https://financialmodelingprep.com/api/v3/historical-market-capitalization/{symbol}?limit=10&apikey={FINANCIAL_MODELING_API_KEY}')
        get_ohlc = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={today}&to={today}&apikey={FINANCIAL_MODELING_API_KEY}')   
        stock_split = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_split/{symbol}?apikey={FINANCIAL_MODELING_API_KEY}')
        mc_data = get_market_cap.json()
        ohlc_json = get_ohlc.json()  
        json_stock_split = stock_split.json()  
             
        cci_p = 253	
        
        # Stock Split
        historical_stock_split = json_stock_split['historical']
        if historical_stock_split:  
            stock_split_date = historical_stock_split[0]['date']
            stock_split_func(stock_split_date) 

        if ohlc_json:
            print(symbol)
            try:
                universal = ohlc_json['historical'][0]            
                date_stored_ = universal['date']
                if date_stored_:
                    # market cap
                    if mc_data:
                        universal_mc = mc_data[0]
                        market_cap_value = universal_mc['marketCap']
                    else:
                        get_stock = Stock.objects.filter(ticker = symbol).last()
                        market_cap_value = get_stock.market_cap
                
                    date_stored = datetime.strptime(date_stored_, '%Y-%m-%d').date()                  
                    if date_stored > c_date:
                        get_duplicate = Stock.objects.filter(ticker = symbol, date = date_stored)
                        if get_duplicate:
                            pass			
                        else:   
                            price = universal['close']
                            open = universal['open']
                            high = universal['high']
                            low = universal['low']
                            try:
                                volume = universal['volume']
                                value = price * volume
                            except KeyError:
                                volume = 1
                                value = volume
                            
                            # net gain
                            date_stored = datetime.strptime(date_stored_, '%Y-%m-%d').date()
                            last_year = date_stored - relativedelta(years=1)	
                            get_stock_net_gain = Stock.objects.filter(ticker = symbol, date__lte = last_year).order_by('-date').first()

                            if get_stock_net_gain:                              
                                company_industry = get_stock_net_gain.industry
                                company_name = get_stock_net_gain.company_name
                                company_sector = get_stock_net_gain.company_sector
                                exchange = get_stock_net_gain.exchange
                                net_gain = round(((price - open)/open) * 100, 3)
                                
                            else:                        
                                company_url = f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FINANCIAL_MODELING_API_KEY}'
                                company_get = requests.get(company_url)
                                company_json = company_get.json()

                                company_name = company_json[0]['companyName']
                                exchange = company_json[0]['exchangeShortName']
                                company_industry = company_json[0]['industry']
                                company_sector = company_json[0]['sector']
                                net_gain = 0
                                if not company_name or not company_industry or not company_sector or not exchange:
                                    get_stock = Stock.objects.filter(ticker = symbol).last()
                                    company_industry = get_stock.industry
                                    company_name = get_stock.company_name
                                    company_sector = get_stock.company_sector
                                    exchange = get_stock.exchange                         
                            
                            Stock.objects.create(ticker = symbol,  exchange = exchange, company_name = company_name, company_sector = company_sector,
                            industry = company_industry, price = price, volume = volume, value = value, date = date_stored, open = open, high = high, low = low,
                                net_gain = net_gain, market_cap = market_cap_value)	

                            # Strategy CCI                                                                                                                                                                         
                            stocks_1 = Stock.objects.filter(ticker = symbol).order_by('-date')[:cci_p]
                            if(len(stocks_1)) == 253:
                                
                                typical_price_sum = 0
                                typical_price_list = []
                                md_sum = 0	
                                for st in reversed(stocks_1):
                                    typical_price = (st.high+st.low+st.price)/3
                                    typical_price_list.append(typical_price)
                                    typical_price_sum += typical_price
                                    
                                    if st == stocks_1[0]:	
                                                                                                        
                                        typical_price_average = typical_price_sum/cci_p
                                        for i in typical_price_list:	
                                            md = (abs(i - typical_price_average))
                                            md_sum += md

                                        md = float(md_sum)/cci_p
                                            
                                        cci = float((typical_price - typical_price_average)) / (0.015 * md)					
                                        try:				
                                            ticker_email = st.ticker													
                                            if cci > 0 and cci < 100:
                                                send_email_func(ticker_email, 'green')
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "green")
                                            if cci > 100 and cci < 200:
                                                send_email_func(ticker_email, 'orange')
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "orange")
                                            if cci > 200 and cci < 300:
                                                send_email_func(ticker_email, 'red')
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "red")
                                            if cci > 300 and cci < 400:
                                                send_email_func(ticker_email, 'pink')
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "pink")
                                            if cci > 400 and cci < 500:
                                                send_email_func(ticker_email, 'brown')
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "brown")
                                            if cci > 500:
                                                send_email_func(ticker_email, 'black')
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "black")
                                            if cci <= 0 and cci > -100:
                                                send_email_func(ticker_email, 'light green')
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "light green")
                                                            
                                            if cci > -200 and cci <	 -100:
                                                send_email_func(ticker_email, "blue")
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI" , color = "blue")

                                            if cci > -300 and cci < -200:
                                                send_email_func(ticker_email, "violet")
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "violet")

                                            if cci > -400 and cci < -300:
                                                send_email_func(ticker_email, "purple")
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "purple")
                                            if cci > -500 and cci < -400:
                                                send_email_func(ticker_email, "light purple")
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "light purple")
                                            if cci < -500:
                                                send_email_func(ticker_email, "yellow")
                                                Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "yellow")
                                        except:
                        
                                            pass
            except:
                pass           

@shared_task
def fedFundUpdate():
    last_fed_fund = FedFundRate.objects.last()
    last_fed_fund_value = last_fed_fund.interest
    new_fed_fund_strategy = 100 - (last_fed_fund_value * 40) + 900
    FedFundRate.objects.create(interest_date = today, interest = last_fed_fund_value, strategy_interest = new_fed_fund_strategy)
                            