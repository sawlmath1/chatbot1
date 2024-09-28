import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai_api_key"])

# 스트림릿 앱 제목 설정
st.title("고급 챗봇")

# 세션 상태에 메시지 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사용자 입력 받기
user_input = st.text_input("메시지를 입력하세요:")

# 챗봇 응답 함수
def get_bot_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

# 사용자가 메시지를 입력했을 때 처리
if user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 최근 10개의 메시지만 유지
    if len(st.session_state.messages) > 20:  # 사용자와 챗봇 메시지를 합해 20개 (10회의 대화)
        st.session_state.messages = st.session_state.messages[-20:]
    
    # 챗봇 응답 얻기
    messages_for_api = [{"role": "system", "content": "You are a helpful assistant."}] + st.session_state.messages
    bot_response = get_bot_response(messages_for_api)
    
    # 챗봇 응답 추가
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# 대화 내용 표시
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text("사용자: " + message["content"])
    else:
        st.text("챗봇: " + message["content"])
