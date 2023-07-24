from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.index, name = 'index'),
    path("login/", views.login_request, name="login"),
    path('logout/', LogoutView.as_view(template_name = 'stock_app/logout.html'), name = 'logout'),
    path('chart/<str:ticker>/', views.chart, name = 'chart'),
    path('final_chart/<str:ticker>/', views.final_chart, name = 'final_chart'),
    path('add-to-watchlist/<str:ticker>/', views.add_to_watchlist, name='add to watch list'),
    path('whatch-list/', views.whatch_list, name = 'whatch_list'),
    path('remove-from-watchlist/<str:ticker>/<str:color>/', views.remove_from_watchlist, name = 'remove_from_watchlist'),
    path('loading/', views.loading, name = 'loading'),
    path('user-preferences/<str:ticker>/', views.preference, name = 'preference'),
    #path('csv/', views.read_csv_file, name = 'csv_file')
]
