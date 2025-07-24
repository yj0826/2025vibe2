import streamlit as st
import numpy as np
from PIL import Image
import random

BOARD_SIZE = 15
EMPTY = 0
PLAYER = 1
AI = 2

# 이미지 불러오기
@st.cache_resource
def load_images():
    board_img = Image.open("board.jpg")
    black_stone = Image.open("black_stone.png").resize((30, 30))
    white_stone = Image.open("white_stone.png").resize((30, 30))
    return board_img, black_stone, white_stone

board_img, black_stone_img, white_stone_img = load_images()

# 승리 조건 확인
def check_win(board, player):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != player:
                continue
            if j <= BOARD_SIZE - 5 and all(board[i][j+k] == player for k in range(5)):
                return True
            if i <= BOARD_SIZE - 5 and all(board[i+k][j] == player for k in range(5)):
                return True
            if i <= BOARD_SIZE - 5 and j <= BOARD_SIZE - 5 and all(board[i+k][j+k] == player for k in range(5)):
                return True
            if i <= BOARD_SIZE - 5 and j >= 4 and all(board[i+k][j-k] == player for k in range(5)):
                return True
    return False

# AI 수 선택
def ai_move(board):
    def score_move(i, j, player):
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        score = 0
        for dx, dy in directions:
            count = 1
            for dir in [1, -1]:
                x, y = i, j
                while True:
                    x += dx * dir
                    y += dy * dir
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == player:
                        count += 1
                    else:
                        break
            if count >= 5:
                return 10000
            elif count == 4:
                score += 1000
            elif count == 3:
                score += 100
            elif count == 2:
                score += 10
        return score

    best_score = -1
    best_moves = []

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != EMPTY:
                continue
            if score_move(i, j, AI) >= 10000:
                return (i, j)
            if score_move(i, j, PLAYER) >= 10000:
                return (i, j)
            total_score = score_move(i, j, AI) + score_move(i, j, PLAYER) * 0.8
            if total_score > best_score:
                best_score = total_score
                best_moves = [(i, j)]
            elif total_score == best_score:
                best_moves.append((i, j))

    return random.choice(best_moves) if best_moves else None

# 세션 초기화
if "board" not in st.session_state:
    st.session_state.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.game_over = False
    st.session_state.message = ""

st.set_page_config(layout="wide")
st.title("🎯 AI와 리얼 오목 대결")
st.markdown("🧠 **당신은 흑돌 (●)** | **AI는 백돌 (○)**")

# 바둑판 이미지 배경
st.image(board_img, caption="바둑판", use_column_width=True)

# 게임판 출력
for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for j in range(BOARD_SIZE):
        with cols[j]:
            cell = st.session_state.board[i][j]
            if cell == PLAYER:
                st.image(black_stone_img)
            elif cell == AI:
                st.image(white_stone_img)
            else:
                if st.button(" ", key=f"{i}-{j}"):
                    if not st.session_state.game_over:
                        st.session_state.board[i][j] = PLAYER
                        if check_win(st.session_state.board, PLAYER):
                            st.session_state.message = "🎉 승리! 당신이 이겼습니다!"
                            st.session_state.game_over = True
                        else:
                            move = ai_move(st.session_state.board)
                            if move:
                                ai_i, ai_j = move
                                st.session_state.board[ai_i][ai_j] = AI
                                if check_win(st.session_state.board, AI):
                                    st.session_state.message = "😢 패배! AI가 승리했습니다."
                                    st.session_state.game_over = True

# 결과 메시지
if st.session_state.message:
    st.subheader(st.session_state.message)

# 다시 시작 버튼
if st.button("🔁 다시 시작"):
    st.session_state.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.game_over = False
    st.session_state.message = ""
