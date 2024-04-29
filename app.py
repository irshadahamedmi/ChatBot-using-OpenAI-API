# Import necessary libraries
import streamlit as st  # Streamlit library for creating web apps
from openai import OpenAI  # OpenAI library for accessing GPT-3 API
from dotenv import find_dotenv, load_dotenv  # Import dotenv for loading environment variables
import os

load_dotenv(find_dotenv())  # Load environment variables from .env file if present
OpenAI.api_key = os.getenv("OPENAI_API_KEY")  # Set OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set the title of the Streamlit app
st.title("💬 Chatbot")

# Initialize messages in the session state if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display previous chat messages in the app
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Check if user inputs a message in the chat input field
if prompt := st.chat_input():
    # Check if OpenAI API key is provided
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()  # Stop execution if API key is missing

    # Initialize OpenAI client with the provided API key
    client = OpenAI(api_key=openai_api_key)
    # Add user's message to the session state messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)  # Display user's message in the chat
    # Generate a response from OpenAI API using GPT-3.5-turbo model
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content  # Get the content of the response
    # Add assistant's message to the session state messages
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)  # Display assistant's message in the chat