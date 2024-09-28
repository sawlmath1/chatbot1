import streamlit as st
import openai
import time

# OpenAI API 키 설정
openai.api_key = st.secrets["openai_api_key"]

# 스트림릿 앱 설정
st.set_page_config(page_title="고급 챗봇", layout="wide")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 챗봇 응답 생성 함수 (스트리밍)
def generate_response(messages):
    full_response = ""
    message_placeholder = st.empty()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        stream=True,
    )
    for chunk in response:
        if "content" in chunk.choices[0].delta:
            full_response += chunk.choices[0].delta.content
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.01)
    message_placeholder.markdown(full_response)
    return full_response

# CSS를 사용하여 레이아웃 조정
st.markdown("""
<style>
/* 전체 페이지를 Flex 레이아웃으로 설정 */
.block-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding-top: 0;
    padding-bottom: 0;
}

/* 제목 스타일 */
h1 {
    flex: 0 0 auto;
    margin: 0;
    padding: 1rem;
    background-color: #f9f9f9;
    position: sticky;
    top: 0;
    z-index: 10;
    border-bottom: 1px solid #ddd;
}

/* 채팅 컨테이너 */
.chat-container {
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 1rem;
}

/* 입력 컨테이너 */
.input-container {
    flex: 0 0 auto;
    padding: 1rem;
    border-top: 1px solid #ddd;
    background-color: #f9f9f9;
}

.stChatMessage {
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# 상단의 제목
st.markdown('<h1>고급 챗봇</h1>', unsafe_allow_html=True)

# 채팅 메시지 영역
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# 화면 하단에 고정된 입력 필드
st.markdown('<div class="input-container">', unsafe_allow_html=True)
if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # 챗봇 응답 생성 및 표시
    with st.chat_message("assistant"):
        messages_for_api = [{"role": "system", "content": "You are a helpful assistant."}] + st.session_state.messages
        response = generate_response(messages_for_api)
        st.session_state.messages.append({"role": "assistant", "content": response})
st.markdown('</div>', unsafe_allow_html=True)
