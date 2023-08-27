import folium, requests

map = folium.Map(location=[30.667390, 31.591890], zoom_start=12, zoom_max=9, zoom_min=15)
cities = ["hihya", "zagazig", "cairo", "alexandria", "ismailia", "giza", "minya", "aswan", "el-Tor", "luxor", "hurghada",
"tanta", "matrouh", "naama bay", "Al ‘Arīsh", "Marsá Maţrūḩ", "Port Said", "damietta", "siwa", "suez", "sohag", "Ţalkhā",
"Al Mansurah", "nuweiba"]

def get_weather(city):
    url1 = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    url2 = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'
    api_key = '605777afd3d72eb5be67234616710a0c'
    url_api = requests.get(url1.format(city,api_key))
    if url_api:
        jsonData = url_api.json()
        lon, lat = (jsonData['coord']['lon'], jsonData['coord']['lat'])
        location = (lat, lon)
        city = jsonData['name']
        country = jsonData['sys']['country']
        temp_klv = jsonData['main']['temp']
        temp_celcius = temp_klv - 273.15
        weather = jsonData['weather'][0]['main']
        pressure = jsonData['main']['pressure']
        description = jsonData['weather'][0]['description']
        url_api = requests.get(url2.format(lat,lon,api_key))
        jsonData = url_api.json()
        data = jsonData['list'][0]['components']
        air = jsonData['list'][0]['main']['aqi']

        final_result = (city,location,country,temp_celcius,weather,pressure,description,air)
        return final_result
    else:
        return None

for i in cities:
    weather_data = get_weather(i)

    if weather_data:
        pollution = ""
        color = ""
        if weather_data[7] == 1:
            pollution = 'Good'
            color = "lightgreen"
        elif weather_data[7] == 2:
            pollution = 'Fair'
            color = "green"
        elif weather_data[7] == 3:
            pollution = 'Moderate'
            color = "darkgreen"
        elif weather_data[7] == 4:
            pollution = 'Poor'
            color = "lightgray"
        elif weather_data[7] == 5:
            pollution = 'Very Poor'
            color = "black"
        pop = "City: {} {}\nTemperature: {}°C\nPollution: {}"
        folium.Marker(
            location=[weather_data[1][0], weather_data[1][1]],
            popup=folium.Popup(pop.format(weather_data[0], weather_data[2], int(weather_data[3]), pollution)),
            icon=folium.Icon(color=color, icon="info-sign"),
        ).add_to(map)

        folium.Circle(
            location=[weather_data[1][0], weather_data[1][1]],
            radius=12000,
            fill=True,
            color = color,
            fill_opacity=0.7
        ).add_to(map)

folium.Marker(
    location=[30.669496, 31.581901],
    popup="بيت مروان الرخم",
    icon=folium.Icon(color="green"),
).add_to(map)

map.save("map.html")