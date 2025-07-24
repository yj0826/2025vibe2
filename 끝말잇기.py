import streamlit as st
import random
import time
import os

st.set_page_config(page_title="끝말잇기 게임", page_icon="🍎")

st.title("🍎 한글 끝말잇기 게임")
st.markdown("**10초 안에 끝말잇기를 이어가세요!**")

# 사전 불러오기
@st.cache_data
def load_dictionary():
    if not os.path.exists("words.txt"):
        return []
    with open("words.txt", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]
    return list(set(words))

dictionary = load_dictionary()

# 세션 상태 초기화
if "used_words" not in st.session_state:
    st.session_state.used_words = []
if "last_word" not in st.session_state:
    st.session_state.last_word = ""
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "turn_start_time" not in st.session_state:
    st.session_state.turn_start_time = time.time()

# 타이머
current_time = time.time()
remaining_time = 10 - int(current_time - st.session_state.turn_start_time)

if not st.session_state.game_over:
    if remaining_time <= 0:
        st.error("⏰ 시간 초과! AI의 승리입니다.")
        st.session_state.game_over = True
    else:
        st.warning(f"⏳ 남은 시간: {remaining_time}초")

# 게임 리셋
if st.button("🔄 게임 다시 시작"):
    st.session_state.used_words = []
    st.session_state.last_word = ""
    st.session_state.game_over = False
    st.session_state.turn_start_time = time.time()
    st.experimental_rerun()

# 단어 입력
if not st.session_state.game_over and remaining_time > 0:
    user_input = st.text_input("당신의 단어:", key="word_input")

    if st.button("제출"):
        word = user_input.strip()
        if not word:
            st.warning("단어를 입력해주세요!")
        elif word in st.session_state.used_words:
            st.error("이미 사용된 단어예요!")
        elif word not in dictionary:
            st.error("사전에 없는 단어예요!")
        elif st.session_state.last_word and word[0] != st.session_state.last_word[-1]:
            st.error(f"'{st.session_state.last_word[-1]}'(으)로 시작해야 해요!")
        else:
            st.success(f"🧑 당신: {word}")
            st.session_state.used_words.append(word)
            st.session_state.last_word = word

            # AI 차례
            last_char = word[-1]
            candidates = [w for w in dictionary if w not in st.session_state.used_words and w[0] == last_char]

            if candidates:
                ai_word = random.choice(candidates)
                st.info(f"🤖 AI: {ai_word}")
                st.session_state.used_words.append(ai_word)
                st.session_state.last_word = ai_word
                st.session_state.turn_start_time = time.time()
                st.experimental_rerun()
            else:
                st.success("🎉 당신의 승리입니다! AI가 단어를 못 찾았어요.")
                st.session_state.game_over = True
else:
    if st.session_state.game_over:
        st.info("게임이 종료되었습니다. '게임 다시 시작'을 눌러주세요.")

