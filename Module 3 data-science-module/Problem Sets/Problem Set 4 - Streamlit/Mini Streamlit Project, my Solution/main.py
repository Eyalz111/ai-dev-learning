# Standard library imports
import os
import sqlite3
import time
import random
import hashlib
from datetime import datetime, timedelta

# Third-party imports
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import anthropic
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Advanced Configuration for Overkill Solution
CLAUDE_MODELS = {
    "latest": "claude-3-5-sonnet-20241022",  # Current latest (will update when newer available)
    "haiku": "claude-3-5-haiku-20241022",    # Faster, cheaper
    "opus": "claude-opus-4-1-20250805",      # Most powerful - Claude Opus 4.1
    "fallback": "claude-3-haiku-20240307"    # Emergency fallback
}

# Cache configuration
CACHE_TTL = 3600  # 1 hour cache
MAX_CACHE_ENTRIES = 100

# Rate limiting configuration
MAX_REQUESTS_PER_MINUTE = 50
REQUEST_WINDOW = 60  # seconds

# Initialize session state for advanced features
if 'request_history' not in st.session_state:
    st.session_state.request_history = []
if 'claude_cache' not in st.session_state:
    st.session_state.claude_cache = {}
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "latest"

# Initialize Claude API client
try:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ מפתח Claude API לא נמצא. אנא הגדר את ANTHROPIC_API_KEY בקובץ .env")
        client = None
    else:
        client = anthropic.Anthropic(api_key=api_key)
except Exception as e:
    st.error(f"⚠️ שגיאה באתחול Claude API: {str(e)}")
    client = None

# Advanced Utility Functions for Overkill Solution

def generate_cache_key(prompt, model, max_tokens, temperature):
    """Generate a unique cache key for the request"""
    content = f"{prompt}_{model}_{max_tokens}_{temperature}"
    return hashlib.md5(content.encode()).hexdigest()

def is_rate_limited():
    """Check if we're hitting rate limits"""
    now = datetime.now()
    # Clean old requests
    st.session_state.request_history = [
        req_time for req_time in st.session_state.request_history
        if now - req_time < timedelta(seconds=REQUEST_WINDOW)
    ]
    
    return len(st.session_state.request_history) >= MAX_REQUESTS_PER_MINUTE

def add_request_to_history():
    """Add current request to history for rate limiting"""
    st.session_state.request_history.append(datetime.now())

def get_from_cache(cache_key):
    """Get response from cache if available and not expired"""
    if cache_key in st.session_state.claude_cache:
        cached_item = st.session_state.claude_cache[cache_key]
        if datetime.now() - cached_item['timestamp'] < timedelta(seconds=CACHE_TTL):
            return cached_item['response']
        else:
            # Remove expired cache
            del st.session_state.claude_cache[cache_key]
    return None

def add_to_cache(cache_key, response):
    """Add response to cache with timestamp"""
    # Limit cache size
    if len(st.session_state.claude_cache) >= MAX_CACHE_ENTRIES:
        # Remove oldest entry
        oldest_key = min(st.session_state.claude_cache.keys(), 
                        key=lambda k: st.session_state.claude_cache[k]['timestamp'])
        del st.session_state.claude_cache[oldest_key]
    
    st.session_state.claude_cache[cache_key] = {
        'response': response,
        'timestamp': datetime.now()
    }

@st.cache_data(ttl=CACHE_TTL, max_entries=MAX_CACHE_ENTRIES)
def load_data_cached():
    """Cached version of load_data for better performance"""
    return load_data()

def get_model_info(model_key):
    """Get information about the selected model"""
    model_info = {
        "latest": {"name": "Claude 3.5 Sonnet (Latest)", "speed": "Fast", "quality": "Excellent", "cost": "Medium"},
        "haiku": {"name": "Claude 3.5 Haiku", "speed": "Very Fast", "quality": "Good", "cost": "Low"},
        "opus": {"name": "Claude Opus 4.1", "speed": "Slower", "quality": "Best", "cost": "High"},
        "fallback": {"name": "Claude 3 Haiku (Fallback)", "speed": "Very Fast", "quality": "Good", "cost": "Low"}
    }
    return model_info.get(model_key, model_info["latest"])

# Advanced Claude API Call with Caching and Rate Limiting
def call_claude_with_retry(prompt, max_tokens=2000, temperature=0.3, max_retries=3):
    """Advanced Claude API call with caching, rate limiting, and retry logic"""
    
    # Validate inputs
    if not isinstance(prompt, str):
        return f"שגיאה: הטקסט שנשלח ל-Claude חייב להיות מחרוזת, קיבלנו: {type(prompt)}"
    
    if not prompt.strip():
        return "שגיאה: לא ניתן לשלוח טקסט ריק ל-Claude"
    
    # Ensure we have a valid client
    if client is None:
        return "שגיאה: לא הצלחנו להתחבר ל-Claude API. בדוק את מפתח ה-API שלך"
    
    # Get selected model
    selected_model = CLAUDE_MODELS[st.session_state.selected_model]
    
    # Generate cache key
    cache_key = generate_cache_key(prompt, selected_model, max_tokens, temperature)
    
    # Check cache first
    cached_response = get_from_cache(cache_key)
    if cached_response:
        st.info("📋 תשובה מהמטמון (מהיר יותר!)")
        return cached_response
    
    # Check rate limiting
    if is_rate_limited():
        return f"⚠️ הגעת למגבלת הבקשות ({MAX_REQUESTS_PER_MINUTE} בקשות לדקה). אנא המתן מעט."
    
    # Add request to history for rate limiting
    add_request_to_history()
    
    # Show model info
    model_info = get_model_info(st.session_state.selected_model)
    st.info(f"🤖 משתמש במודל: {model_info['name']} | מהירות: {model_info['speed']} | איכות: {model_info['quality']}")
    
    # Create progress bar for better UX
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for attempt in range(max_retries):
        try:
            # Update progress
            progress_bar.progress((attempt + 1) / max_retries)
            status_text.text(f"מנסה להתחבר ל-Claude... ניסיון {attempt + 1}/{max_retries}")
            
            # Make API call with selected model
            response = client.messages.create(
                model=selected_model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": str(prompt)}]
            )
            
            # Clear progress indicators on success
            progress_bar.empty()
            status_text.empty()
            
            # Validate response structure
            if hasattr(response, 'content') and len(response.content) > 0:
                if hasattr(response.content[0], 'text'):
                    result = response.content[0].text
                    # Cache the successful response
                    add_to_cache(cache_key, result)
                    return result
                else:
                    result = str(response.content[0])
                    add_to_cache(cache_key, result)
                    return result
            else:
                return "שגיאה: תגובה לא תקינה מ-Claude"
                
        except Exception as e:
            error_str = str(e)
            
            # Handle specific error types with advanced retry logic
            if "overloaded" in error_str.lower() or "529" in error_str:
                if attempt < max_retries - 1:
                    # Progressive model fallback strategy
                    if attempt == 0 and st.session_state.selected_model == "latest":
                        st.warning("🔄 מודל עמוס, מנסה עם Opus 4.1 (איכות גבוהה)...")
                        selected_model = CLAUDE_MODELS["opus"]
                    elif attempt == 1:
                        st.warning("🔄 מנסה עם Haiku (מהיר)...")
                        selected_model = CLAUDE_MODELS["haiku"]
                    elif attempt == 2:
                        st.warning("🔄 מנסה עם מודל גיבוי...")
                        selected_model = CLAUDE_MODELS["fallback"]
                    
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    st.warning(f"שרת Claude עמוס, מנסה שוב בעוד {wait_time:.1f} שניות...")
                    time.sleep(wait_time)
                    continue
                else:
                    progress_bar.empty()
                    status_text.empty()
                    fallback_response = "מצטערים, כל מודלי Claude עמוסים כרגע. הנה ניתוח בסיסי במקום:\n\n" + get_basic_analysis()
                    add_to_cache(cache_key, fallback_response)
                    return fallback_response
            elif "api_key" in error_str.lower() or "authentication" in error_str.lower():
                return "שגיאה: בעיה באימות ה-API. בדוק את מפתח ה-API שלך"
            elif "rate_limit" in error_str.lower():
                return "⚠️ הגעת למגבלת הקצב של Claude API. אנא המתן מעט לפני הבקשה הבאה."
            elif "not_found_error" in error_str.lower() or "404" in error_str:
                if attempt < max_retries - 1:
                    st.warning(f"🔄 מודל {selected_model} לא זמין, מנסה עם מודל אחר...")
                    selected_model = CLAUDE_MODELS["haiku"]  # Fallback to most reliable
                    continue
                else:
                    return f"⚠️ המודל שנבחר אינו זמין. אנא בחר מודל אחר או נסה שוב מאוחר יותר."
            else:
                progress_bar.empty()
                status_text.empty()
                return f"שגיאה בחיבור ל-Claude: {error_str}"
    
    # Clean up progress indicators if we get here
    progress_bar.empty()
    status_text.empty()
    return "לא הצלחנו להתחבר לשרת Claude לאחר מספר ניסיונות."

def get_basic_analysis():
    """Fallback analysis when Claude is unavailable"""
    try:
        df = load_data()
        if len(df) == 0:
            return "אין נתונים זמינים לניתוח"
            
        total_clients = len(df)
        avg_age = df['age'].mean()
        issue_counts = df['legal_issue'].value_counts()
        most_common_issue = issue_counts.index[0] if len(issue_counts) > 0 else "לא זמין"
    except Exception as e:
        return f"שגיאה בטעינת הנתונים: {str(e)}"
    
    return f"""
📊 **ניתוח בסיסי של נתוני הלקוחות:**

**סטטיסטיקות כלליות:**
- סה"כ לקוחות: {total_clients}
- גיל ממוצע: {avg_age:.1f}
- התחום הנפוץ ביותר: {most_common_issue}

**התפלגות תחומים משפטיים:**
{chr(10).join([f"- {issue}: {count} לקוחות ({count/total_clients*100:.1f}%)" for issue, count in issue_counts.items()])}

**טווח גילאים:**
- הצעיר ביותר: {df['age'].min()}
- המבוגר ביותר: {df['age'].max()}
- חציון: {df['age'].median()}
"""

# Streamlit app starts here

# Create Database Initialization Function
def init_db():
    """Initialize the database and create clients table if it doesn't exist"""
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            legal_issue TEXT NOT NULL
        )
    ''')
    
    # Check if table is empty and add sample data if it is
    cursor.execute("SELECT COUNT(*) FROM clients")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Sample data matching the project requirements
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
        
        cursor.executemany(
            "INSERT INTO clients (name, age, legal_issue) VALUES (?, ?, ?)",
            sample_data
        )
        
    conn.commit()
    conn.close()

# Add Client Function
def add_client(name, age, issue):
    """Add a new client to the database"""
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO clients (name, age, legal_issue) VALUES (?, ?, ?)",
        (name, age, issue)
    )
    
    conn.commit()
    conn.close()

#  Load Data Function
def load_data():
    """Load all clients from the database into a pandas DataFrame"""
    conn = sqlite3.connect('clients.db')
    df = pd.read_sql_query("SELECT * FROM clients", conn)
    conn.close()
    return df

# Initialize database when app starts
init_db()

# Step 7: Enhanced Data Analysis Function with Claude
def analyze_data(df):
    """Use Claude to provide sophisticated analysis of client data"""
    try:
        # Validate input
        if df is None or len(df) == 0:
            return "אין נתונים זמינים לניתוח"
        
        # Prepare detailed statistics safely
        total_clients = len(df)
        age_stats = df['age'].describe()
        issue_counts = df['legal_issue'].value_counts().to_dict()
        
        # Create a more detailed prompt with context
        prompt = f"""
You are a legal analytics expert analyzing client data for a law firm. 
Please provide a comprehensive analysis in Hebrew.

Dataset Overview:
- Total clients: {total_clients}
- Columns: {df.columns.tolist()}

Client Data (Full Table):
{df.to_string()}

Age Statistics:
{age_stats.to_string()}

Legal Issue Distribution:
{issue_counts}

Please provide a detailed analysis including:

1. **סטטיסטיקה תיאורית**
   - התפלגות גילאים מפורטת
   - ממוצע, חציון, סטיית תקן
   - זיהוי חריגים אם קיימים

2. **ניתוח תחומים משפטיים**
   - התחום השכיח ביותר ולמה זה משמעותי
   - האם יש תחומים שדורשים תשומת לב מיוחדת?
   - המלצות לשיפור השירות בתחומים השונים

3. **קורלציות ותובנות**
   - האם יש קשר בין גיל לסוג הבעיה המשפטית?
   - זיהוי דפוסים או מגמות בנתונים
   - תובנות עסקיות שיכולות לעזור למשרד

4. **המלצות אסטרטגיות**
   - איזה תחומים כדאי לחזק?
   - איזה קבוצות גיל חסרות ייצוג?
   - הצעות לשיפור השירות

Format the response with clear headers, bullet points, and use markdown for better readability.
Include specific numbers and percentages where relevant.
"""
        
        return call_claude_with_retry(prompt, max_tokens=2000, temperature=0.3)
        
    except Exception as e:
        return f"שגיאה בניתוח הנתונים: {str(e)}\n\nהנה ניתוח בסיסי במקום:\n\n{get_basic_analysis()}"

# Step 8: Enhanced Chatbot Response Function
def chatbot_response(user_input, df):
    """Sophisticated Q&A about client data using Claude"""
    try:
        # Validate inputs
        if not user_input or not user_input.strip():
            return "אנא הזן שאלה תקינה"
        
        if df is None or len(df) == 0:
            return "אין נתונים זמינים לענות על השאלה"
        
        # Prepare context safely
        total_clients = len(df)
        unique_issues = df['legal_issue'].unique().tolist()
        age_range = f"{df['age'].min()}-{df['age'].max()}"
        
        prompt = f"""
You are an intelligent legal assistant with access to a law firm's client database.
Answer questions in Hebrew based ONLY on the available data. Be precise and helpful.

Database Summary:
- Total Clients: {total_clients}
- Age Range: {age_range}
- Legal Areas: {', '.join(unique_issues)}

Full Client Database:
{df.to_string()}

Detailed Statistics:
- Age distribution: {df['age'].describe().to_dict()}
- Legal issues frequency: {df['legal_issue'].value_counts().to_dict()}

User Question: {user_input}

Instructions:
1. Answer specifically based on the data
2. Include relevant statistics and percentages
3. If the question requires calculations, show them
4. If the question is unrelated to the data, politely redirect
5. Use clear Hebrew with professional legal terminology where appropriate
6. Format numbers nicely (e.g., 45.5% not 0.455)
7. If relevant, suggest follow-up questions the user might find interesting

Respond in a conversational yet professional tone.
"""
        
        return call_claude_with_retry(prompt, max_tokens=1500, temperature=0.2)
        
    except Exception as e:
        return f"שגיאה בעיבוד השאלה: {str(e)}"

# Initialize database when app starts
init_db()

# Professional UI/UX Configuration
st.set_page_config(
    page_title="LegalSmart Pro - מערכת ניהול לקוחות משפטית",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for Professional UI/UX
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Typography */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.15);
    }
    
    /* Button Styles */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Primary Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Secondary Button */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #8b5cf6;
    }
    
    /* Form Styles */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        font-family: 'Inter', sans-serif;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Dataframe Styles */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        border-radius: 8px;
        border-left: 4px solid #10b981;
    }
    
    .stError {
        border-radius: 8px;
        border-left: 4px solid #ef4444;
    }
    
    .stWarning {
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
    }
    
    .stInfo {
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
    }
    
    /* Header Styles */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .metric-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Professional Header with Hero Section
st.markdown("""
    <div class="fade-in">
        <h1 class="main-title">⚖️ LegalSmart Pro</h1>
        <p class="subtitle">מערכת ניהול לקוחות משפטית מתקדמת עם בינה מלאכותית</p>
    </div>
""", unsafe_allow_html=True)

# Load data once for the entire app (cached version)
df = load_data_cached()

# Sidebar for Quick Stats and Navigation
with st.sidebar:
    st.markdown("### 🚀 הגדרות מתקדמות")
    
    # Model selector
    st.markdown("**🤖 בחירת מודל Claude:**")
    model_options = {
        "latest": "🔥 Claude 3.5 Sonnet (מומלץ)",
        "haiku": "⚡ Claude 3.5 Haiku (מהיר)",
        "opus": "💎 Claude Opus 4.1 (הטוב ביותר)"
    }
    
    selected_model = st.selectbox(
        "בחר מודל:",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=list(model_options.keys()).index(st.session_state.selected_model)
    )
    
    if selected_model != st.session_state.selected_model:
        st.session_state.selected_model = selected_model
        st.rerun()
    
    # Show model info
    model_info = get_model_info(st.session_state.selected_model)
    st.info(f"""
    **מידע על המודל:**
    - מהירות: {model_info['speed']}
    - איכות: {model_info['quality']}
    - עלות: {model_info['cost']}
    """)
    
    # Performance monitoring
    st.markdown("---")
    st.markdown("### 📈 ביצועים")
    
    cache_size = len(st.session_state.claude_cache)
    requests_count = len(st.session_state.request_history)
    
    st.metric("מטמון פעיל", f"{cache_size}/{MAX_CACHE_ENTRIES}")
    st.metric("בקשות בדקה האחרונה", f"{requests_count}/{MAX_REQUESTS_PER_MINUTE}")
    
    if st.button("🗑️ נקה מטמון", width="stretch"):
        st.session_state.claude_cache = {}
        st.success("מטמון נוקה!")
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 סטטיסטיקות מהירות")
    
    # Professional metric cards
    total_clients = len(df)
    avg_age = df['age'].mean() if len(df) > 0 else 0
    most_common_issue = df['legal_issue'].mode()[0] if len(df) > 0 else "לא זמין"
    
    st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #667eea;">👥 {total_clients}</h3>
            <p style="margin: 0; color: #64748b;">סה"כ לקוחות</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #667eea;">{avg_age:.1f} 📅</h3>
            <p style="margin: 0; color: #64748b;">גיל ממוצע</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #667eea;">⭐ {most_common_issue}</h3>
            <p style="margin: 0; color: #64748b;">תחום נפוץ</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("---")
    st.markdown("### ⚡ פעולות מהירות")
    
    if st.button("🔄 רענן נתונים", width="stretch"):
        st.rerun()
    
    if st.button("📊 ניתוח מהיר", width="stretch"):
        with st.spinner("מכין ניתוח..."):
            basic_analysis = get_basic_analysis()
            st.markdown("### ניתוח מהיר:")
            st.info(basic_analysis)

# Main Content Area with Tabs
tab1, tab2, tab3, tab4 = st.tabs(["👥 ניהול לקוחות", "➕ הוספת לקוח", "🧠 ניתוח AI", "💬 עוזר וירטואלי"])

with tab1:
    st.markdown('<h2 class="section-header">👥 ניהול לקוחות</h2>', unsafe_allow_html=True)
    
    # Enhanced search and filter section
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 חיפוש לפי שם לקוח", placeholder="הזן שם לקוח...")
    
    with col2:
        age_filter = st.selectbox("🎂 סינון לפי גיל", 
                                 ["הכל", "18-30", "31-45", "46-60", "60+"])
    
    with col3:
        issue_filter = st.selectbox("⚖️ סינון לפי תחום", 
                                   ["הכל"] + list(df['legal_issue'].unique()) if len(df) > 0 else ["הכל"])
    
    # Apply filters
    df_filtered = df.copy()
    
    if search_term:
        df_filtered = df_filtered[df_filtered['name'].str.contains(search_term, case=False, na=False)]
    
    if age_filter != "הכל":
        if age_filter == "18-30":
            df_filtered = df_filtered[(df_filtered['age'] >= 18) & (df_filtered['age'] <= 30)]
        elif age_filter == "31-45":
            df_filtered = df_filtered[(df_filtered['age'] >= 31) & (df_filtered['age'] <= 45)]
        elif age_filter == "46-60":
            df_filtered = df_filtered[(df_filtered['age'] >= 46) & (df_filtered['age'] <= 60)]
        elif age_filter == "60+":
            df_filtered = df_filtered[df_filtered['age'] > 60]
    
    if issue_filter != "הכל":
        df_filtered = df_filtered[df_filtered['legal_issue'] == issue_filter]
    
    # Display results
    if len(df_filtered) > 0:
        st.markdown(f"**נמצאו {len(df_filtered)} לקוחות**")
        
        # Enhanced dataframe display
        st.dataframe(
            df_filtered,
            width="stretch",
            height=400,
            column_config={
                "id": st.column_config.NumberColumn("מזהה", width="small"),
                "name": st.column_config.TextColumn("שם הלקוח", width="medium"),
                "age": st.column_config.NumberColumn("גיל", width="small"),
                "legal_issue": st.column_config.TextColumn("תחום משפטי", width="medium")
            }
        )
        
        # Export functionality
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 הורד כ-CSV",
            data=csv,
            file_name=f"clients_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("🔍 לא נמצאו לקוחות התואמים את הקריטריונים שנבחרו")

with tab2:
    st.markdown('<h2 class="section-header">➕ הוספת לקוח חדש</h2>', unsafe_allow_html=True)
    
    # Professional form layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("add_client_form", clear_on_submit=True):
            st.markdown("### פרטי הלקוח")
            
            name = st.text_input("שם מלא *", placeholder="הזן שם מלא של הלקוח")
            age = st.number_input("גיל *", min_value=18, max_value=120, value=35, 
                                help="גיל הלקוח (18-120)")
            
            # Hebrew legal issue options with descriptions
            legal_issues_hebrew = {
                "משפחה": "Family",
                "נדל\"ן": "Real Estate", 
                "חוזים": "Contracts",
                "פלילי": "Criminal",
                "צוואות וירושות": "Wills and Inheritance"
            }
            
            issue_descriptions = {
                "משפחה": "גירושין, מזונות, אימוץ",
                "נדל\"ן": "קנייה, מכירה, השכרה",
                "חוזים": "הסכמים מסחריים ואזרחיים",
                "פלילי": "הגנה פלילית",
                "צוואות וירושות": "תכנון עיזבון וירושה"
            }
            
            issue_hebrew = st.selectbox(
                "תחום משפטי *", 
                list(legal_issues_hebrew.keys()),
                help="בחר את התחום המשפטי הרלוונטי"
            )
            
            st.info(f"📝 {issue_descriptions[issue_hebrew]}")
            
            # Form submission
            col_submit, col_clear = st.columns(2)
            
            with col_submit:
                submitted = st.form_submit_button("💾 שמור לקוח", type="primary", width="stretch")
            
            with col_clear:
                if st.form_submit_button("🗑️ נקה טופס", width="stretch"):
                    st.rerun()
            
            # Handle form submission
            if submitted:
                if name and name.strip():
                    issue_english = legal_issues_hebrew[issue_hebrew]
                    add_client(name.strip(), age, issue_english)
                    st.success(f"✅ {name} נוסף בהצלחה למערכת!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("⚠️ נא להזין שם לקוח")
    
    with col2:
        st.markdown("### 📋 הנחיות")
        st.info("""
        **שדות חובה מסומנים ב-***
        
        **טיפים להוספת לקוח:**
        - וודא שהשם מלא ומדויק
        - בדוק שהגיל נכון
        - בחר את התחום המשפטי המתאים ביותר
        
        **לאחר השמירה:**
        - הלקוח יופיע ברשימת הלקוחות
        - ניתן לחפש אותו בכרטיסיית "ניהול לקוחות"
        """)
        
        # Recent additions
        if len(df) > 0:
            st.markdown("### 🕒 לקוחות שנוספו לאחרונה")
            recent_clients = df.tail(3)[['name', 'legal_issue']]
            for _, client_row in recent_clients.iterrows():
                st.markdown(f"• **{client_row['name']}** - {client_row['legal_issue']}")

with tab3:
    st.markdown('<h2 class="section-header">🧠 ניתוח מתקדם עם Claude AI</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 מה כולל הניתוח המתקדם?
        
        **📊 ניתוח סטטיסטי מעמיק:**
        - התפלגות גילאים מפורטת
        - ניתוח תחומים משפטיים
        - זיהוי מגמות ודפוסים
        
        **💡 תובנות עסקיות:**
        - המלצות אסטרטגיות
        - זיהוי הזדמנויות
        - ניתוח פערים בשירות
        
        **🔍 קורלציות מתקדמות:**
        - קשרים בין גיל לתחום משפטי
        - ניתוח התפלגות לקוחות
        - חיזוי מגמות עתידיות
        """)
        
        if st.button("🚀 הפעל ניתוח מתקדם", type="primary", width="stretch"):
            with st.spinner("🤖 Claude מנתח את הנתונים... זה עשוי לקחת מספר שניות"):
                analysis = analyze_data(df)
                
                st.markdown("---")
                st.markdown("### 📋 תוצאות הניתוח:")
                
                # Display analysis in an expandable container
                with st.expander("📊 ניתוח מלא", expanded=True):
                    st.markdown(analysis)
                
                # Download option
                st.download_button(
                    label="📥 הורד ניתוח כקובץ טקסט",
                    data=analysis,
                    file_name=f"legal_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    width="stretch"
                )
    
    with col2:
        st.markdown("### 📈 תצוגה מקדימה")
        
        if len(df) > 0:
            # Quick visualizations
            st.markdown("**התפלגות תחומים משפטיים:**")
            issue_counts = df['legal_issue'].value_counts()
            st.bar_chart(issue_counts)
            
            st.markdown("**התפלגות גילאים:**")
            # Create histogram using age bins
            
            # Create age bins for histogram
            age_bins = np.arange(df['age'].min(), df['age'].max() + 5, 5)
            age_counts, _ = np.histogram(df['age'], bins=age_bins)
            
            # Create a DataFrame for the histogram
            hist_df = pd.DataFrame({
                'Age Range': [f"{int(age_bins[i])}-{int(age_bins[i+1])}" for i in range(len(age_bins)-1)],
                'Count': age_counts
            })
            
            st.bar_chart(hist_df.set_index('Age Range'))
            
            # Key metrics
            st.markdown("### 🔢 מדדים מרכזיים")
            st.metric("לקוח הצעיר ביותר", f"{df['age'].min()} שנים")
            st.metric("לקוח המבוגר ביותר", f"{df['age'].max()} שנים")
            st.metric("סטיית תקן גילאים", f"{df['age'].std():.1f}")

with tab4:
    st.markdown('<h2 class="section-header">💬 עוזר וירטואלי חכם</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🤖 שאל את העוזר הוירטואלי")
        st.markdown("העוזר הוירטואלי יכול לענות על שאלות מורכבות על בסיס נתוני הלקוחות שלך")
        
        # Quick question buttons
        st.markdown("**🎯 שאלות מהירות:**")
        quick_questions = [
            "מי הלקוח הצעיר ביותר?",
            "כמה לקוחות יש בתחום המשפחה?",
            "מה הגיל הממוצע של לקוחות נדל\"ן?",
            "האם יש קשר בין גיל לסוג התיק?"
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(quick_questions):
            with cols[i % 2]:
                if st.button(question, key=f"quick_{i}", width="stretch"):
                    with st.spinner("🤔 חושב על התשובה..."):
                        response = chatbot_response(question, df)
                        st.markdown("### 💡 תשובה:")
                        st.info(response)
        
        st.markdown("---")
        
        # Custom question input
        user_question = st.text_area(
            "או שאל שאלה מותאמת אישית:",
            placeholder="לדוגמה: 'מה האחוז של לקוחות מעל גיל 50 בתחום הצוואות?'",
            height=100
        )
        
        if st.button("📨 שלח שאלה", type="primary", width="stretch"):
            if user_question.strip():
                with st.spinner("🤖 העוזר הוירטואלי חושב..."):
                    response = chatbot_response(user_question, df)
                    st.markdown("### 💡 תשובה:")
                    st.success(response)
            else:
                st.warning("⚠️ אנא הזן שאלה")
    
    with col2:
        st.markdown("### 💡 טיפים לשימוש")
        st.info("""
        **שאלות שהעוזר יכול לענות עליהן:**
        
        📊 **סטטיסטיקות:**
        - "כמה לקוחות יש לי?"
        - "מה הגיל הממוצע?"
        
        🔍 **חיפושים:**
        - "מי הלקוחות בתחום הפלילי?"
        - "רשימת לקוחות מעל גיל 45"
        
        📈 **ניתוחים:**
        - "איזה תחום הכי פופולרי?"
        - "האם יש קשר בין גיל לתחום?"
        
        💼 **תובנות עסקיות:**
        - "איזה תחומים כדאי לחזק?"
        - "איזה קבוצות גיל חסרות?"
        """)
        
        # Chat history (simple implementation)
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if len(st.session_state.chat_history) > 0:
            st.markdown("### 📝 היסטוריית שאלות")
            for i, (q, a) in enumerate(st.session_state.chat_history[-3:]):  # Show last 3
                with st.expander(f"שאלה {i+1}: {q[:50]}..."):
                    st.write(f"**שאלה:** {q}")
                    st.write(f"**תשובה:** {a[:200]}...")

# Professional Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 12px; margin-top: 2rem;'>
        <h4 style='color: #1e293b; margin-bottom: 0.5rem;'>⚖️ LegalSmart Pro</h4>
        <p style='color: #64748b; margin: 0;'>
            פותח כחלק מקורס פיתוח AI | גרסה 2.0 | מופעל על ידי Claude 3.5 Sonnet
        </p>
        <p style='color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;'>
            © 2024 - מערכת ניהול לקוחות משפטית מתקדמת
        </p>
    </div>
""", unsafe_allow_html=True)