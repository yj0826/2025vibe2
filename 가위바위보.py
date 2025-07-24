import streamlit as st
import random
import time

st.set_page_config(page_title="귀여운 가위바위보", page_icon="🐣")

st.markdown("<h1 style='text-align: center;'>🐣 가위바위보 게임</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>입력창에 <strong>가위</strong>, <strong>바위</strong>, <strong>보</strong> 중 하나를 입력해보세요!</p>", unsafe_allow_html=True)

# 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []

choices = ["가위", "바위", "보"]
emojis = {"가위": "✌", "바위": "✊", "보": "✋"}

# 귀여운 캐릭터 이미지
USER_IMG = "https://i.ibb.co/zG8rKcm/chick-user.png"
COMP_IMG = "https://i.ibb.co/X44tXpz/chick-comp.png"

# 사용자 입력
st.markdown("### ✏️ 입력하기")
user_input = st.text_input("👉 여기에 입력:", placeholder="가위 / 바위 / 보").strip()

# 게임 로직
if user_input:
    if user_input not in choices:
        st.warning("⚠️ '가위', '바위', '보' 중 하나만 입력해 주세요.")
    else:
        # 애니메이션 효과 (컴퓨터 생각 중)
        with st.spinner("🤖 컴퓨터가 선택 중입니다..."):
            time.sleep(1.5)  # 애니메이션 대기

        computer_choice = random.choice(choices)

        # 결과 출력
        st.markdown("### 🎮 게임 결과")
        col1, col2 = st.columns(2)
        with col1:
            st.image(USER_IMG, width=120)
            st.markdown(f"<div style='text-align:center;'>🙋‍♀️ 당신: {emojis[user_input]} {user_input}</div>", unsafe_allow_html=True)
        with col2:
            st.image(COMP_IMG, width=120)
            st.markdown(f"<div style='text-align:center;'>🤖 컴퓨터: {emojis[computer_choice]} {computer_choice}</div>", unsafe_allow_html=True)

        if user_input == computer_choice:
            st.info("🤝 비겼어요! +1점")
            st.session_state.score += 1
            result = "무승부"
        elif (user_input == "가위" and computer_choice == "보") or \
             (user_input == "바위" and computer_choice == "가위") or \
             (user_input == "보" and computer_choice == "바위"):
            st.success("🎉 이겼어요! +2점")
            st.session_state.score += 2
            result = "승리"
        else:
            st.error("😢 졌어요... -1점")
            st.session_state.score -= 1
            result = "패배"

        # 기록 저장
        st.session_state.history.append({
            "나": user_input,
            "컴퓨터": computer_choice,
            "결과": result
        })

# 점수 출력
st.markdown("---")
st.markdown(f"<h3 style='text-align:center;'>🧮 현재 점수: <span style='color:#4CAF50;'>{st.session_state.score}점</span></h3>", unsafe_allow_html=True)

# 기록 출력
if st.session_state.history:
    st.markdown("### 📜 최근 게임 기록")
    for i, h in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.markdown(f"{i}. 나: {emojis[h['나']]} {h['나']} | 컴퓨터: {emojis[h['컴퓨터']]} {h['컴퓨터']} | 결과: **{h['결과']}**")

# 리셋
if st.button("🔄 점수 및 기록 초기화"):
    st.session_state.score = 0
    st.session_state.history = []
    st.experimental_rerun()

