import streamlit as st
from datetime import datetime


st.set_page_config(layout="wide")


st.title("ExploreWise")
st.markdown("*Creating travel plans has never been easier*")

col1, col2 = st.columns(2)
container1 = col1.container()
container2 = col2.container()

container1_col1, container1_col2 = container1.columns(2)

source = container1_col1.text_input("Starting City", value="New York")
destination = container1_col2.text_input("Destination City", value="San Fransisco")

start_date = container1_col1.date_input("Trip Start", min_value=datetime.now())
duration = container1_col2.number_input("Trip Duration (Days)", min_value=1, max_value=15, value=1)

currency = container1_col1.selectbox("Currency", options=['USD (US Dollar)', 'INR (Indian Rupee)', 'EUR (Euro)', 'GBP (British Pound)', 'CAD (Canadian Dollar)', 'JPY (Japanese Yen)', 'AUD (Australian Dollar)'])
budget = container1_col2.number_input("Budget")

people = container1_col2.number_input("Number of Travelers", min_value=1, max_value=20, value=1)
diet = container1_col1.radio("Preferred Diet", options=['All', 'Vegetarian', 'Vegan'], horizontal=True)

col1.divider()

if col1.button("Generate Itinerary"):
    # generate itinerary dict
    # create persistent list of visited places
    pass
