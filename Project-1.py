import requests, json, datetime, customtkinter as tk
from tkintermapview import *
from tkvideo import *

markers = []

cityData = {}

cities = ["Hihya", "Zagazig", "Cairo", "Alexandria", "Ismailia", "Minya", "Aswan", "El-Tor", "Luxor", "Hurghada",
"Tanta", "Sharm el Sheikh", "Al ‘Arīsh", "Marsá Maţrūḩ", "Port Said", "Damietta", "Siwa", "Suez", "Sohag",
"Al Mansurah", "Nuweiba", "Al Fayyum", "Giza", "Talkha"]

about = "{}- Name: {}, Email: {}, Phone: {}"

marker_click = False

json_result = [{"date": [0,0,0]}]

write = False

def update_event():

    root.after(500, update_event)

def legend_event(marker):
    for marker in markers:
        if marker.enter == True:
            marker_click = True
            break
        else:
            marker_click = False
    print(marker_click)
    if marker_click == True:
        city = cityData[marker.text]
        print(f"COLLIDED {city}")
        name_text = f"{city[0]}"
        temp_text = f"Temperature: {city[3]}°C"
        pollution_text = f"Air quality: {city[6]}"

        legend_name.configure(True, text=name_text)
        legend_temp.configure(True, text=temp_text)
        legend_pollution.configure(True, text=pollution_text)
    else:
        legend_name.configure(True, text="")
        legend_temp.configure(True, text="")
        legend_pollution.configure(True, text="")

def get_weather(city):
    global write
    time = datetime.datetime.now()

    file = open("res\data.json", "r")
    src = file.read()
    file.close()

    json_object = json.loads(src)
    date = json_object[0]["date"]
    
    json_cities = json_object[1:]

    if date[2] == time.day and date[1] == time.month:
        write = False
        for i in json_cities:
            if i["name"] == city:
                location = i["position"]
                country = i["country"]
                temp = i["temp"]
                weather = i["weather"]
                description = i["description"]
                pollution = i["pollution"]

        final_result = (city,location,country,temp,weather,description,pollution)
        return final_result
    else:
        write = True
        json_data = {
            "name": "",
            "country": "",
            "position": [],
            "temp": 0,
            "weather": "",
            "description": "",
            "pollution": "",
        }

        url1 = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
        url2 = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'
        url3 = 'https://api.api-ninjas.com/v1/city?name={}'
        api_key1 = '605777afd3d72eb5be67234616710a0c'
        api_key2 = 'a3Zq8f6N+Nt1opb9WTsvCQ==E5q8VqojyqkIEB11'
        url_api = requests.get(url1.format(city,api_key1))
        if url_api:
            jsonData = url_api.json()
            lon, lat = (jsonData['coord']['lon'], jsonData['coord']['lat'])
            location = (lat, lon)
            country = jsonData['sys']['country']
            temp_klv = jsonData['main']['temp']
            temp_celcius = int(temp_klv - 273.15)
            weather = jsonData['weather'][0]['main']
            pressure = jsonData['main']['pressure']
            description = jsonData['weather'][0]['description']
            url_api = requests.get(url2.format(lat,lon,api_key1))
            if url_api:
                jsonData = url_api.json()
                data = jsonData['list'][0]['components']
                air = jsonData['list'][0]['main']['aqi']
                pollution = ''
                if air == 1:
                    pollution = 'Good'
                elif air == 2:
                    pollution = 'Fair'
                elif air == 3:
                    pollution = 'Moderate'
                elif air == 4:
                    pollution = 'Poor'
                elif air == 5:
                    pollution = 'Very Poor'

            final_result = (city,location,country,temp_celcius,weather,description,pollution)

            json_data["name"] = city
            json_data["country"] = country
            json_data["position"] = location
            json_data["temp"] = temp_celcius
            json_data["weather"] = weather
            json_data["description"] = description
            json_data["pollution"] = pollution
            
            json_result[0]["date"][0] = time.year
            json_result[0]["date"][1] = time.month
            json_result[0]["date"][2] = time.day
            json_result.append(json_data)

            return final_result
        else:
            return None

for i in cities:
    data = get_weather(i)
    if data:
        cityData[data[0]] = data
    else:
        print(f"Error: {i}")

if write == True:
    json_object = json.dumps(json_result, indent=4)

    with open("res\data.json", "w") as outfile:
        outfile.write(json_object)

tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")
root = tk.CTk()
root.resizable(True, True)
root.title("Project-1")
root.geometry("900x700")

tab = tk.CTkTabview(root)
tab.pack(padx=20, pady=20, fill="y")

tab.add("Weather")
tab.add("Climate changes")
tab.add("Ways to solve")
tab.add("Game")
tab.add("About Us")

#### MAP ####
map = TkinterMapView(tab.tab("Weather"), width=800, height=600, corner_radius=0)
map.place()
map.set_position(26.7907965, 29.6267872)
map.add_left_click_map_command(legend_event)
map.set_zoom(9)

for i in cityData:
    marker = map.set_marker(cityData[i][1][0], cityData[i][1][1], cityData[i][0])
    if cityData[i][6] == 'Good':
        color = "lightgreen"
    elif cityData[i][6] == 'Fair':
        color = "green"
    elif cityData[i][6] == 'Moderate':
        color = "darkgreen"
    elif cityData[i][6] == 'Poor':
        color = "lightgray"
    elif cityData[i][6] == 'Very Poor':
        color = "black"
    marker.marker_color_circle = color
    marker.command = legend_event
    markers.append(marker)


map.pack(side=tk.LEFT)

frame1 = tk.CTkFrame(tab.tab("Weather"))
frame1.pack(padx=10, pady=0, side=tk.LEFT, fill="y", expand=False)

legend_name = tk.CTkLabel(frame1, text="", font=("arial", 32))
legend_name.pack(padx=20, pady=20)

legend_temp = tk.CTkLabel(frame1, text="", font=("arial", 24))
legend_temp.pack(padx=20, pady=20)

legend_pollution = tk.CTkLabel(frame1, text="", font=("arial", 24))
legend_pollution.pack(padx=20, pady=20)

### Climate changes ###
textbox = tk.CTkTextbox(tab.tab("Climate changes"), width=700, height=500, font=("arial", 32))
textbox.grid(row=0, column=0)
entry = tk.CTkEntry(root)

textbox.insert("0.0", "Egypt is highly vulnerable to climate change, with projected increase in heat waves, dust storms, storms along the Mediterranean coast and extreme weather events. Stronger warming has been documented over the past 30 years, with average annual temperatures increasing by 0.53 degree Celsius per decade.  The country’s climate risks are and will impact the younger generations of today.\nCrucially, the awareness of the importance of climate change action both domestically and at the global level is fast increasing in Egypt. The country is at a turning point in its commitment and action to tackle the consequences of climate change. In the 2030 Vision and sustainable development strategy, Egypt has also made commitments to integrate climate change in national development policies and to progressively green its budget across sectors.\nUNICEF will be at COP27 to ensure that the climate crisis is recognized as a crisis for children and their rights, to promote approaches to decrease climate risk for those who are most vulnerable, and to support children and young people’s participation in COP27 as part of efforts to support children and young people’s participation in climate-related decision-making.")  # insert at line 0 character 0
text = textbox.get("0.0", "end")  # get text from line 0 character 0 till the end

textbox.configure(state="disabled")  # configure textbox to be read-only

#### About Us ####
frame2 = tk.CTkFrame(tab.tab("About Us")) 
frame2.pack(padx=10, pady=5, fill="both")

first_name = tk.CTkLabel(frame2, text=about.format(1,"Abdalah","alsragbode@gmail.com","01220767786"), font=("arial", 16))
first_name.pack(padx=20, pady=20)

second_name = tk.CTkLabel(frame2, text=about.format(2,"","",""), font=("arial", 16))
second_name.pack(padx=20, pady=20)

third_name = tk.CTkLabel(frame2, text=about.format(3,"","",""), font=("arial", 16))
third_name.pack(padx=20, pady=20)

fourth_name = tk.CTkLabel(frame2, text=about.format(4,"","",""), font=("arial", 16))
fourth_name.pack(padx=20, pady=20)

#### Game ####
frame3 = tk.CTkFrame(tab.tab("Game"))
frame3.pack(padx=10, pady=0, side=tk.LEFT, fill="both", expand=True)

root.after(500, update_event)
root.mainloop()