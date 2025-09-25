import sqlite3
import pandas as pd
import streamlit as st

# Title and description
st.title("User Information App")
st.write("This app allows you to submit a name and age, stores them in a SQLite database, and displays all entries.")