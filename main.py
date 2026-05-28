import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os
from dotenv import load_dotenv

# LOAD ENV VARIABLES
load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

# WINDOW
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("500x650")
root.config(bg="#1e1e2f")

# TITLE
title = tk.Label(
    root,
    text="Weather App",
    font=("Arial", 28, "bold"),
    bg="#1e1e2f",
    fg="white"
)
title.pack(pady=20)

# CITY ENTRY
city_entry = tk.Entry(
    root,
    font=("Arial", 18),
    width=20,
    justify="center"
)
city_entry.pack(pady=10)

# WEATHER ICON
icon_label = tk.Label(root, bg="#1e1e2f")
icon_label.pack()

# RESULT LABEL
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 16),
    bg="#1e1e2f",
    fg="white",
    justify="left"
)
result_label.pack(pady=20)

# FUNCTION
def get_weather():
    city = city_entry.get()

    if city == "":
        messagebox.showerror("Error", "Please enter a city name")
        return

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found")
            return

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        # WEATHER ICON
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        icon_response = requests.get(icon_url)
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)

        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        result = (
            f"City: {city}\n\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Condition: {condition.title()}\n"
            f"Wind Speed: {wind_speed} m/s"
        )

        result_label.config(text=result)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# BUTTON
search_button = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 16, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    command=get_weather
)
search_button.pack(pady=20)

# RUN
root.mainloop()