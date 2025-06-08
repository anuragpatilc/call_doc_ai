import streamlit as st
from openai import AzureOpenAI
from config import ENDPOINT, DEPLOYMENT, SUBSCRIPTION_KEY, API_VERSION
from dotenv import load_dotenv

# Set page configuration (must be called before any other Streamlit commands)
st.set_page_config(
    page_title="Streamlit Chatbot",
    layout="centered"
)

# Inject a viewport meta tag for mobile responsiveness
st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """,
    unsafe_allow_html=True
)

# Load environment variables from the .env file
load_dotenv()

client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT,
    api_key=SUBSCRIPTION_KEY,
)

# Initialize page state if not already set
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation buttons at the top of the app
col1, col2 = st.columns(2)
with col1:
    if st.button("Home"):
        st.session_state.page = "home"
with col2:
    if st.button("About Me"):
        st.session_state.page = "about"

# Show content based on the current page
if st.session_state.page == "home":
    st.title("Streamlit Chatbot")

    # Initialize conversation history in session state if not already set
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{
            "role": "system",
            "content": "You are a helpful assistant."
        }]

    # Allow resetting the conversation
    if st.button("Reset Chat"):
        st.session_state.chat_history = [{
            "role": "system",
            "content": "You are a helpful assistant."
        }]
        st.experimental_rerun()

    # Create a chat input form for a single message
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your message:")
        submitted = st.form_submit_button("Send")
        if submitted and user_input:
            # Append the user message and call the API
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            response = client.chat.completions.create(
                messages=st.session_state.chat_history,
                max_completion_tokens=512,
                model=DEPLOYMENT
            )
            bot_reply = response.choices[0].message.content
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": bot_reply
            })

    # Display the chat history using Streamlit's chat message interface
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        elif msg["role"] == "assistant":
            st.chat_message("assistant").markdown(msg["content"])

elif st.session_state.page == "about":
    st.title("About Me")
    st.write("Name: Anurag Patil C")
    st.write("Work: EY GDS")
