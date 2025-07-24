import streamlit as st
import chess
import chess.svg
import tempfile
from PIL import Image
import cairosvg
import os

st.set_page_config(page_title="체스 연습판", layout="centered")
st.title("♟️ 체스 연습용 웹앱")

# 세션 초기화
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.move_history = []

# 체스판 시각화 함수
def render_board(board):
    svg = chess.svg.board(board, size=400)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as png_file:
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=png_file.name)
        img = Image.open(png_file.name)
        st.image(img)
    os.unlink(png_file.name)

# 체스판 출력
render_board(st.session_state.board)

# 수 입력
move_input = st.text_input("수 입력 (예: e2e4)").strip()

if st.button("두기"):
    try:
        move = chess.Move.from_uci(move_input)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.move_history.append(move_input)
        else:
            st.warning("🚫 불가능한 수입니다.")
    except:
        st.warning("❌ 올바른 형식이 아닙니다 (예: e2e4).")

# 되돌리기
if st.button("↩️ 한 수 되돌리기"):
    if st.session_state.board.move_stack:
        st.session_state.board.pop()
        if st.session_state.move_history:
            st.session_state.move_history.pop()

# 전체 초기화
if st.button("🔄 게임 초기화"):
    st.session_state.board = chess.Board()
    st.session_state.move_history = []

# 수 기록
if st.session_state.move_history:
    st.markdown("### 📜 수 기록")
    for i, move in enumerate(st.session_state.move_history, 1):
        st.write(f"{i}. {move}")

# 게임 종료 여부
if st.session_state.board.is_game_over():
    st.markdown("### ❗ 게임 종료")
    st.write(f"결과: {st.session_state.board.result()}")

