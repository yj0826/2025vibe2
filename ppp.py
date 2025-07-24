import streamlit as st
import numpy as np

st.set_page_config(page_title="🎨 색칠놀이", layout="wide")

# 설정
GRID_SIZE = 16
CELL_SIZE = 30  # 픽셀 크기(px)

# 색상 선택
st.sidebar.title("🎨 색상 선택")
selected_color = st.sidebar.color_picker("원하는 색을 고르세요!", "#ff0000")

# 세션 상태에 색상 그리드 저장
if "grid" not in st.session_state:
    st.session_state.grid = np.full((GRID_SIZE, GRID_SIZE), "#ffffff")

# 행렬 그리기
st.markdown("<h2 style='text-align: center;'>🧩 픽셀 색칠놀이</h2>", unsafe_allow_html=True)
for row in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for col in range(GRID_SIZE):
        cell_key = f"{row}-{col}"
        color = st.session_state.grid[row][col]
        if cols[col].button(" ", key=cell_key, help="눌러서 색칠하기",
                            args=(row, col),
                            use_container_width=True):
            st.session_state.grid[row][col] = selected_color
        # 스타일 적용 (버튼 배경색)
        cols[col].markdown(
            f"""<style>
                [data-testid="stButton"][key="{cell_key}"] button {{
                    background-color: {color};
                    height: {CELL_SIZE}px;
                    border-radius: 0;
                    padding: 0;
                    border: 1px solid #aaa;
                }}
            </style>""",
            unsafe_allow_html=True,
        )

# 초기화 버튼
if st.sidebar.button("전체 초기화"):
    st.session_state.grid = np.full((GRID_SIZE, GRID_SIZE), "#ffffff")
