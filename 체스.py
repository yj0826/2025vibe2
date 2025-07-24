import streamlit as st
import chess
import chess.svg
from stockfish import Stockfish
import tempfile
import os
import time
from PIL import Image
import cairosvg

# ====== 경로 설정 ======
STOCKFISH_PATH = "/path/to/your/stockfish"  # 예: "C:/stockfish/stockfish-windows-x86-64-avx2.exe"

# ====== 초기 설정 ======
st.set_page_config(page_title="♟️ 체스 vs AI", layout="centered")
st.title("♟️ 나 vs AI 체스")

# ====== 세션 상태 초기화 ======
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.moves = []
    st.session_state.turn = "사용자"  # 첫 수는 사용자
    st.session_state.game_over = False

# ====== 체스 엔진 설정 ======
stockfish = Stockfish(path=STOCKFISH_PATH)
stockfish.set_skill_level(6)

# ====== 체스판 그리기 함수 ======
def render_board(board):
    svg_data = chess.svg.board(board=board, size=400)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as png_file:
        cairosvg.svg2png(bytestring=svg_data, write_to=png_file.name)
        img = Image.open(png_file.name)
        st.image(img)
    os.unlink(png_file.name)

# ====== 게임 상태 확인 ======
if st.session_state.board.is_game_over():
    st.session_state.game_over = True
    result = st.session_state.board.result()
    if result == "1-0":
        st.success("🎉 승리! (백)")
    elif result == "0-1":
        st.error("😢 패배! (흑)")
    else:
        st.info("🤝 무승부!")
    if st.button("🔄 다시 시작하기"):
        st.session_state.board = chess.Board()
        st.session_state.moves = []
        st.session_state.turn = "사용자"
        st.session_state.game_over = False
        st.experimental_rerun()
    st.stop()

# ====== 체스판 표시 ======
render_board(st.session_state.board)
st.markdown(f"🔄 현재 턴: **{st.session_state.turn}**")

# ====== 사용자 수 입력 ======
user_move = st.text_input("당신의 수를 입력하세요 (예: e2e4)").strip().lower()

if st.button("♟️ 수 두기"):
    if st.session_state.board.is_game_over():
        st.warning("게임이 종료되었습니다.")
    elif st.session_state.turn != "사용자":
        st.warning("지금은 AI 차례입니다.")
    elif not user_move:
        st.warning("수를 입력하세요.")
    else:
        try:
            move = chess.Move.from_uci(user_move)
            if move in st.session_state.board.legal_moves:
                st.session_state.board.push(move)
                st.session_state.moves.append(user_move)
                st.session_state.turn = "AI"
            else:
                st.error("🚫 유효하지 않은 수입니다.")
        except:
            st.error("❌ 형식이 올바르지 않아요 (예: e2e4)")

# ====== AI 차례 처리 ======
if st.session_state.turn == "AI" and not st.session_state.board.is_game_over():
    stockfish.set_fen_position(st.session_state.board.fen())
    ai_move = stockfish.get_best_move()
    if ai_move:
        st.session_state.board.push_uci(ai_move)
        st.session_state.moves.append(ai_move)
        st.session_state.turn = "사용자"
        st.success(f"🤖 AI 수: {ai_move}")
        time.sleep(0.5)

# ====== 수 기록 표시 ======
if st.session_state.moves:
    st.markdown("### 📝 수 기록")
    for i in range(0, len(st.session_state.moves), 2):
        white = st.session_state.moves[i]
        black = st.session_state.moves[i + 1] if i + 1 < len(st.session_state.moves) else ""
        st.write(f"{i//2 + 1}. {white} {black}")
