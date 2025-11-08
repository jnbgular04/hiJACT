# Save this as typhoon_demo.py and run with: streamlit run typhoon_demo.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from math import radians, cos, sin, asin, sqrt

# --- Sample Typhoon Data ---
typhoon_name = "Goring"
typhoon_lat = 13.5       # Typhoon center latitude
typhoon_lon = 123.0      # Typhoon center longitude
wind_speed = 140         # km/h
pressure = 950           # hPa

# --- Sample User Input ---
st.title("Philippine Typhoon Safety Map Demo")

user_location = st.text_input("Enter your city/location:", "Albay")
# For demo purposes, we use fixed coordinates for Albay
user_lat = 13.2
user_lon = 123.7

# --- Haversine Formula to Compute Distance ---
def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

distance_km = haversine(user_lat, user_lon, typhoon_lat, typhoon_lon)

# --- Generate Adaptive Safety Tip ---
if distance_km < 100 and wind_speed > 120:
    tip = "Evacuate immediately! Secure your belongings."
elif distance_km < 200 and wind_speed > 80:
    tip = "Secure belongings, charge devices, monitor updates."
elif distance_km < 400:
    tip = "Prepare emergency supplies."
else:
    tip = "Stay alert and monitor updates."

st.markdown(f"### Safety Tip for {user_location}")
st.info(tip)

st.markdown(f"**Distance to Typhoon {typhoon_name}:** {distance_km:.1f} km")
st.markdown(f"**Typhoon Wind Speed:** {wind_speed} km/h")
st.markdown(f"**Typhoon Pressure:** {pressure} hPa")

# --- Create Folium Map ---
m = folium.Map(location=[user_lat, user_lon], zoom_start=6)

# Typhoon marker
folium.Marker(
    [typhoon_lat, typhoon_lon],
    popup=f"Typhoon {typhoon_name}\nWind: {wind_speed} km/h\nPressure: {pressure} hPa",
    icon=folium.Icon(color='red')
).add_to(m)

# User location marker
folium.Marker(
    [user_lat, user_lon],
    popup=f"Your Location: {user_location}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Line between user and typhoon
folium.PolyLine(
    [[user_lat, user_lon], [typhoon_lat, typhoon_lon]],
    color="orange", weight=2
).add_to(m)

# Display map in Streamlit
st_folium(m, width=700, height=500)
