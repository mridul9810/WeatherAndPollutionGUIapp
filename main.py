import tkinter as tk
from PIL import ImageTk, Image
import requests
import os


weather_key = os.environ.get('WAETHER_API_KEY')


def get_weather(city):
    key = weather_key
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'appid': key, 'q': city, 'units': 'metric'}
    ans = requests.get(url, params=params)
    d = ans.json()

    # adding weather details to label1
    label1['text'] = weather_format_response(d)


def get_air_pollution(lat, lon):
    key = weather_key
    url = 'http://api.openweathermap.org/data/2.5/air_pollution'
    params = {'appid': key, 'lat': lat, 'lon': lon}
    ans = requests.get(url, params=params)
    d = ans.json()

    label2['text'] = pollution_format_response(d)


def weather_format_response(d):
    try:
        name = d['name']
        desc = d['weather'][0]['description']
        temp = d['main']['temp']
        humidity = d['main']['humidity']
        visibility = d['visibility']

        final_str = 'City: {} \nDescription: {} \nTemperature: {} \nHumidity:{} \nVisibility: {}'\
            .format(name, desc, temp, humidity, visibility)

        # to get the pollution details
        lat = d['coord']['lat']
        lon = d['coord']['lon']

        get_air_pollution(lat, lon)

    except Exception:
        final_str = """Please check the name
of the city that you have 
entered !"""

    return final_str


def pollution_format_response(d):

    aqi = {1: 'Good',
           2: 'Fair',
           3: 'Moderate',
           4: 'Poor',
           5: 'Very Poor'}

    aqi_value = d['list'][0]['main']['aqi']

    if aqi_value in aqi:
        final_str = 'Pollution Status: {}'.format(aqi[aqi_value])
    else:
        final_str = "Error"

    return final_str


HEIGHT = 600
WIDTH = 700

root = tk.Tk()

root.title('Weather And Pollution GUI Application')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Adding an image in the background using pillow library
bg_image = ImageTk.PhotoImage(Image.open('3.jpg'))
label_image = tk.Label(root, image=bg_image)
label_image.place(relheight=1, relwidth=1)


# Creating the upper frame in which i will put my entry box and button
frame = tk.LabelFrame(root, bg='black', bd=7)
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

# Entry Box
entry = tk.Entry(frame, font=('Arial', 15))
entry.place(relwidth=0.74, relheight=1)

# Button
button = tk.Button(frame, text='Get Weather \n& Pollution', font=('Arial', 13), command=lambda: get_weather(entry.get()))
button.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)


# Create a lower frame
lower_frame = tk.LabelFrame(root, bd=10, bg='black')
lower_frame.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.7)

# Label to display weather details
label1 = tk.Label(lower_frame, font=('Arial', 15), anchor='nw', justify='left')
label1.place(relx=0, rely=0, relwidth=0.50, relheight=1)

# Label2 to display pollution details
label2 = tk.Label(lower_frame, font=('Arial', 15), anchor='nw', justify='left')
label2.place(relx=0.51, rely=0, relwidth=0.49, relheight=1)


root.mainloop()
