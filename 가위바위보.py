import streamlit as st
import random

st.title("✊ ✋ ✌ 가위바위보 게임 (입력식)")

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []

choices = ["가위", "바위", "보"]
emojis = {"가위": "✌", "바위": "✊", "보": "✋"}

# 사용자 입력 받기
user_input = st.text_input("가위, 바위, 보 중 하나를 입력하세요:")

if user_input:
    user_input = user_input.strip()

    if user_input not in choices:
        st.warning("❗ 올바른 입력이 아닙니다. '가위', '바위', '보' 중 하나만 입력해 주세요.")
    else:
        computer_choice = random.choice(choices)

        st.markdown("### 결과")
        st.write(f"당신의 선택: {emojis[user_input]} {user_input}")
        st.write(f"컴퓨터의 선택: {emojis[computer_choice]} {computer_choice}")

        if user_input == computer_choice:
            st.info("🤝 비겼어요! (+1점)")
            st.session_state.score += 1
            result = "무승부"
        elif (user_input == "가위" and computer_choice == "보") or \
             (user_input == "바위" and computer_choice == "가위") or \
             (user_input == "보" and computer_choice == "바위"):
            st.success("🎉 당신이 이겼어요! (+2점)")
            st.session_state.score += 2
            result = "승리"
        else:
            st.error("😢 당신이 졌어요! (-1점)")
            st.session_state.score -= 1
            result = "패배"

        # 기록 저장
        st.session_state.history.append({
            "나": user_input,
            "컴퓨터": computer_choice,
            "결과": result
        })

        st.markdown(f"### 🧮 현재 점수: **{st.session_state.score}점**")

        # 결과 히스토리 출력
        if st.session_state.history:
            st.markdown("### 📝 게임 기록")
            for i, h in enumerate(reversed(st.session_state.history[-5:]), 1):
                st.write(f"{i}. 나: {h['나']} | 컴퓨터: {h['컴퓨터']} | 결과: {h['결과']}")

# 전체 초기화
if st.button("🧹 점수 및 기록 초기화"):
    st.session_state.score = 0
    st.session_state.history = []
    st.experimental_rerun()

