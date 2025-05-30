import streamlit as st
import google.generativeai as genai

# 테스트용 텍스트
st.write("테스트 메시지입니다. 이 텍스트가 보이시나요?")

# 페이지 설정
st.set_page_config(
    page_title="Gemini Chatbot"
)

# 타이틀 표시
st.title("Gemini Chatbot")

# Gemini API 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Gemini 모델 설정
model = genai.GenerativeModel('gemini-1.5-flash')

# 시스템 프롬프트 설정
SYSTEM_PROMPT = """당신은 친절하고 도움이 되는 AI 어시스턴트입니다.
사용자의 질문에 정확하고 유용한 답변을 제공해주세요.
답변은 한국어로 작성해주세요."""

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 시스템 프롬프트를 첫 메시지로 추가
    st.session_state.messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT
    })

# 채팅 입력 UI
user_input = st.chat_input("메시지를 입력하세요...")

# 사용자 입력이 있을 경우
if user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.write(user_input)
    
    # Gemini API 호출을 위한 대화 컨텍스트 구성
    chat = model.start_chat(history=[])
    
    # 이전 대화 내역을 모델에 전달
    for message in st.session_state.messages[1:]:  # 시스템 프롬프트 제외
        if message["role"] == "user":
            chat.send_message(message["content"])
        elif message["role"] == "assistant":
            chat.send_message(message["content"])
    
    # Gemini 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            response = chat.send_message(user_input)
            assistant_response = response.text
            
            # 어시스턴트 응답을 세션 상태에 추가
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            # 응답 표시
            
            st.write(assistant_response)

# 이전 대화 내역 표시 (시스템 프롬프트 제외)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.write(message["content"])
