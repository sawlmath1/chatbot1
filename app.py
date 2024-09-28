import streamlit as st
from openai import OpenAI

st.title("💬 Chatbot")
st.write("This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses.")

# OpenAI 클라이언트 생성
client = OpenAI(api_key=st.secrets["openai_api_key"])

# 세션 상태 변수를 생성하여 채팅 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력을 받기 위한 채팅 입력 필드 생성
if prompt := st.chat_input("What is up?"):
    # 현재 프롬프트 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI API를 사용하여 응답 생성
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # 응답을 채팅에 스트리밍하고 세션 상태에 저장
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
