import os
import requests
import streamlit as st
from datetime import datetime
import uuid


# --- Global Styles ---
st.markdown(
    """
    <style>
    /* 🌈 App-wide background */
    body {
        background: linear-gradient(135deg, #fff7ed 0%, #ffe4cc 100%);
    }

    /* 🟧 Gradient header styling */
    .bill-header {
        background: linear-gradient(to right, #f97316, #ea580c);
        padding: 16px;
        border-radius: 12px;
        color: white;
        margin-bottom: 10px;
    }

    .bill-header h1 {
        margin: 0;
        font-size: 32px;
        color: white !important; /* ensures text is visible */
        background: none !important; /* removes global h1 gradient */
        -webkit-text-fill-color: white !important;
    }

    .bill-header small {
        font-size: 15px;
        color: #fff8f2;
    }

    /* 🟠 Gradient text only for chat section titles */
    .chat-section h1, .chat-section h2, .chat-section h3 {
        background: linear-gradient(to right, #f97316, #ea580c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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
    <div class="bill-header">
        <h1>Bill Assistant AI</h1>
        <small>AI-powered bill analysis & expense tracking</small>
    </div>
    """,
    unsafe_allow_html=True,
)

# Custom styles for chat UI (gradient orange + dark background)
st.markdown(
    """
    <style>
    /* --- App background --- */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #1e1e1e 0%, #0b0b0b 100%) !important;
        color: #f3f4f6 !important;
    }

    /* --- Header gradient --- */
    div[data-testid="stMarkdownContainer"] h1 {
        background: linear-gradient(to right, #f97316, #ea580c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* --- Chat container --- */
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 16px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(8px);
    }

    /* --- Message bubbles --- */
    .msg-row { display: flex; margin: 10px 0; }
    .msg-bubble { padding: 12px 16px; border-radius: 16px; max-width: 75%; line-height: 1.5; }

    /* User message (right side) */
    .msg-user {
        background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
        color: #f3f4f6;
        margin-left: auto;
        border-bottom-right-radius: 2px;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.08);
    }

    /* Assistant message (left side) */
    .msg-assistant {
        background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%);
        color: #78350f;
        margin-right: auto;
        border-bottom-left-radius: 2px;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.2);
    }

    /* --- Avatars --- */
    .avatar {
        width: 38px; height: 38px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold; font-size: 16px;
        box-shadow: 0 0 8px rgba(0,0,0,0.4);
    }
    .avatar-user { background: #6b7280; color: white; }
    .avatar-assistant {
        background: linear-gradient(135deg, #f97316, #ea580c);
        color: white;
        box-shadow: 0 0 10px rgba(249, 115, 22, 0.5);
    }

    /* --- Timestamps & attachments --- */
    .timestamp { font-size: 11px; color: #9ca3af; margin-top: 4px; }
    .attachment { font-size: 13px; color: #065f46; }

    /* --- Buttons --- */
    button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(249, 115, 22, 0.3) !important;
        border-radius: 10px !important;
    }

    button:hover {
        background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(249, 115, 22, 0.5) !important;
    }

    button:active { transform: translateY(0) !important; }

    /* --- Sidebar --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%) !important;
        color: white !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f97316 !important;
    }
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
        # Clear the file uploader selection so the uploaded PDFs are 'unseated' and user can add new files
        try:
            st.session_state["ingest_pdfs"] = None
        except Exception:
            # best-effort; don't block on clearing the uploader
            pass



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
