import os
import streamlit as st
from dotenv import load_dotenv
from coach import ScientificCoach

load_dotenv()

st.set_page_config(page_title="Socratic Science Coach", page_icon="🔬", layout="wide")

# App Header
st.title("🔬 Apertus Socratic Science Coach")
st.caption("Scaffolding scientific thinking without giving away answers.")

# Get API key from .env
api_key = os.getenv("HF_API_KEY")

if not api_key:
    st.error("HF_API_KEY missing! Please check your .env file.")
    st.stop()

# Initialize Coach and session state memory
if "coach" not in st.session_state:
    st.session_state.coach = ScientificCoach(api_key)
    st.session_state.history = []

coach = st.session_state.coach
stage_info = coach.get_stage_info()

# --- SIDEBAR: Stage Machine Controls ---
st.sidebar.header("Reasoning Stage Progress")
st.sidebar.progress(stage_info["index"] / stage_info["total"])
st.sidebar.subheader(f"Stage {stage_info['index']} of 9")
st.sidebar.markdown(f"**{stage_info['name']}**")
st.sidebar.info(f"**Objective:** {stage_info['objective']}")

st.sidebar.markdown("---")

col_prev, col_next = st.sidebar.columns(2)
with col_next:
    if st.button("Next Stage ▶️"):
        if coach.advance():
            st.rerun()
        else:
            st.sidebar.success("Already at Final Stage!")

with col_prev:
    if st.button("Reset Session 🔄"):
        coach.reset()
        st.session_state.history = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Chat Input
if user_input := st.chat_input("State your problem, observation, or answer..."):
    # Display user input
    st.chat_message("user").write(user_input)
    
    # Get coach response
    with st.spinner("Apertus is formulating a coaching response..."):
        bot_response = coach.respond(user_input, st.session_state.history)
        
    # Display coach output
    st.chat_message("assistant").write(bot_response)
    
    # Update local memory
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": bot_response})