import streamlit as st
import sqlite3
import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Database setup ---
def init_db():
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            legal_issue TEXT
        )
    ''')
    # Insert sample data 
    
    sample_data = [
        ("David Levi", 42, "Real Estate"),
        ("Noa Cohen", 35, "Family"),
        ("Itamar Ben-Ari", 60, "Wills and Inheritance"),
        ("Yael Mizrahi", 29, "Contracts"),
        ("Avi Dahan", 45, "Criminal"),
        ("Rina Azulay", 38, "Family"),
        ("Daniel Kadosh", 50, "Wills and Inheritance"),
        ("Lior Avrahami", 33, "Real Estate"),
        ("Maya Segal", 41, "Family"),
        ("Eliad Shlomo", 28, "Contracts")
        ]
    c.executemany("INSERT INTO clients (name, age, legal_issue) VALUES (?, ?, ?)", sample_data)
    
    conn.commit()
    
    conn.close()

# --- Add new client ---
def add_client(name, age, issue):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("INSERT INTO clients (name, age, legal_issue) VALUES (?, ?, ?)", (name, age, issue))
    conn.commit()
    conn.close()

# --- Load data ---
def load_data():
    conn = sqlite3.connect("clients.db")
    df = pd.read_sql_query("SELECT * FROM clients", conn)
    conn.close()
    return df

# --- GPT Analysis ---
def analyze_data(df):
    from openai import OpenAI
    client = OpenAI()

    prompt = f"""
    Here is a data table of clients in a law office:
    {df.to_markdown()}
    
    Please provide an analysis of:
    1. What is the average age?
    2. Which legal fields are most common?
    3. Is there an age pattern by legal field?
    """

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )
    return response.output_text

def chatbot_response(user_input, df):
    prompt = f"""
    Answer the following question based on the law office's data:
    {df.to_markdown()}
    
    Question: {user_input}
    """
    from openai import OpenAI
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )
    return response.output_text

# ---------- Streamlit UI ----------
init_db()
st.title("📊 LegalSmart - Legal Client Management")

# Add new client
st.header("➕ Add New Client")
with st.form("new_client_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=120)
    issue = st.selectbox("Legal Issue", ["Family", "Wills and Inheritance", "Real Estate", "Contracts", "Criminal"])
    submitted = st.form_submit_button("Save")
    if submitted:
        add_client(name, age, issue)
        st.success("✅ Client added successfully!")

# View table
st.header("📁 All Cases")
df = load_data()
st.dataframe(df)

# GPT Analysis
st.header("📈 Analysis with GPT")
if st.button("Run Analysis"):
    analysis = analyze_data(df)
    st.markdown(analysis)

# Chatbot
st.header("🤖 Ask LegalSmart")
user_q = st.text_input("Ask a question about the data:")
if st.button("Send"):
    if user_q.strip():
        response = chatbot_response(user_q, df)
        st.markdown(response)