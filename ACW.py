import tkinter as tk
from tkinter import ttk
from geopy.geocoders import Nominatim
import requests

def get_weather(city, country_code, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": f"{city},{country_code}",
        "appid": api_key,
        "units": "metric",  # You can change this to "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data["list"]
        else:
            return None

    except Exception as e:
        return None

def display_weather_details(weather_data):
    details_text = ""
    current_date = None

    for forecast in weather_data:
        timestamp = forecast["dt_txt"]
        date, time = timestamp.split(" ")
        temperature = forecast["main"]["temp"]
        weather_description = forecast["weather"][0]["description"].capitalize()
        weather_condition = forecast["weather"][0]["main"]

        emoji = get_emoji_based_on_condition(weather_condition)

        if date != current_date:
            details_text += f"\n{date}:\n"
            current_date = date

        details_text += f"  {time}: {temperature}°C, {emoji} {weather_description}\n"

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, details_text)
    result_text.config(state=tk.DISABLED)

def get_emoji_based_on_condition(weather_condition):
    if "clear" in weather_condition.lower():
        return "☀️"
    elif "cloud" in weather_condition.lower():
        return "☁️"
    elif "rain" in weather_condition.lower():
        return "🌧️"
    elif "snow" in weather_condition.lower():
        return "❄️"
    else:
        return "🌈"

def toggle_dark_light_mode():
    current_bg = root.cget("bg")
    if current_bg == "white":
        root.configure(bg="black")
        label.configure(foreground="purple")
        result_text.configure(foreground="purple", bg="black")
        dark_light_button.configure(text="Light Mode")
        label.configure(foreground="purple", bg="white")
    else:
        root.configure(bg="white")
        label.configure(foreground="black")
        result_text.configure(foreground="black", bg="white")
        dark_light_button.configure(text="Dark Mode")

def on_search():
    location = location_entry.get()
    api_key = "57224bcc0be31d5f800345062e2cf689"

    if location:
        # Use geopy to get city and country code
        geolocator = Nominatim(user_agent="weather_app")
        location_info = geolocator.geocode(location)

        if location_info:
            city = location_info.address.split(",")[0]
            country_code = location_info.address.split(",")[-1].strip()
            weather_data = get_weather(city, country_code, api_key)

            if weather_data:
                display_weather_details(weather_data)
                return
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Error fetching weather data.")
    result_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Akaansh's Custom Weather")
root.configure(bg="white")

# Create and configure widgets
label = ttk.Label(root, text="5-Day Weather Forecast:", foreground="blue")
label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

location_entry = ttk.Entry(root)
location_entry.grid(row=1, column=0, padx=10, pady=10)

search_button = ttk.Button(root, text="Get Weather", command=on_search)
search_button.grid(row=1, column=1, padx=10, pady=10)

dark_light_button = ttk.Button(root, text="Dark Mode", command=toggle_dark_light_mode)
dark_light_button.grid(row=2, column=0, padx=10, pady=10)

# Create a Text widget for displaying results
result_text = tk.Text(root, wrap="word", height=10, width=50, foreground="black", bg="white", state=tk.DISABLED)
result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Make the Text widget scrollable
scrollbar = ttk.Scrollbar(root, orient="vertical", command=result_text.yview)
scrollbar.grid(row=3, column=2, sticky="ns")
result_text.configure(yscrollcommand=scrollbar.set)

# Run the main loop
root.mainloop()
