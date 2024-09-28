import streamlit as st
import openai
import time

# Streamlit 페이지 설정
st.set_page_config(page_title="AI Chatbot", page_icon=":robot_face:")

# OpenAI API 키 설정
openai.api_key = st.secrets["openai_api_key"]

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"

# 함수: OpenAI API를 사용하여 응답 생성
def generate_response(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]
    
    # 이전 대화 내역 10개 추가
    for message in st.session_state.messages[-10:]:
        messages.append({"role": "user" if message["is_user"] else "assistant", "content": message["content"]})
    
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model=st.session_state.openai_model,
        messages=messages,
        stream=True
    )

    return response

# 스트림릿 UI
st.title("AI Chatbot")

# 사용자 입력
user_input = st.text_input("메시지를 입력하세요:", key="user_input")

# Enter 키 처리
if user_input and user_input != st.session_state.get("previous_input", ""):
    st.session_state.messages.append({"content": user_input, "is_user": True})
    st.session_state.previous_input = user_input

    with st.spinner("AI가 응답하는 중..."):
        response = generate_response(user_input)
        ai_response = ""
        message_placeholder = st.empty()
        
        for chunk in response:
            if chunk.choices[0].delta.get("content"):
                ai_response += chunk.choices[0].delta.content
                message_placeholder.markdown(ai_response + "▌")
                time.sleep(0.01)
        
        message_placeholder.markdown(ai_response)
        st.session_state.messages.append({"content": ai_response, "is_user": False})

# 대화 내역 표시
for i, msg in enumerate(reversed(st.session_state.messages)):
    st.text_area(f"{'You' if msg['is_user'] else 'AI'}", value=msg["content"], height=100, key=f"message_{i}", disabled=True)

# 대화 내역 초기화 버튼
if st.button("대화 내역 초기화"):
    st.session_state.messages = []
    st.experimental_rerun()
