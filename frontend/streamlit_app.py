import os
import requests
import streamlit as st
from datetime import datetime
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

# no chat attachments; ingestion is PDF-only


# --- Sidebar / Header ---
st.markdown(
    """
    <div style="background: linear-gradient(to right, #f97316, #ea580c); padding: 12px; border-radius: 8px; color: white;">
        <h1 style="margin:0; font-size:28px;">Bill Assistant</h1>
        <small>AI-powered bill analysis & expense tracking</small>
    </div>
    """,
    unsafe_allow_html=True,
)

# Custom styles for chat UI
st.markdown(
    """
    <style>
    .chat-container { max-height: 60vh; overflow-y: auto; padding: 8px; }
    .msg-row { display: flex; margin: 8px 0; }
    .msg-bubble { padding: 12px; border-radius: 12px; max-width: 75%; }
    .msg-user { background: #e5e7eb; color: #111827; margin-left: auto; border-bottom-right-radius: 2px; }
    .msg-assistant { background: #fff7ed; color: #92400e; margin-right: auto; border-bottom-left-radius: 2px; }
    .avatar { width:36px; height:36px; border-radius:50%; display:inline-block; text-align:center; line-height:36px; font-weight:bold; }
    .avatar-user { background:#6b7280; color:white; }
    .avatar-assistant { background:#f97316; color:white; }
    .timestamp { font-size:11px; color:#6b7280; margin-top:4px; }
    .attachment { font-size:13px; color:#065f46; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Backend base URL
API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000")


# Note: chat attachments removed — ingestion is PDF-only via the section below

# --- Dedicated PDF ingestion for bills ---
st.markdown("---")
st.markdown("### Ingest bills (PDF only)")
pdfs_to_ingest = st.file_uploader("Upload PDF bill files to ingest", type=["pdf"], accept_multiple_files=True, key="ingest_pdfs")
if pdfs_to_ingest:
    st.info(f"{len(pdfs_to_ingest)} file(s) ready to ingest. Click 'Ingest PDFs' to upload to the backend.")
ingest_button = st.button("Ingest PDFs")

if ingest_button:
    if not pdfs_to_ingest:
        st.warning("Please select one or more PDF files to ingest.")
    else:
        total_inserted = 0
        details = []
        for file in pdfs_to_ingest:
            try:
                with st.spinner(f"Uploading {file.name}..."):
                    files = {"file": (file.name, file.getvalue(), file.type)}
                    r = requests.post(f"{API_BASE}/api/ingest_pdf", files=files, timeout=120)
                if r.ok:
                    data = r.json()
                    inserted = data.get("inserted_count", 0)
                    total_inserted += int(inserted or 0)
                    details.append(f"{file.name}: {inserted} chunks")
                else:
                    details.append(f"{file.name}: failed ({r.status_code})")
            except Exception as e:
                details.append(f"{file.name}: error ({e})")

        assistant_text = f"Ingestion complete. Total chunks inserted: {total_inserted}.\n" + "; ".join(details)
        assistant_msg = {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": assistant_text,
            "attachments": [],
            "timestamp": datetime.now(),
        }
        st.session_state.messages.append(assistant_msg)



# Controls (clear chat)
st.sidebar.markdown("## Controls")
if st.sidebar.button("Clear chat"):
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


# --- Input form ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Type your message here:", height=80)
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    # Add user message
    user_msg = {
        "id": str(uuid.uuid4()),
        "role": "user",
        "content": user_input,
        "attachments": [],
        "timestamp": datetime.now(),
    }
    st.session_state.messages.append(user_msg)

    # Query the backend for an answer
    try:
        with st.spinner("Querying backend..."):
            r = requests.post(f"{API_BASE}/api/query", json={"question": user_input, "top_k": 4}, timeout=60)
        if r.ok:
            data = r.json()
            assistant_text = data.get("answer") or "(no answer returned)"
            assistant_sources = data.get("sources") or []
        else:
            assistant_text = f"Query failed: {r.status_code} - {r.text}"
            assistant_sources = []
    except Exception as e:
        assistant_text = f"Request failed: {e}"
        assistant_sources = []

    assistant_msg = {
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "content": assistant_text,
        "attachments": assistant_sources,
        "timestamp": datetime.now(),
    }
    st.session_state.messages.append(assistant_msg)

# Render messages (after input handling so newly appended messages appear immediately)
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        is_user = msg.get("role") == "user"
        avatar_class = "avatar-user" if is_user else "avatar-assistant"
        bubble_class = "msg-user" if is_user else "msg-assistant"

        if is_user:
            cols = st.columns([1, 9])
            with cols[1]:
                st.markdown(
                    f"<div class='msg-row'><div class='msg-bubble {bubble_class}'>" + msg.get("content", "") + "</div></div>",
                    unsafe_allow_html=True,
                )
                ts = msg.get("timestamp")
                if ts:
                    st.markdown(f"<div class='timestamp' style='text-align:right'>{ts}</div>", unsafe_allow_html=True)
        else:
            cols = st.columns([1, 9])
            with cols[0]:
                st.markdown(f"<div class='avatar {avatar_class}'>A</div>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(
                    f"<div class='msg-row'><div class='msg-bubble {bubble_class}'>" + msg.get("content", "") + "</div></div>",
                    unsafe_allow_html=True,
                )
                ts = msg.get("timestamp")
                if ts:
                    st.markdown(f"<div class='timestamp'>{ts}</div>", unsafe_allow_html=True)

                # If assistant provided sources, render download buttons
                sources = msg.get("attachments") or []
                if sources:
                    for i, s in enumerate(sources):
                        src_text = s.get("text") or s.get("content") or str(s)
                        src_name = s.get("metadata", {}).get("source", f"source_{i}.txt")
                        try:
                            st.download_button(f"Download source {i+1}", data=src_text, file_name=f"{src_name}.txt")
                        except Exception:
                            st.markdown(f"<div class='attachment'>📎 {src_name}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

