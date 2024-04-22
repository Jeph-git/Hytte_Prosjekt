import requests

def get_weather(city, date):
    api_key = '3fb0aef06dc7cbbda990d8928b2b3111'
    url = f"https://api.weatherapi.com/v1/history.json?key={api_key}&q={city}&dt={date}"
    response = requests.get(url)
    data = response.json()
    
    if 'error' in data:
        print(f"Error: {data['error']['message']}")
        return None
    
    weather_desc = data['forecast']['forecastday'][0]['day']['condition']['text']
    weather_code = data['forecast']['forecastday'][0]['day']['condition']['code']
    temp = data['forecast']['forecastday'][0]['day']['avgtemp_c']
    humidity = data['forecast']['forecastday'][0]['day']['avghumidity']
    wind_speed = data['forecast']['forecastday'][0]['day']['maxwind_kph']
    
    # Display weather icon
    weather_icons = {
        'Thunderstorm': "⛈️",
        'Drizzle': "🌧️",
        'Rain': "🌧️",
        'Snow': "❄️",
        'Atmosphere': "🌫️",
        'Clear': "☀️",
        'Clouds': "☁️"
    }
    weather_icon = weather_icons.get(weather_desc, "❓")
    
    print(f"Weather Icon: {weather_icon}")
    return weather_icon
# Replace 'YOUR_API_KEY' with your actual API key from OpenWeatherMap


# Replace 'Brekkeveien 19, Oslo' with your desired location
city = 'Bergen'

if __name__ == '__main__':
    
    get_weather(city)