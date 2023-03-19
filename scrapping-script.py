import csv
import googlemaps
from datetime import datetime
from secrets_env import api_key;
import pandas as pd
import time

# Next page token to load more data
page_token = ""

# Load existing data from file (if it exists)
try:
    existing_data = pd.read_csv('./build/businesses.csv', engine='python', encoding='ISO-8859-1')
except pd.errors.EmptyDataError and FileNotFoundError:
    existing_data = pd.DataFrame()

# Replace with the area you want to search in
search_area = 'Campinas, SP'

# Replace with the type of business you want to search for
search_type = ''

# Initialize the Google Maps client
gmaps = googlemaps.Client(api_key)

toContinue = True

while toContinue:
    # Perform the search
    if (len(page_token) > 0):
        time.sleep(2)
        places = gmaps.places(query=search_type, location=search_area, radius=50000, page_token=page_token)
        existing_data = pd.read_csv('./build/businesses.csv', engine='python', encoding='ISO-8859-1')
    else:
        places = gmaps.places(query=search_type, location=search_area, radius=50000)
    if (places.get('next_page_token') is None):
        toContinue = False
        break
    page_token = places['next_page_token']

    # Create a list to hold the results
    results = []

    # Iterate through the places and save the name, phone, website, and address
    for place in places['results']:
        name = place['name']
        if len(existing_data) == 0 or name not in existing_data['Name']:
            name = place['name']
            phone = place['formatted_phone_number'] if 'formatted_phone_number' in place else ''
            website = place['website'] if 'website' in place else ''
            address = place['formatted_address']
            url = place['url'] if 'url' in place else ''
            tipo = search_type
            results.append([name, phone, website, address, url, tipo])

    # Output the results to a CSV file
    try:
        with open('./build/businesses.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Phone', 'Website', 'Address', 'Url', 'Tipo'])
            for result in results:
                writer.writerow(result)
    except FileNotFoundError:
        with open('./build/businesses.csv', 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Phone', 'Website', 'Address', 'Url', 'Tipo'])
            for result in results:
                writer.writerow(result)
