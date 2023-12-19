import requests

api_key = '722ef9fd22420b8a16fe4be923918a3d'
url = 'https://api.openweathermap.org/data/2.5/forecast'
city = 'Abidjan'

params = {
    'q': city,
    'appid': api_key
}

try:
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
       print("Weather Forecast for", city)
    for entry in data['list']:
        print(entry['dt_txt'], entry['main']['temp'])

    else:
        print("Error:", data['message'])

except Exception as e:
    print("An error occurred:", str(e))
