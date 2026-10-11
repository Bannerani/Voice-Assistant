import pickle
import os
import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Voice Assistant Dashboard",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive effects and dark mode styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMetric {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        border: 1px solid #374151;
    }
    .command-card {
        background: #1f2937;
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 12px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }
    .command-card:hover {
        transform: translateY(-2px);
    }
    .title-glow {
        text-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "assistant_state.pkl"

def load_data():
    """Load assistant state from pickle file or initialize default values."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "rb") as f:
                return pickle.load(f)
        except Exception:
            pass
    # Default fallback state matching your pickle schema
    return {
        "user_name": None,
        "history": [
            {
                "time": "2026-10-11 07:41:16",
                "command": "open YouTube",
                "response": "Opening YouTube"
            }
        ],
        "total_commands": 1
    }

def save_data(data):
    """Save assistant state back to pickle file."""
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

# Initialize state
state = load_data()

# App Header
st.markdown("<h1 class='title-glow' style='text-align: center;'>🎙️ Voice Assistant Control Panel</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Interactive Dashboard for your Pickled Assistant Session State</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Controls
st.sidebar.header("⚙️ Assistant Configuration")
user_name_input = st.sidebar.text_input("User Name", value=state.get("user_name") or "")
if user_name_input != (state.get("user_name") or ""):
    state["user_name"] = user_name_input if user_name_input else None
    save_data(state)
    st.sidebar.success("User name updated!")

if st.sidebar.button("🔄 Reset State to Default"):
    state = {
        "user_name": None,
        "history": [{"time": "2026-10-11 07:41:16", "command": "open YouTube", "response": "Opening YouTube"}],
        "total_commands": 1
    }
    save_data(state)
    st.rerun()

# Main Dashboard Metrics Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Commands Executed", value=state.get("total_commands", 0))
with col2:
    st.metric(label="Active User", value=state.get("user_name") if state.get("user_name") else "Guest (None)")
with col3:
    st.metric(label="Logged Interactions", value=len(state.get("history", [])))

st.markdown("### 💬 Simulate Voice Command")
with st.form("command_form", clear_on_submit=True):
    new_command = st.text_input("Enter a command (e.g., 'play music', 'check weather'):")
    submitted = st.form_submit_button("Run Command")
    if submitted and new_command:
        response_text = f"Executed action for: {new_command}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Append to history & increment counter
        state["history"].append({
            "time": timestamp,
            "command": new_command,
            "response": response_text
        })
        state["total_commands"] += 1
        save_data(state)
        st.success(f"Response: {response_text}")
        st.rerun()

st.markdown("---")
st.markdown("### 📜 Command History Log")

if not state.get("history"):
    st.info("No history logs found.")
else:
    for item in reversed(state["history"]):
        st.markdown(f"""
            <div class="command-card">
                <small style="color: #9ca3af;">🕒 {item.get('time')}</small><br>
                <b>Command:</b> {item.get('command')}<br>
                <b>Response:</b> <span style="color: #60a5fa;">{item.get('response')}</span>
            </div>
        """, unsafe_allow_html=True)
