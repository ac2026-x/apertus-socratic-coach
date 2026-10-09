import os
import streamlit as st
from dotenv import load_dotenv
from coach import ScientificCoach

# Explicitly load .env from the track_2b directory
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(dotenv_path=env_path)

st.set_page_config(page_title="Scaffold AI Coach", page_icon="🔬", layout="wide")

st.title("🔬 Scaffold AI: Socratic Science Coach")
st.caption("Apertus-powered scientific reasoning mentor with adaptive scaffolding.")

api_key = os.getenv("HF_API_KEY")
if not api_key:
    st.error("HF_API_KEY missing from .env file!")
    st.stop()

if "coach" not in st.session_state:
    st.session_state.coach = ScientificCoach(api_key)
    st.session_state.history = []
    st.session_state.session_ended = False

coach = st.session_state.coach
stage_info = coach.get_stage_info()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Reasoning Progress")
st.sidebar.progress(stage_info["index"] / stage_info["total"])
st.sidebar.subheader(f"Stage {stage_info['index']}/9: {stage_info['name']}")
st.sidebar.info(stage_info["objective"])

st.sidebar.markdown("---")

# Adaptive Circuit Breaker Warning
if stage_info["stuck_count"] >= 2:
    st.sidebar.warning("💡 You seem stuck on this step. Feel free to use 'Next Stage' or click 'I'm Stuck' for another angle!")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Next Stage ▶️"):
        coach.advance()
        st.rerun()

with col2:
    if st.button("Reset 🔄"):
        coach.reset()
        st.session_state.history = []
        st.session_state.session_ended = False
        st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("Finish & Exit Session 🏁"):
    st.session_state.session_ended = True
    st.rerun()

# --- MAIN CHAT AREA ---
if not st.session_state.session_ended:
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Action Buttons under chat
    col_input, col_stuck = st.columns([4, 1])
    
    with col_stuck:
        stuck_clicked = st.button("🙋 I'm Stuck!")

    user_input = st.chat_input("Share your observation or answer...")

    if user_input or stuck_clicked:
        prompt_text = user_input if user_input else "I am having trouble with this question."
        st.chat_message("user").write(prompt_text)
        
        with st.spinner("Your mentor is formulating a hint..."):
            reply = coach.respond(prompt_text, st.session_state.history, is_stuck_signal=stuck_clicked)
            
        st.chat_message("assistant").write(reply)
        st.session_state.history.append({"role": "user", "content": prompt_text})
        st.session_state.history.append({"role": "assistant", "content": reply})
        st.rerun()

# --- END OF SESSION FEEDBACK FORM ---
else:
    st.success("🎉 Great job exercising your scientific reasoning skills today!")
    st.subheader("Session Feedback & Reflection")
    
    # Track whether feedback has been saved
    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False

    if not st.session_state.feedback_submitted:
        with st.form("feedback_form"):
            rating = st.slider("How helpful was the coach's guidance?", 1, 5, 4)
            feedback = st.text_area("What felt frustrating or particularly helpful during this session?")
            submitted = st.form_submit_button("Submit Feedback & Save Telemetry")
            
            if submitted:
                coach.save_session_analytics(rating, feedback)
                st.session_state.feedback_submitted = True
                st.rerun()

    else:
        st.success("Thank you! Session analytics saved to `data/session_logs.json`.")
        
        # Standalone button OUTSIDE the form block
        if st.button("Start New Session 🔄"):
            coach.reset()
            st.session_state.history = []
            st.session_state.session_ended = False
            st.session_state.feedback_submitted = False
            st.rerun()