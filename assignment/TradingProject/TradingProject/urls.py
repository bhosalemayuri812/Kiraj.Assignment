# MainApp/urls.py
from django.urls import path
from MainApp import views

urlpatterns = [
    # path('upload-csv/', views.upload_csv_view, name='upload_csv'),
    # path('convert-candles/<int:timeframe_minutes>/', views.convert_candles_view, name='convert_candles'),
    # path('store-data-as-json/<int:timeframe_minutes>/', views.store_data_as_json, name='store_data_as_json'),
    # URL for the view to convert candles
     path('convert_candles/<int:timeframe_minutes>/', views.convert_candles_view, name='convert_candles'),

    # URL for the view to store data as JSON
    path('store_data_as_json/<int:timeframe_minutes>/', views.store_data_as_json, name='store_data_as_json'),
]
