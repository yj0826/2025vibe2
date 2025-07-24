import streamlit as st
import random

st.set_page_config(page_title="끝말잇기 게임", page_icon="📝")

st.title("🎮 한글 끝말잇기 게임")
st.markdown("**단어를 입력하고 끝말잇기를 이어가 보세요!**")

# 예시 단어 리스트 (간단한 사전 역할)
basic_dictionary = [
    "사과", "과일", "일기", "기도", "도서", "서랍", "랍스터", "터널", "널빤지",
    "지하철", "철도", "도마", "마늘", "늘보", "보리", "리본", "본드", "드라이버"
]

# 세션 상태 초기화
if "used_words" not in st.session_state:
    st.session_state.used_words = []
if "last_word" not in st.session_state:
    st.session_state.last_word = ""
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# 게임 리셋 버튼
if st.button("🔄 게임 다시 시작"):
    st.session_state.used_words = []
    st.session_state.last_word = ""
    st.session_state.game_over = False
    st.success("게임을 초기화했어요!")

# 단어 입력
if not st.session_state.game_over:
    user_input = st.text_input("당신의 단어를 입력하세요:", "")

    if st.button("제출"):
        word = user_input.strip()

        # 유효성 검사
        if not word:
            st.warning("단어를 입력해주세요!")
        elif word in st.session_state.used_words:
            st.error("이미 사용된 단어예요!")
        elif word not in basic_dictionary:
            st.error("사전에 없는 단어예요!")
        elif st.session_state.last_word and word[0] != st.session_state.last_word[-1]:
            st.error(f"❌ '{st.session_state.last_word[-1]}'(으)로 시작하는 단어여야 해요!")
        else:
            st.success(f"🧑 당신: {word}")
            st.session_state.used_words.append(word)
            st.session_state.last_word = word

            # AI 차례
            last_char = word[-1]
            candidates = [w for w in basic_dictionary
                          if w not in st.session_state.used_words and w[0] == last_char]

            if candidates:
                ai_word = random.choice(candidates)
                st.session_state.used_words.append(ai_word)
                st.session_state.last_word = ai_word
                st.info(f"🤖 AI: {ai_word}")
            else:
                st.success("🎉 축하합니다! AI가 단어를 못 찾았어요. 당신의 승리입니다!")
                st.session_state.game_over = True
else:
    st.info("게임이 종료되었습니다. '게임 다시 시작'을 눌러 새로 시작하세요.")
