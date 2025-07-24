import streamlit as st
import numpy as np
import random

BOARD_SIZE = 15
EMPTY = 0
PLAYER = 1
AI = 2

# 승리 조건 확인 함수
def check_win(board, player):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != player:
                continue
            # 가로
            if j <= BOARD_SIZE - 5 and all(board[i][j+k] == player for k in range(5)):
                return True
            # 세로
            if i <= BOARD_SIZE - 5 and all(board[i+k][j] == player for k in range(5)):
                return True
            # 대각 (↘)
            if i <= BOARD_SIZE - 5 and j <= BOARD_SIZE - 5 and all(board[i+k][j+k] == player for k in range(5)):
                return True
            # 대각 (↙)
            if i <= BOARD_SIZE - 5 and j >= 4 and all(board[i+k][j-k] == player for k in range(5)):
                return True
    return False

# AI 랜덤 수
def ai_move(board):
    empties = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == EMPTY]
    return random.choice(empties) if empties else None

# 이모지로 표현
def stone_symbol(value):
    if value == PLAYER:
        return "●"
    elif value == AI:
        return "○"
    else:
        return "➖"

# 초기 설정
if "board" not in st.session_state:
    st.session_state.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.game_over = False
    st.session_state.message = ""

st.title("🎮 오목 대결: 나 vs AI")
st.markdown("👉 당신은 **흑돌(●)** 입니다.")

# 게임판 표시
for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for j in range(BOARD_SIZE):
        with cols[j]:
            btn_label = stone_symbol(st.session_state.board[i][j])
            if st.button(btn_label, key=f"{i}-{j}"):
                if st.session_state.board[i][j] == EMPTY and not st.session_state.game_over:
                    # 플레이어 수
                    st.session_state.board[i][j] = PLAYER
                    if check_win(st.session_state.board, PLAYER):
                        st.session_state.message = "🎉 승리! 당신이 이겼습니다!"
                        st.session_state.game_over = True
                    else:
                        # AI 수
                        move = ai_move(st.session_state.board)
                        if move:
                            ai_i, ai_j = move
                            st.session_state.board[ai_i][ai_j] = AI
                            if check_win(st.session_state.board, AI):
                                st.session_state.message = "😢 패배! AI가 승리했습니다."
                                st.session_state.game_over = True

# 메시지 출력
if st.session_state.message:
    st.subheader(st.session_state.message)

# 다시 시작
if st.button("🔁 다시 시작"):
    st.session_state.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.game_over = False
    st.session_state.message = ""
