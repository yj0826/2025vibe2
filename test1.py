import streamlit as st
import numpy as np
import random
import time

# 게임 설정
BOARD_SIZE = 9
NUM_MINES = 10
TIME_LIMIT = 20 * 60  # 20분 (초 단위)

# 지뢰 보드 생성
def create_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    mines = random.sample(range(BOARD_SIZE * BOARD_SIZE), NUM_MINES)
    for m in mines:
        row, col = divmod(m, BOARD_SIZE)
        board[row, col] = -1  # 지뢰는 -1
    # 주변 지뢰 수 계산
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row, col] == -1:
                continue
            count = sum(
                board[r, c] == -1
                for r in range(max(0, row - 1), min(BOARD_SIZE, row + 2))
                for c in range(max(0, col - 1), min(BOARD_SIZE, col + 2))
            )
            board[row, col] = count
    return board

# 초기화
if "board" not in st.session_state:
    st.session_state.board = create_board()
    st.session_state.revealed = np.full((BOARD_SIZE, BOARD_SIZE), False)
    st.session_state.game_over = False
    st.session_state.start_time = time.time()
    st.session_state.flagged = np.full((BOARD_SIZE, BOARD_SIZE), False)
    st.session_state.win = False

# 타이머
elapsed = time.time() - st.session_state.start_time
remaining = TIME_LIMIT - int(elapsed)

st.title("🧨 지뢰찾기")
st.write(f"⏱️ 남은 시간: {remaining//60}분 {remaining%60}초")

if remaining <= 0:
    st.session_state.game_over = True
    st.warning("⏰ 시간이 초과되었습니다! 게임 오버.")

def reveal_cell(row, col):
    if st.session_state.revealed[row, col] or st.session_state.flagged[row, col]:
        return
    st.session_state.revealed[row, col] = True
    if st.session_state.board[row, col] == -1:
        st.session_state.game_over = True
    elif st.session_state.board[row, col] == 0:
        # 재귀적으로 주변 셀 열기
        for r in range(max(0, row - 1), min(BOARD_SIZE, row + 2)):
            for c in range(max(0, col - 1), min(BOARD_SIZE, col + 2)):
                if not st.session_state.revealed[r, c]:
                    reveal_cell(r, c)

# 보드 표시
for row in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for col in range(BOARD_SIZE):
        cell_label = " "
        if st.session_state.revealed[row, col]:
            val = st.session_state.board[row, col]
            cell_label = "💣" if val == -1 else (str(val) if val > 0 else "")
            cols[col].markdown(f"**{cell_label}**")
        elif st.session_state.flagged[row, col]:
            if cols[col].button("🚩", key=f"flag_{row}_{col}"):
                st.session_state.flagged[row, col] = False
        else:
            if cols[col].button("⬜", key=f"cell_{row}_{col}"):
                reveal_cell(row, col)

# 승리 조건 체크
if not st.session_state.game_over:
    unrevealed = np.sum(~st.session_state.revealed)
    if unrevealed == NUM_MINES:
        st.session_state.win = True
        st.session_state.game_over = True

# 결과 표시
if st.session_state.game_over:
    if st.session_state.win:
        st.success("🎉 승리! 모든 지뢰를 피해냈어요!")
    else:
        st.error("💥 지뢰를 밟았어요! 게임 오버입니다.")
    if st.button("🔄 다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
