import streamlit as st
from openai import OpenAI
import time

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai_api_key"])

# 스트림릿 앱 설정
st.set_page_config(page_title="고급 챗봇", layout="wide")
st.title("고급 챗봇")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 메시지 표시 함수
def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 챗봇 응답 생성 함수 (스트리밍)
def generate_response(messages):
    full_response = ""
    message_placeholder = st.empty()
    for chunk in client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    ):
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.01)
    message_placeholder.markdown(full_response)
    return full_response

# 메인 UI
chat_container = st.container()

with chat_container:
    # 기존 메시지 표시
    display_chat_messages()

    # 새 사용자 입력 처리
    if prompt := st.chat_input("메시지를 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 챗봇 응답 생성 및 표시
        with st.chat_message("assistant"):
            messages_for_api = [{"role": "system", "content": "You are a helpful assistant."}] + st.session_state.messages
            response = generate_response(messages_for_api)
            st.session_state.messages.append({"role": "assistant", "content": response})

# CSS를 사용하여 입력창을 화면 하단에 고정
st.markdown("""
<style>
.stTextInput {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem;
    background-color: white;
    z-index: 1000;
}
.stChatFloatingInputContainer {
    bottom: 3rem !important;
}
</style>
""", unsafe_allow_html=True)
