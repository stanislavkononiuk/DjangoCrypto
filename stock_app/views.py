from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Stock,  Account, FedFundRate, UsersLastSearchSettings, SmartMoney, UserPreference
from json import dumps
import json


@login_required(login_url='stock:login')
def index(request): 
    find_settings = UsersLastSearchSettings.objects.filter(user = request.user)
    if request.method == 'POST':
        # Get all submited data
        exchange = request.POST.get('exchange')
        min_price = request.POST.get('minPrice')
        max_price = request.POST.get('maxPrice')
        min_market_cap = request.POST.get('minMarketCap')
        max_market_cap = request.POST.get('maxMarketCap')
        min_volume = request.POST.get('minVolume')
        date_stock = request.POST.get('date')
        strategy = request.POST.get('strategy')
        alt_data = request.POST.get('color')
      
        try:
            # Delete last user search settings and save new search settings
            UsersLastSearchSettings.objects.create(user = request.user, exchange = exchange, min_price = min_price,
            max_price = max_price, min_market_cap = min_market_cap, max_market_cap = max_market_cap, min_volume = min_volume, 
            date_stock = date_stock, alt_data = alt_data)
            UsersLastSearchSettings.objects.filter(user = request.user).first().delete()
        except ValidationError:
            # If invalid input
            messages.error(request,"Invalid input! Select the date and provide all information in the fields.")
            context = {"pre_exchange":exchange, "pre_min_price":min_price,"pre_max_price":max_price, "pre_min_market_cap":min_market_cap,
                "pre_max_market_cap":max_market_cap, "pre_min_volume":min_volume, "pre_date_stock":date_stock, "pre_alt_data":alt_data }
            return render(request, 'stock_app/index.html', context)

        # Find last search
        
        if find_settings:
            access_data = find_settings[0]
            pre_exchange = access_data.exchange
            pre_min_price = access_data.min_price
            pre_max_price = access_data.max_price
            pre_min_market_cap = access_data.min_market_cap
            pre_max_market_cap = access_data.max_market_cap
            pre_min_volume = access_data.min_volume
            pre_date_stock = access_data.date_stock
            pre_alt_data = access_data.alt_data

        # If user is searching for the first time
        else:
            find_settings = UsersLastSearchSettings.objects.create(user = request.user, exchange = exchange, min_price = min_price,
            max_price = max_price, min_market_cap = min_market_cap, max_market_cap = max_market_cap, min_volume = min_volume, 
            date_stock = date_stock, alt_data = alt_data)
        context =  {"pre_exchange":pre_exchange, "pre_min_price":pre_min_price,"pre_max_price":pre_max_price, "pre_min_market_cap":pre_min_market_cap,
        "pre_max_market_cap":pre_max_market_cap, "pre_min_volume":pre_min_volume, "pre_date_stock":pre_date_stock, "pre_alt_data":pre_alt_data }

        # Get search result 
        try:
            if exchange == 'all':           
                get_all_stocks = Stock.objects.filter(price__gte = min_price, price__lte = max_price, 
                market_cap__gte = min_market_cap, market_cap__lte = max_market_cap, volume__gte = min_volume, date = date_stock, strategy__color = alt_data,  strategy__name = strategy) 
            else:
                get_all_stocks = Stock.objects.filter(date = date_stock, exchange = exchange, price__gte = min_price, price__lte = max_price,
                market_cap__gte = min_market_cap, market_cap__lte = max_market_cap, volume__gte = min_volume, strategy__name = strategy, strategy__color = alt_data).defer('open', 'high', 'low', 'volume', 'value')

            context = {'stocks': get_all_stocks, "pre_exchange":pre_exchange, "pre_min_price":pre_min_price,"pre_max_price":pre_max_price, "pre_min_market_cap":pre_min_market_cap,
            "pre_max_market_cap":pre_max_market_cap, "pre_min_volume":pre_min_volume, "pre_date_stock":pre_date_stock, "pre_alt_data":pre_alt_data }
            
        except ValidationError: 
            messages.error(request,"Invalid input! Select the date and provide all information in the fields.")

        return render(request, 'stock_app/index.html', context)
    
    # POST METHOD ENDS
    # When user loggs in again
    if find_settings:
        access_data = find_settings[0]
        pre_exchange = access_data.exchange
        pre_min_price = access_data.min_price
        pre_max_price = access_data.max_price
        pre_min_market_cap = access_data.min_market_cap
        pre_max_market_cap = access_data.max_market_cap
        pre_min_volume = access_data.min_volume
        pre_date_stock = access_data.date_stock
        pre_alt_data = access_data.alt_data
        context ={"pre_exchange":pre_exchange, "pre_min_price":pre_min_price,"pre_max_price":pre_max_price, "pre_min_market_cap":pre_min_market_cap,
        "pre_max_market_cap":pre_max_market_cap, "pre_min_volume":pre_min_volume, "pre_date_stock":pre_date_stock, "pre_alt_data":pre_alt_data }

    # First time on site
    else:
        context = {}

    return render(request, 'stock_app/index.html', context)


@login_required(login_url='stock:login')
def chart(request, ticker):
    stocks = Stock.objects.filter(ticker = ticker).select_related('strategy').order_by('date')
    interest = FedFundRate.objects.all().order_by('interest_date')
    smart_money = SmartMoney.objects.all().order_by('dateY')
    user_preference = UserPreference.objects.filter(user = request.user)

    if user_preference:
        for i in user_preference:
            nav = i.navbar_color
            background_color = i.background_color
            border_body = i.border_body
            button_color = i.button_color
            text_color = i.text_color
    else:
        nav  = '#061821'
        border_body = 'black'
        button_color = '#093042'
        background_color = '#061821'
        text_color = 'white'

    context = {'stocks':stocks, 'ticker':ticker, 'text_color': text_color, 'interest':interest, 'smart_money':smart_money, 'nav':nav, 'background_color':background_color,'border_body':border_body, 'button_color':button_color}
    return render(request, 'stock_app/chart.html', context)	

@login_required(login_url='stock:login')
def final_chart(request, ticker):   
    stocks = Stock.objects.filter(ticker = ticker).select_related('strategy').order_by('date')
    interest = FedFundRate.objects.all().order_by('interest_date')
    smart_money = SmartMoney.objects.all().order_by('dateY')
    user_preference = UserPreference.objects.filter(user = request.user)

    if user_preference:
        for i in user_preference:
            nav = i.navbar_color
            background_color = i.background_color
            border_body = i.border_body
            button_color = i.button_color
            text_color = i.text_color
    else:
        nav  = '#061821'
        border_body = 'black'
        button_color = '#093042'
        background_color = '#061821'
        text_color = 'white'

    context = {'stocks':stocks, 'ticker':ticker, 'text_color': text_color, 'interest':interest, 'smart_money':smart_money, 'nav':nav, 'background_color':background_color,'border_body':border_body, 'button_color':button_color}
    return render(request, 'stock_app/final_chart.html', context)

def loading(request):
    return render(request, 'stock_app/loader.html')

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password =  request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                
                login(request, user)
                nav  = '#061821'
                border_body_color = 'black'
                button_color = '#093042'
                background_color = '#061821'
                
                user_preference = UserPreference.objects.filter(user = request.user)
                if user_preference:
                    pass
                else:
                    UserPreference.objects.create(user = user, navbar_color = nav, background_color = background_color, button_color = button_color, border_body = border_body_color)
            
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("stock:loading")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    
    form = AuthenticationForm()
    context={"login_form":form}
    return render(request, "stock_app/login.html", context)


def add_to_watchlist(request, ticker):
    if request.method == 'POST':
        color = request.POST.get('color')
        user = request.user
        account = Account.objects.filter(user = user, color = color, stock_ticker = ticker)
        if account:
            messages.info(request, "You already have this stock with same color on the watch list!")
        else:
            Account.objects.create(user = user, color = color, stock_ticker = ticker)

    added_to_watchlist = Account.objects.filter(user = request.user)
    context = {'ticker':ticker, 'added_to_watchlist':added_to_watchlist}
    return render(request, 'stock_app/add_to_watchlist.html', context)


def remove_from_watchlist(request, ticker, color):
    if request.method == 'POST':
        Account.objects.filter(user = request.user , stock_ticker = ticker, color = color).delete()
        messages.info(request, f"{ticker} stock with {color} indication is removed!")
        return render(request, 'stock_app/add_to_watchlist.html')
    context = {'ticker':ticker, 'color':color}
    return render(request, 'stock_app/remove_from_watchlist.html', context)

def whatch_list(request):
    added_to_watchlist = Account.objects.filter(user = request.user)
    context = {'stocks':added_to_watchlist}
    return render(request, 'stock_app/whatch_list.html', context)

def preference(request, ticker):
    user = request.user
    if request.method == 'POST':
        stocks = Stock.objects.filter(ticker = ticker).select_related('strategy').order_by('date')
        interest = FedFundRate.objects.all().order_by('interest_date')
        smart_money = SmartMoney.objects.all().order_by('dateY')
        mode = request.POST.get('mode')    
        if mode ==   'dark':
            nav  = '#061821'
            border_body_color = 'black'
            button_color = '#093042'
            background_color = '#061821'
            text_color = 'white'
        else: 
            nav  = 'white'
            border_body_color = 'white'
            button_color = '#3B71CA'
            background_color = 'white'
            text_color = 'black'
        UserPreference.objects.filter(user = user).delete()
        UserPreference.objects.create(user = user, text_color = text_color, navbar_color = nav, background_color = background_color, button_color = button_color, border_body = border_body_color)
        context = {'stocks':stocks, 'ticker':ticker, 'interest':interest, 'smart_money':smart_money,
            'nav':nav,
            'border_body':border_body_color,
            'button_color':button_color,
            'background_color':background_color,
            'ticker':ticker,
            "text_color":text_color
        }
        return render(request, 'stock_app/chart.html', context)
    return render(request, 'stock_app/preferences.html')