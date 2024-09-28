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

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a text input field for the user's message
prompt = st.text_input("Your message:", key="user_input")

# Send button
if st.button("Send"):
    if prompt:
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # 이 부분을 "gpt-4"로 변경했습니다.
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )

            # Display and store the assistant's response
            assistant_response = response.choices[0].message['content']
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
