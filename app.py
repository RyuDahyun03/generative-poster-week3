# generative-poster-week3

import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import colorsys

# --- 0. Streamlit Setup and State Initialization ---

st.set_page_config(layout="centered", page_title="Generative Poster Styles")

# 세션 상태 초기화: 포스터 시드 저장 (버튼 클릭 시 새 포스터 생성)
if 'poster_seed' not in st.session_state:
    st.session_state.poster_seed = random.randint(0, 1000000)

# --- 1. Palette Functions (색상 팔레트 함수) ---

def palette_pastel(k=6):
    """파스텔 색상 팔레트 생성"""
    # k는 무시하고 항상 6개의 색상을 반환하도록 k=6으로 고정
    return [(random.uniform(0.7, 1.0), random.uniform(0.7, 1.0), random.uniform(0.7, 1.0)) for _ in range(k)]

def palette_vivid_hsv(k=6):
    """선명한 고대비 색상 팔레트 생성 (HSV 색 공간 사용)"""
    colors = []
    for _ in range(k):
        hue = random.random()
        saturation = random.uniform(0.8, 1)
        value = random.uniform(0.9, 1)
        colors.append(colorsys.hsv_to_rgb(hue, saturation, value))
    return colors

def palette_muted(k=6):
    """톤 다운된 차분한 색상 팔레트 생성 (HSV 색 공간 사용)"""
    colors = []
    for _ in range(k):
        hue = random.random()
        saturation = random.uniform(0.1, 0.3)
        value = random.uniform(0.4, 0.7)
        colors.append(colorsys.hsv_to_rgb(hue, saturation, value))
    return colors

# --- 2. Blob Function (도형 좌표 생성 함수) ---

def blob(center, r, points=200, wobble=0.15):
    """울퉁불퉁한 도형 좌표 생성"""
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- 3. Main Drawing Function (메인 드로잉 함수) ---

def generate_poster(style="Pastel", seed=0):
    """지정된 스타일에 따라 추상 포스터를 생성하고 Matplotlib Figure 객체를 반환합니다."""

    # 시드 설정
    random.seed(seed)
    np.random.seed(seed)

    presets = {
        "Minimal": {
            "n_layers": 8, "radius_range": (0.05, 0.20), "wobble_range": (0.01, 0.10),
            "alpha_range": (0.4, 0.7), "palette_func": palette_muted, "bg_color": (0.95, 0.95, 0.95)
        },
        "Vivid": {
            "n_layers": 25, "radius_range": (0.15, 0.45), "wobble_range": (0.10, 0.30),
            "alpha_range": (0.3, 0.6), "palette_func": palette_vivid_hsv, "bg_color": (0.1, 0.1, 0.1)
        },
        "NoiseTouch": {
            "n_layers": 50, "radius_range": (0.05, 0.15), "wobble_range": (0.4, 0.8),
            "alpha_range": (0.1, 0.3), "palette_func": palette_vivid_hsv, "bg_color": (0.98, 0.98, 0.97)
        },
        "Pastel": {
            "n_layers": 15, "radius_range": (0.10, 0.35), "wobble_range": (0.05, 0.25),
            "alpha_range": (0.25, 0.6), "palette_func": palette_pastel, "bg_color": (0.98, 0.98, 0.97)
        }
    }

    params = presets.get(style, presets["Pastel"])
    
    # Matplotlib Figure 생성
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis('off')
    ax.set_facecolor(params["bg_color"])

    # 팔레트 생성
    palette = params["palette_func"](6)

    # 레이어 드로잉 루프
    for _ in range(params["n_layers"]):
        cx, cy = random.random(), random.random()
        rr = random.uniform(*params["radius_range"])
        wobble_val = random.uniform(*params["wobble_range"])
        alpha_val = random.uniform(*params["alpha_range"])

        x, y = blob(center=(cx, cy), r=rr, wobble=wobble_val)
        color = random.choice(palette)
        ax.fill(x, y, color=color, alpha=alpha_val, edgecolor=(0, 0, 0, 0))

    # 텍스트 설정
    text_color = (0.9, 0.9, 0.9) if style == "Vivid" else (0.1, 0.1, 0.1)
    ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', color=text_color, transform=ax.transAxes)
    ax.text(0.05, 0.91, f"Style • {style}", fontsize=11, color=text_color, transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    return fig

# --- 4. Streamlit UI Layout (Streamlit UI 레이아웃) ---

st.title("🖼️ 추상 포스터 스타일 생성기")

# UI 컨트롤 영역
col1, col2 = st.columns([1, 2])

# 스타일 선택
style_options = ["Pastel", "Vivid", "Minimal", "NoiseTouch"]
selected_style = col1.selectbox(
    "포스터 스타일 선택", 
    options=style_options,
    index=style_options.index("Pastel")
)

# 새 포스터 생성 버튼
if col1.button("✨ 새 포스터 생성", type="primary"):
    # 버튼 클릭 시 새로운 무작위 시드 생성
    st.session_state.poster_seed = random.randint(0, 1000000)

col1.caption(f"현재 시드: {st.session_state.poster_seed}")
col1.markdown("---")
col1.info("새 포스터 생성 버튼을 누르거나, 스타일을 변경할 때마다 포스터가 업데이트됩니다.")

with col2:
    st.subheader(f"선택된 스타일: {selected_style}")
    
    # 현재 상태(스타일 및 시드)를 사용하여 포스터 생성 및 표시
    poster_fig = generate_poster(style=selected_style, seed=st.session_state.poster_seed)
    st.pyplot(poster_fig)
    plt.close(poster_fig) # 메모리 누수 방지를 위해 그림 닫기
