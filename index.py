import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="Nebula",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

        .stApp {
            background-color: #0b0c10;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(76, 29, 149, 0.2), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(14, 116, 144, 0.2), transparent 25%);
            font-family: 'Space Grotesk', sans-serif;
        }

        h1, h2, h3, p, div, span, label {
            font-family: 'Space Grotesk', sans-serif !important;
            color: #e2e8f0 !important;
        }

        .block-container {
            padding-top: 4rem;
            max-width: 850px;
        }

        .nebula-header {
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }

        .nebula-title {
            font-size: 3.5rem;
            font-weight: 700;
            letter-spacing: -1px;
            background: linear-gradient(90deg, #c084fc, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(192, 132, 252, 0.3);
            margin-bottom: 0.5rem;
        }

        .nebula-subtitle {
            font-size: 1.1rem;
            color: #94a3b8 !important;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .glass-panel {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        div[data-testid="stFileUploader"] {
            background: rgba(15, 23, 42, 0.6);
            border: 1px dashed rgba(192, 132, 252, 0.5);
            border-radius: 16px;
            padding: 1rem;
        }

        div[data-testid="stFileUploader"] section {
            background: transparent !important;
        }

        div[data-testid="stFileUploader"] button {
            background: linear-gradient(90deg, #9333ea, #0891b2) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            padding: 0.5rem 1.5rem !important;
        }

        .data-stream {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 0.6rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .data-stream:last-child {
            border-bottom: none;
        }

        .stream-marker {
            color: #22d3ee;
            font-weight: bold;
        }

        .stream-text {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.05rem;
            line-height: 1.5;
            word-break: break-word;
        }

        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="nebula-header">', unsafe_allow_html=True)
st.markdown('<div class="nebula-title">Nebula</div>', unsafe_allow_html=True)
st.markdown('<div class="nebula-subtitle">Анализ данных</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def init_sensor():
    return easyocr.Reader(['ru', 'en'], gpu=False)

sensor = init_sensor()

st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("### Сканирование объекта")
st.markdown("Загрузите изображение для извлечения текста.")
uploaded_file = st.file_uploader(
    "Сектор загрузки",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### Визуализация объекта")
    st.image(image, use_container_width=True, caption=f"Источник: {uploaded_file.name}")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.spinner("Анализ..."):
        img_np = np.array(image)
        result = sensor.readtext(img_np, detail=0)

    if result:
        st.success("Анализ завершён.")
        
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### Извлечённый поток данных")
        for line in result:
            st.markdown(
                f'<div class="data-stream"><span class="stream-marker">◈</span><span class="stream-text">{line}</span></div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        filename = f"nebula_log_{uploaded_file.name}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(result))

        st.info(f"Поток сохранён в архив: `{filename}`")
    else:
        st.warning("Сигнал не обнаружен. Попробуйте другой источник.")