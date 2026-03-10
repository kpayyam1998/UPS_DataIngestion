import streamlit as st
import requests
import time
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

st.set_page_config(page_title="UPS RAG System", page_icon="📦", layout="wide")

# --- API Endpoints ---
INGEST_URL = "http://localhost:8000/api/v1/vector/vector/ingest"
CHAT_URL = "http://localhost:8000/api/v1/vector/vector/generate_response"

# --- Sidebar: Data Ingestion ---
with st.sidebar:
    st.header("📥 Data Ingestion")
    st.write("Upload PDFs to sync with Qdrant index.")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if st.button("Start Ingestion"):
        if uploaded_file is not None:
            with st.spinner("Processing and indexing PDF..."):
                try:
                    # Prepare the file for the POST request
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    
                    response = requests.post(INGEST_URL, files=files)
                    
                    if response.status_code == 200:
                        st.success(f"✅ Success! '{uploaded_file.name}' is ingested.")
                        logger.info(f"Successfully ingested {uploaded_file.name}")
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"📡 Connection Failed: {e}")
        else:
            st.warning("Please upload a file first.")

    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Main UI: Chat Interface ---
st.title("🤖 UPS RAG Chatbot")
st.caption("Ask questions about your ingested documents.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Query Input
if prompt := st.chat_input("Ask a question..."):
    # Display User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Assistant Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 Searching documents...")

        try:
            # Send query to backend
            response = requests.post(CHAT_URL, json={"query": prompt})
            
            if response.status_code == 200:
                data = response.json()
                assistant_response = data.get("response", "I couldn't find an answer in the documents.")
            else:
                assistant_response = f"⚠️ Backend Error: {response.status_code}"
                
        except Exception as e:
            assistant_response = f"🚫 Connection Error: {str(e)}"

        # Typing effect
        full_response = ""
        for chunk in assistant_response.split(" "):
            full_response += chunk + " "
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})