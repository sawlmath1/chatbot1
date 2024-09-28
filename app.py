import streamlit as st
from openai import OpenAI
import time

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai_api_key"])

# 스트림릿 앱 설정
st.set_page_config(page_title="고급 챗봇", layout="wide")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

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

# CSS를 사용하여 레이아웃 조정
st.markdown("""
<style>
/* 전체 페이지를 Flex 레이아웃으로 설정 */
.main {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 0;
    margin: 0;
}
/* 제목 스타일 */
.title {
    flex: 0 0 auto;
    padding: 1rem;
    background-color: #f9f9f9;
    border-bottom: 1px solid #ddd;
    text-align: center;
}
/* 채팅 컨테이너 */
.chat-container {
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
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
/* Streamlit 기본 패딩 제거 */
.block-container {
    padding-top: 0;
    padding-bottom: 0;
    padding-left: 0;
    padding-right: 0;
}
.stChatFloatingInputContainer {
    padding-bottom: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# 메인 레이아웃
main = st.container()
with main:
    # 상단의 제목
    st.markdown('<div class="title"><h1>고급 챗봇</h1></div>', unsafe_allow_html=True)
    
    # 채팅 메시지 영역
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 화면 하단에 고정된 입력 필드
    input_container = st.container()
    with input_container:
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        if prompt := st.chat_input("메시지를 입력하세요"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
                # 챗봇 응답 생성 및 표시
                with st.chat_message("assistant"):
                    messages_for_api = [{"role": "system", "content": "You are a helpful assistant."}] + st.session_state.messages
                    response = generate_response(messages_for_api)
                    st.session_state.messages.append({"role": "assistant", "content": response})
        st.markdown('</div>', unsafe_allow_html=True)
