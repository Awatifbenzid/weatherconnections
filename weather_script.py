import csv
import requests
import pandas as pd
from datetime import datetime

# Function to get population from API
def get_population_from_api(api_key, city_name):
    #url = f"http://api.populationdata.com/population?city={city_name}&apikey={api_key}"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        population_data = response.json()

        # Assuming the API response contains a "total_population" key
        total_population = population_data.get("total_population", None)

        if total_population is not None:
            return total_population
        else:
            #print(f"Total population data not found for {city_name}.")
            return None

    except requests.exceptions.RequestException as e:
        #print(f"Error fetching total population data for {city_name}: {e}")
        return None

# Function to get average daily temperature for a city
def get_average_temp(api_key, city_name):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    # Extract temperature data from the API response
    temps = [entry['main']['temp'] for entry in data['list']]

    # Calculate the average temperature
    avg_temp = sum(temps) / len(temps)

    return avg_temp

# Function to process Excel data
def process_excel(file_path):
    df = pd.read_excel(file_path, sheet_name="raw_city_data")
    cities_data = df.to_dict(orient="records")

    return cities_data

# Function to write data to CSV
def write_to_csv(output_file, data):
    with open(output_file, 'w', newline='') as csv_file:
        fieldnames = ["date", "city", "avg_temp", "Country", "Language", "Climate", "Population_CSV","Population_API", "population_difference"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Your OpenWeather API key
api_key = "722ef9fd22420b8a16fe4be923918a3d"

# Excel file path
excel_file_path = "city_data_bi_developer_case_study_final (1).xlsx"

# List of cities from Excel
cities_data = process_excel(excel_file_path)

# Process each city
processed_data = []
for city in cities_data:
    city_name = city["City"]
    country_name= city["Country"]
    Climate_name= city["Climate"]
    language = city["Language"]
    population_csv = city["Population"]
    population_api1=0
    population_difference = population_csv - population_api1
    avg_temp = get_average_temp(api_key, city_name)
    population_api = get_population_from_api(api_key, city_name)

    # Perform further processing and populate the data structure for writing to CSV
    processed_data.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "city": city_name,
        "avg_temp": avg_temp,
        "Country": country_name,
        "Language": language,
        "Climate": Climate_name,
        "Population_CSV":population_csv,
        "Population_API":population_api1,
        "population_difference":population_difference




      #  "Population_API": population_api
        # Add other fields based on your requirements
    })

# Write data to CSV
write_to_csv("output.csv", processed_data)
