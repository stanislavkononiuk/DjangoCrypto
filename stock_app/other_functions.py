from __future__ import absolute_import, unicode_literals
import requests
from django.core.mail import send_mail
from datetime import datetime
import datetime as dt
from .models import Stock, Strategy, Account,  SmartMoney
from dateutil.relativedelta import relativedelta
import os, csv
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings


FINANCIAL_MODELING_API_KEY = 'caf440df50e719f644d53cb01165d5d3'
today = datetime.today().strftime('%Y-%m-%d')

def send_email_func(ticker_email, color):
    get_user_to_send_email = Account.objects.filter(stock_ticker = ticker_email, color = color)
    for i in get_user_to_send_email:
        email = i.user.email
        send_mail(
            'STOCK ACHIVED DESIRED COLOR',
            'Stock: '+ticker_email+' achived wanted : '+color + ' color with Ultimate Recovery Strategy' + '\n',
            'stefan.programming22@gmail.com',
            [email],
        )

def stock_split_func(stock_split_date):
      if stock_split_date == today:
        symbol = symbol
        print('STOCK SPLIT FOR: ' + symbol)
        Stock.objects.filter(ticker = symbol).delete()
        ohlc_data = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=1996-01-01&to={today}&apikey={FINANCIAL_MODELING_API_KEY}'
        market_cap = f'https://financialmodelingprep.com/api/v3/historical-market-capitalization/{symbol}?apikey={FINANCIAL_MODELING_API_KEY}'
        get_ohlc = requests.get(ohlc_data)
        json_historical_data = get_ohlc.json()
        get_market_cap = requests.get(market_cap)
        if get_market_cap and json_historical_data['historical']:          
            market_cap_json = get_market_cap.json()
            try:   
                # getting number of loops to run through json data
                number_of_dictionaries_count = (len(json_historical_data['historical']))
                # getting company data
                company_url = f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FINANCIAL_MODELING_API_KEY}'
                company_get = requests.get(company_url)
                company_json = company_get.json()
                
                
                company_name = company_json[0]['companyName']
                exchange = company_json[0]['exchangeShortName']
                company_industry = company_json[0]['industry'] 
                company_sector = company_json[0]['sector'] 	
                
                
                
                if company_name and company_industry and company_sector and exchange:                  
                        
                        for date_index in range(number_of_dictionaries_count):
                            # getting historical data values
                            historical_date = json_historical_data['historical'][date_index]['date']
                            if historical_date:
                                
                                date_stored = datetime.strptime(historical_date, '%Y-%m-%d').date()
                                
                                
                                # other values	
                                price = json_historical_data['historical'][date_index]['close']
                                try:
                                    volume = json_historical_data['historical'][date_index]['volume']	
                                except KeyError:
                                    volume = 1
                                open = json_historical_data['historical'][date_index]['open']
                                high = json_historical_data['historical'][date_index]['high']
                                low = json_historical_data['historical'][date_index]['low']
                                value = price * volume                            
                                # NET GAIN
                                net_gain = 0
                                # market cap
                                
                                if market_cap_json:	
                                    for i in range(len(market_cap_json)):
                                        market_cap_date = market_cap_json[i]['date']
                                        mc_date_stored = datetime.strptime(market_cap_date, '%Y-%m-%d').date()				
                                        
                                        if mc_date_stored == date_stored:								
                                            market_cap_value = market_cap_json[i]['marketCap']
                                            break
                                        
                                        else:
                                            market_cap_value = 100000000
                                else:
                                    market_cap_value = 100000000		
                                
                                create_new_stock = Stock.objects.create(ticker = symbol, exchange = exchange, company_name = company_name, company_sector = company_sector,
                                industry = company_industry, price = price, volume = volume, value = value, date = date_stored, open = open, high = high, low = low,
                                    net_gain = net_gain, market_cap = market_cap_value)

                        find = Stock.objects.filter(ticker = symbol, net_gain = 0).order_by('-date')
                        count_net = 0
                        for stock in find:
                            if count_net == 3:
                                break
                            else:
                                last_year =stock.date - relativedelta(years=1)
                                last_year_data = dt.date(last_year.year, last_year.month, last_year.day)
                                get_stock = Stock.objects.filter(ticker = stock.ticker, date__lte = last_year_data, net_gain = 0).order_by('-date').first()
                                if get_stock:

                                    starting_price = get_stock.open
                                    if starting_price == 0:
                                        starting_price = 1
                                    current_price =  stock.price

                                    net_gain = round(((float(current_price) - float(starting_price))/float(starting_price)) * 100, 3)
                                    create_new_stock = Stock.objects.filter(ticker = stock.ticker, date = stock.date).update(net_gain = net_gain)											
                                else:
                                    count_net += 1			
                                    
                        strategy_list = ['CCI']			
                        cci_p = 253
                        for strategy in strategy_list:
                            if strategy == 'CCI':
                            
                                stocks = Stock.objects.filter(ticker = symbol).order_by("date")[cci_p:]
                                for stock in stocks:
                                    stocks_1 = Stock.objects.filter(ticker = symbol, date = stock.date).order_by('-date')[:cci_p]    
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
                                                if cci > 0 and cci < 100:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "green")
                                                if cci > 100 and cci < 200:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "orange")
                                                if cci > 200 and cci < 300:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "red")
                                                if cci > 300 and cci < 400:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "pink")
                                                if cci > 400 and cci < 500:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "brown")
                                                if cci > 500:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "black")
                                                if cci <= 0 and cci > -100:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "light green")
                                                if cci > -200 and cci <	 -100:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI" , color = "blue")
                                                if cci > -300 and cci < -200:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "violet")
                                                if cci > -400 and cci < -300:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "purple")
                                                if cci > -500 and cci < -400:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "light purple")
                                                if cci < -500:
                                                    Strategy.objects.create(stock = st, result = cci, name = "CCI", color = "yellow")
                                            except:                          
                                                pass																																																
            except KeyError:
                pass
        

# FUNCTION FOR CSV UPLOAD
def read_csv_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file = open(os.path.join(settings.MEDIA_ROOT, filename), encoding='utf8')
        reader = csv.reader(file)

        for row in reader:
            interest_date = row[0]
            interest_value = float(row[1])    
            interest_date = interest_date.replace('ï»¿', '')
            #value = 100
            #strategy_interest = 100 - (interest_value * 40) + 900
            if interest_date and interest_value:
                SmartMoney.objects.create(dateY = interest_date, value = interest_value)
                #FedFundRate.objects.create(interest_date = interest_date, interest = interest_value, value = value, strategy_interest = strategy_interest)
    return render(request, 'stock_app/upload_blogs.html')
