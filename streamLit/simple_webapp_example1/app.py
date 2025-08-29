# app.js

import streamlit as st

import streamlit as st

# Title of the app
st.title("Simple Interactive Menu App")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select a Page",
    ["Home", "Data Analysis", "About"]
)

# Menu logic
if menu == "Home":
    st.header("Welcome to the Home Page")
    st.write("This is a basic interactive menu using Streamlit.")

elif menu == "Data Analysis":
    st.header("Data Analysis Page")
    st.write("Upload your data and perform analysis.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

elif menu == "About":
    st.header("About")
    st.write("This app is built with Streamlit.")



    