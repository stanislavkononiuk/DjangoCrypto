from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=100, null = True, blank = True)
    stock_ticker = models.CharField(max_length=100, null = True, blank = True)
    def __str__(self):
        return str(self.user) + ' ' + self.stock_ticker

class Stock(models.Model):
    ticker = models.CharField(max_length=10, null = True, blank = True, db_index = True)
    exchange = models.CharField(max_length=10, null = True, blank = True,  db_index = True)
    company_name = models.CharField(max_length=200, null = True, blank = True)
    company_sector = models.CharField(max_length=200, null = True, blank = True, default="NOT PROVIDED")
    industry = models.CharField(max_length=200, null = True, blank = True, default="NOT PROVIDED")
    market_cap = models.DecimalField(max_digits=100, decimal_places=20, null = True, blank = True, default = 100000000)
    price = models.DecimalField(max_digits=50, decimal_places=20, null = True, blank = True)
    volume = models.DecimalField(max_digits=100, decimal_places=20, null = True, blank = True)
    value =models.DecimalField(max_digits=50, decimal_places=20, null = True, blank = True)
    net_gain =models.DecimalField(max_digits=100, decimal_places=20, null = True, blank = True)
    open =models.DecimalField(max_digits=50, decimal_places=20, null = True, blank = True)
    low = models.DecimalField(max_digits=50, decimal_places=20, null = True, blank = True)
    high = models.DecimalField(max_digits=50, decimal_places=20, null = True, blank = True)
    date = models.DateField(null = True, blank = True, db_index = True)

    def __str__(self):
        return self.ticker + ' ' + str(self.date)
    
class SmartMoney(models.Model):
    dateY = models.DateField(blank=True, null=True) 
    value = models.DecimalField(max_digits=15, decimal_places=5, null = True, blank = True)
    
    def __str__(self):
        return str(self.dateY) + ' ' +  str(self.value)
    
        
class Strategy(models.Model):
    name = models.CharField(max_length=100)
    stock = models.OneToOneField(Stock, on_delete = models.CASCADE, null = True, blank = True)
    color = models.CharField(max_length=50, null = True, blank = True)
    result =  models.DecimalField(max_digits=15, decimal_places=5, null = True, blank = True)
    value = models.IntegerField(null = True, blank = True, default = 100)

    def __str__(self):
        try:
            return self.name + " "+ str(self.stock.ticker) + " " + str(self.stock.date)
        except:
            return self.name + " " + "stock not provided"

class P(models.Model):
    strategy = models.OneToOneField(Strategy, on_delete=models.DO_NOTHING)
    value = models.IntegerField()

    def __str__(self):
        return self.strategy.name

class UsersLastSearchSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange =  models.CharField(max_length=10, null = True, blank = True)
    min_price =  models.DecimalField(max_digits=100, decimal_places=3, null = True, blank = True)
    max_price =  models.DecimalField(max_digits=100, decimal_places=3, null = True, blank = True)
    min_market_cap =  models.DecimalField(max_digits=100, decimal_places=3, null = True, blank = True)
    max_market_cap =  models.DecimalField(max_digits=100, decimal_places=3, null = True, blank = True)
    min_volume =  models.DecimalField(max_digits=100, decimal_places=3, null = True, blank = True)
    date_stock = models.DateField(null = True, blank = True)
    alt_data =models.CharField(max_length=100, null = True, blank = True)  
    
    def __str__(self):
        return self.user

class FedFundRate(models.Model):
    interest_date = models.DateField(blank=True, null=True)  
    interest = models.DecimalField(max_digits=5, decimal_places= 3)
    strategy_interest  = models.DecimalField(max_digits=15, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return str(self.interest) +  ' ' +  str(self.interest_date)

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    navbar_color = models.CharField(max_length=100, null = True, blank = True, default='#061821')
    border_body = models.CharField(max_length=100, null=True, blank=True, default='black')
    background_color = models.CharField(max_length=100, null=True, blank=True, default='#061821')
    button_color = models.CharField(max_length=100, null=True, blank=True, default='#093042')
    text_color = models.CharField(max_length=100, null=True, blank=True, default='white')

    def __str__(self):
        return str(self.user) + ' ' +  self.border_body
