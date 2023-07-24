from django.contrib import admin
from .models import Stock, Strategy, P, Account, UsersLastSearchSettings, FedFundRate, SmartMoney, UserPreference

admin.site.register(Stock)
admin.site.register(Strategy)
admin.site.register(P)
admin.site.register(Account)
admin.site.register(UsersLastSearchSettings)
admin.site.register(FedFundRate)
admin.site.register(SmartMoney)
admin.site.register(UserPreference)