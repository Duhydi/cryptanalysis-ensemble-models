import streamlit as st
import joblib
from feature_extraction import extract_features
import pandas as pd

st.markdown("""
<style>
/* màu nền tổng quát */
body {
    background-color: #f5f7fa;
}

/* tiêu đề chính */
.main-title {
    font-size: 38px;
    font-weight: 700;
    color: #2c3e50;
    text-align: center;
    padding-bottom: 10px;
}

/* subtitle */
.sub-title {
    font-size: 20px;
    font-weight: 500;
    color: #34495e;
    text-align: center;
    margin-bottom: 30px;
}

/* ô hiển thị kết quả */
.result-box {
    padding: 20px;
    background: #eafaf1;
    border-left: 6px solid #27ae60;
    border-radius: 8px;
    font-size: 20px;
    margin-top: 20px;
}

/* box nhập liệu */
.stTextArea textarea {
    border-radius: 10px !important;
    border: 2px solid #3498db;
}

/* nút dự đoán */
.stButton>button {
    background-color: #3498db;
    color: white;
    padding: .6rem 1.2rem;
    border-radius: 10px;
    border: none;
    font-size: 18px;
}

.stButton>button:hover {
    background-color: #217dbb;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title"> Cryptanalysis Classifier Demo</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Ứng dụng dự đoán loại mã hóa từ ciphertext</div>', unsafe_allow_html=True)

background_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2ZPstX4QA_A9gvQd-GyaoH5jS8rhJoJTzWQ&s"

st.markdown(
    f"""
    <style>
    /* Ảnh nền toàn màn hình */
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Lớp phủ mờ để dễ đọc chữ */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        backdrop-filter: blur(1515px) brightness(0.45);
        z-index: -1;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


model = joblib.load("best_model.pkl")

ciphertext = st.text_area("Nhập Ciphertext để dự đoán:", height=200)

if st.button("Dự đoán"):
    if ciphertext.strip() == "":
        st.warning("Bạn chưa nhập ciphertext!")
    else:
        df = pd.DataFrame([{'ciphertext': ciphertext}])
        features = extract_features(df)        
        prediction = model.predict(features)[0]
        cipher_map = {0: "Caesar", 1: "Playfair", 2: "Railfence", 3: "Vigenere", 4: "Xor"}
        st.success(f"→ Loại mã hóa dự đoán: **{cipher_map[prediction]}**")
