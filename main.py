# Modules used
import streamlit as st
import plotly.express as px
from backend import get_data


# Add title, text input, slider, select box, and sub header
st.title("Weather forecast for the next few Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select number of forecasted days.")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")


if place:

    try:
        # Get the temperature/sky data
        filtered_data = get_data(place, days)

        if option == "Temperature":
            # Create a temperature plot
            temperatures = [dict["main"]["temp"]/10 for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            # Create set of weather images
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=85)

    except KeyError:
        # Error message
        st.write("<p style='color:red; font-size:20px;'>Place does not exist</p>", unsafe_allow_html=True)