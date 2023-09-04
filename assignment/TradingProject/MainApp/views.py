import pandas as pd
from .models import Candle
from django.shortcuts import render
# from .forms import CSVUploadForm
# MainApp/views.py
import pandas as pd
from .models import Candle
import asyncio
from datetime import datetime, timedelta
from django.http import JsonResponse
import json
from django.http import JsonResponse
import json
from django.http import JsonResponse
import asyncio
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import Candle
import json
import os
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.conf import settings



# def upload_csv_view(request):
#     if request.method == 'POST':
#         form = CSVUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file = form.cleaned_data['csv_file']
#             timeframe = form.cleaned_data['timeframe']
            
#             # Read the CSV file using Pandas
#             df = pd.read_csv(csv_file)

#             # Iterate through the CSV data and create Candle objects
#             for _, row in df.iterrows():
#                 Candle.objects.create(
#                     symbol=row['BANKNIFTY'],
#                     date=row['DATE'],
#                     time=row['TIME'],
#                     open=row['OPEN'],
#                     high=row['HIGH'],
#                     low=row['LOW'],
#                     close=row['CLOSE'],
#                     volume=row['VOLUME']
#                 )

#             # Now, the CSV data is stored in the database as Candle objects
#             # Proceed to the next steps for data conversion and JSON storage
#             # ...

#     else:
#         form = CSVUploadForm()
#     return render(request, 'upload_csv.html', {'form': form})

# # MainApp/views.py

# # Define a function to convert candles to the desired timeframe
# async def convert_candles_to_timeframe(candles, timeframe_minutes):
#     # Create a dictionary to store the converted data
#     converted_data = []

#     # Initialize variables to track the open, high, low, and close prices
#     open_price = candles[0].open
#     high_price = candles[0].high
#     low_price = candles[0].low
#     close_price = candles[0].close

#     # Initialize the timestamp for the first candle
#     current_time = candles[0].date + timedelta(minutes=(candles[0].time.hour * 60 + candles[0].time.minute) % timeframe_minutes)

#     for candle in candles:
#         # Check if the current candle is within the desired timeframe
#         if candle.date + timedelta(minutes=(candle.time.hour * 60 + candle.time.minute) % timeframe_minutes) != current_time:
#             # Add the converted data to the list
#             converted_data.append({
#                 'open': open_price,
#                 'high': high_price,
#                 'low': low_price,
#                 'close': close_price,
#                 'date': current_time.strftime('%Y-%m-%d %H:%M:%S'),
#             })

#             # Reset variables for the next timeframe
#             open_price = candle.open
#             high_price = candle.high
#             low_price = candle.low
#             close_price = candle.close
#             current_time = candle.date + timedelta(minutes=(candle.time.hour * 60 + candle.time.minute) % timeframe_minutes)
#         else:
#             # Update high and low prices for the current timeframe
#             high_price = max(high_price, candle.high)
#             low_price = min(low_price, candle.low)
#             close_price = candle.close

#     # Add the last converted data
#     converted_data.append({
#         'open': open_price,
#         'high': high_price,
#         'low': low_price,
#         'close': close_price,
#         'date': current_time.strftime('%Y-%m-%d %H:%M:%S'),
#     })

#     return converted_data

# # Create a view to convert candles and return as JSON
# async def convert_candles_view(request, timeframe_minutes):
#     # Get all Candle objects from the database (you may need to filter by symbol or date)
#     candles = Candle.objects.all()

#     # Convert candles to the desired timeframe
#     converted_data = await convert_candles_to_timeframe(candles, timeframe_minutes)

#     # Return the converted data as JSON
#     return JsonResponse({'data': converted_data})

# def store_data_as_json(request, timeframe_minutes):
#     # Get the converted data (you can reuse the previous conversion function)
#     converted_data = await convert_candles_to_timeframe(candles, timeframe_minutes)

#     # Define the path to store the JSON file
#     json_filename = f'data_{timeframe_minutes}min.json'
#     json_path = os.path.join(settings.MEDIA_ROOT, json_filename)

#     # Store the converted data as JSON
#     with open(json_path, 'w') as json_file:
#         json.dump({'data': converted_data}, json_file)

#     # Return a JSON response with the path to the stored JSON file
#     return JsonResponse({'json_path': json_path})


def convert_candles_to_timeframe(candles, timeframe_minutes):
    converted_data = []
    current_timeframe = None
    candle_group = []

    for candle in candles:
        candle_datetime = datetime.combine(candle.date, candle.time)
        
        # Calculate the start time of the current timeframe
        if current_timeframe is None:
            current_timeframe = candle_datetime
        elif (candle_datetime - current_timeframe).total_seconds() >= 60 * timeframe_minutes:
            # If the current candle is outside the current timeframe, start a new one
            converted_data.append({
                'open': candle_group[0].open,
                'high': max(c.open for c in candle_group),
                'low': min(c.low for c in candle_group),
                'close': candle_group[-1].close,
                'date': current_timeframe.strftime('%Y-%m-%d %H:%M:%S'),
            })
            current_timeframe = candle_datetime
            candle_group = []

        candle_group.append(candle)

    # Add the last converted data
    if candle_group:
        converted_data.append({
            'open': candle_group[0].open,
            'high': max(c.open for c in candle_group),
            'low': min(c.low for c in candle_group),
            'close': candle_group[-1].close,
            'date': current_timeframe.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return converted_data
def convert_candles_view(request, timeframe_minutes):
    # Get all Candle objects from the database (you may need to filter by symbol or date)
    candles = Candle.objects.all()

    # Convert candles to the desired timeframe
    converted_data = convert_candles_to_timeframe(candles, timeframe_minutes)

    # Return the converted data as JSON
    return JsonResponse({'data': converted_data})

def store_data_as_json(request, timeframe_minutes):
    # Get all Candle objects from the database (you may need to filter by symbol or date)
    candles = Candle.objects.all()

    # Get the converted data
    converted_data = convert_candles_to_timeframe(candles, timeframe_minutes)

    # Define the path to store the JSON file
    json_filename = f'data_{timeframe_minutes}min.json'
    json_path = os.path.join(settings.MEDIA_ROOT, json_filename)

    # Store the converted data as JSON
    with open(json_path, 'w') as json_file:
        json.dump({'data': converted_data}, json_file)

    # Return a JSON response with the path to the stored JSON file
    return JsonResponse({'json_path': json_path})

