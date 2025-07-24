import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="숫자 맞추기 게임", page_icon="🔢")

st.title("🔢 숫자 맞추기 게임")
st.markdown("최대 **4자리 숫자(1~9999)** 중 하나를 맞춰보세요!")
st.markdown("기회는 **20번**입니다. UP / DOWN 힌트로 도와드릴게요. 😊")

# 세션 상태 초기화
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(1, 9999)
    st.session_state.tries = 0
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.rankings = []  # 게임 성공시 기록 저장

# 입력창
if not st.session_state.game_over:
    guess = st.number_input("숫자를 입력하세요 (1~9999):", min_value=1, max_value=9999, step=1, format="%d")

    if st.button("🔍 제출하기"):
        st.session_state.tries += 1
        answer = st.session_state.answer

        if guess == answer:
            st.success(f"🎉 정답입니다! {st.session_state.tries}번 만에 맞췄어요!")
            st.session_state.game_over = True

            # 랭킹에 추가
            st.session_state.rankings.append(st.session_state.tries)
            st.session_state.rankings = sorted(st.session_state.rankings)[:5]  # 상위 5개만 저장
        elif guess < answer:
            st.info("📈 UP! 더 큰 수를 입력해보세요.")
            st.session_state.history.append((guess, "UP"))
        else:
            st.info("📉 DOWN! 더 작은 수를 입력해보세요.")
            st.session_state.history.append((guess, "DOWN"))

        if st.session_state.tries >= 20 and guess != answer:
            st.error(f"💥 게임 오버! 정답은 {answer}였습니다.")
            st.session_state.game_over = True

# 시도 기록 표시
if st.session_state.history:
    st.markdown("### 📝 시도 기록")
    for idx, (g, hint) in enumerate(reversed(st.session_state.history[-10:]), 1):
        st.markdown(f"{idx}. 입력: **{g}** → 힌트: **{hint}**")

# 남은 기회
if not st.session_state.game_over:
    remaining = 20 - st.session_state.tries
    st.markdown(f"🕐 남은 기회: **{remaining}번**")

# 랭킹 표시
if st.session_state.rankings:
    st.markdown("### 🏆 베스트 기록 (시도 수 기준)")
    for i, r in enumerate(st.session_state.rankings, 1):
        st.write(f"{i}위: {r}번 만에 성공")

# 다시 시작
if st.session_state.game_over:
    if st.button("🔄 다시 시작하기"):
        st.session_state.answer = random.randint(1, 9999)
        st.session_state.tries = 0
        st.session_state.game_over = False
        st.session_state.history = []
        st.experimental_rerun()
