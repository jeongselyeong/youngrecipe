import streamlit as st

# 페이지 설정 (반드시 가장 첫 번째 Streamlit 명령어여야 함)
st.set_page_config(page_title="Gemini Chatbot")

import google.generativeai as genai

# 테스트용 텍스트
st.write("테스트 메시지입니다. 이 텍스트가 보이시나요?")

# Gemini API 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
GEMINI_API_KEY = "AIzaSyApxQihvq1SYuHNU_4s7oggO8dJ8HD5zB4"

# 모델 초기화
model = genai.GenerativeModel("gemini-1.5-flash")

# 타이틀
st.title("Gemini Chatbot")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Gemini Chatbot에 오신 것을 환영합니다!"}]

# 이전 대화 내역 표시
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# 채팅 입력 UI
user_input = st.chat_input("메시지를 입력하세요...")

# 사용자 입력이 있을 경우
if user_input:
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.write(user_input)
    
    # Gemini API 호출
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            response = model.generate_content(user_input)
            st.write(response.text)
