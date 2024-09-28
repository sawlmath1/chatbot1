import streamlit as st
import openai

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-4 model to generate responses. "
    "This app uses an OpenAI API key stored in Streamlit secrets. "
)

# Get the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    st.text(f"{message['role'].capitalize()}: {message['content']}")

# User input
user_input = st.text_input("Your message:", key="user_input")

# Send button
if st.button("Send"):
    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.text(f"User: {user_input}")

        # Generate response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )

            # Get and display assistant's response
            assistant_response = response.choices[0].message['content']
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.text(f"Assistant: {assistant_response}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
