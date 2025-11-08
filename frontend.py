import streamlit as st
from datetime import datetime
import pandas as pd
import uuid

st.set_page_config(page_title="Bill Assistant", layout="wide")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": (
                "Hi! I'm your AI bill assistant. Upload receipts, invoices, or bill documents "
                "and I'll instantly extract key details, calculate totals, and help you track expenses."
            ),
            "attachments": [],
            "timestamp": datetime.now(),
        }
    ]

if "attachments" not in st.session_state:
    st.session_state.attachments = []

# --- Sidebar / Header ---
st.markdown(
    """
    <div style="background: linear-gradient(to right, #f97316, #ea580c); padding: 15px; border-radius: 8px; color: white;">
        <h1 style="margin:0;">Bill Assistant</h1>
        <small>AI-powered bill analysis & expense tracking</small>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- File Uploader ---
uploaded_files = st.file_uploader(
    "Upload receipts or invoices", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True
)
if uploaded_files:
    for file in uploaded_files:
        st.session_state.attachments.append(
            {
                "id": str(uuid.uuid4()),
                "name": file.name,
                "type": file.type,
                "file": file,
            }
        )

# --- Display messages ---
for msg in st.session_state.messages:
    role_color = "#f97316" if msg["role"] == "assistant" else "#6b7280"
    st.markdown(
        f"""
        <div style="margin: 10px 0; padding: 10px; background-color:{'#ffedd5' if msg['role']=='assistant' else '#e5e7eb'}; 
                    border-radius: 8px;">
            <b style="color:{role_color}">{msg['role'].capitalize()}:</b> {msg['content']}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if msg.get("attachments"):
        for att in msg["attachments"]:
            st.markdown(f"- 📎 {att['name']}")

# --- Input form ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here:")
    submit_button = st.form_submit_button("Send")

if submit_button and (user_input.strip() or st.session_state.attachments):
    # Add user message
    user_msg = {
        "id": str(uuid.uuid4()),
        "role": "user",
        "content": user_input,
        "attachments": st.session_state.attachments.copy() if st.session_state.attachments else [],
        "timestamp": datetime.now(),
    }
    st.session_state.messages.append(user_msg)
    st.session_state.attachments = []  # clear after sending

    # Generate assistant response
    if user_msg["attachments"]:
        assistant_text = (
            f"Got it! I've processed {len(user_msg['attachments'])} document(s). "
            "Analyzing bill details including vendor, amount, and dates. "
            "Here's what I found: Amount due: $156.99 | Vendor: Acme Corp | Due date: March 15, 2025"
        )
    else:
        assistant_text = (
            "I'm here to help! You can ask me about bill details, request expense summaries, or upload new documents."
        )

    assistant_msg = {
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "content": assistant_text,
        "attachments": [],
        "timestamp": datetime.now(),
    }
    st.session_state.messages.append(assistant_msg)

    # Rerun to show new messages
    st.experimental_rerun()
