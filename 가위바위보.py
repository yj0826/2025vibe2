import streamlit as st
import random

st.title("✊ ✋ ✌ 가위바위보 게임")

# 선택지
choices = ["가위", "바위", "보"]
emojis = {"가위": "✌", "바위": "✊", "보": "✋"}

# 사용자 선택
user_choice = st.radio("당신의 선택은?", choices, index=None, horizontal=True)

if user_choice:
    computer_choice = random.choice(choices)

    st.write(f"당신의 선택: {emojis[user_choice]} {user_choice}")
    st.write(f"컴퓨터의 선택: {emojis[computer_choice]} {computer_choice}")

    # 승부 판단
    if user_choice == computer_choice:
        st.info("🤝 비겼어요!")
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        st.success("🎉 당신이 이겼어요!")
    else:
        st.error("😢 당신이 졌어요!")

    if st.button("🔄 다시 하기"):
        st.experimental_rerun()
