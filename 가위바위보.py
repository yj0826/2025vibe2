import streamlit as st
import random

st.title("✊ ✋ ✌ 가위바위보 게임")

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []

choices = ["가위", "바위", "보"]
emojis = {"가위": "✌", "바위": "✊", "보": "✋"}

user_choice = st.radio("당신의 선택은?", choices, index=None, horizontal=True)

if user_choice:
    computer_choice = random.choice(choices)

    st.markdown("### 결과")
    st.write(f"당신의 선택: {emojis[user_choice]} {user_choice}")
    st.write(f"컴퓨터의 선택: {emojis[computer_choice]} {computer_choice}")

    if user_choice == computer_choice:
        st.info("🤝 비겼어요! (+1점)")
        st.session_state.score += 1
        result = "무승부"
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        st.success("🎉 당신이 이겼어요! (+2점)")
        st.session_state.score += 2
        result = "승리"
    else:
        st.error("😢 당신이 졌어요! (-1점)")
        st.session_state.score -= 1
        result = "패배"

    # 기록 저장
    st.session_state.history.append({
        "나": user_choice,
        "컴퓨터": computer_choice,
        "결과": result
    })

    st.markdown(f"### 🧮 현재 점수: **{st.session_state.score}점**")

    # 결과 히스토리 출력
    if st.session_state.history:
        st.markdown("### 📝 게임 기록")
        for i, h in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.write(f"{i}. 나: {h['나']} | 컴퓨터: {h['컴퓨터']} | 결과: {h['결과']}")

    # 다시 하기 버튼
    if st.button("🔄 다음 판 하기"):
        st.experimental_rerun()

# 전체 초기화
if st.button("🧹 점수 및 기록 초기화"):
    st.session_state.score = 0
    st.session_state.history = []
    st.experimental_rerun()
