import streamlit as st
import pickle
import pandas as pd

# Modeli yükle
model_path = "rf_model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Streamlit başlığı ortalı
st.markdown("<h1 style='text-align: center;'>Hastalık Durumu Tahmin Uygulaması</h1>", unsafe_allow_html=True)

# Center the buttons
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

# "Temizle" button to reset the form
if st.button("Temizle"):
    # Reset all form values to None
    st.session_state.tur = None
    st.session_state.inkordinasyon = None
    st.session_state.ishal = None
    st.session_state.istahsızlık = None
    st.session_state.kusma = None
    st.session_state.solunum_guclugu = None
    st.session_state.GRAN = None
    st.session_state.GRAN_A = None
    st.session_state.LYM = None
    st.session_state.LYM_A = None
    st.session_state.MON = None
    st.session_state.HCT = None
    st.session_state.MCH = None
    st.session_state.MCHC = None
    st.session_state.MCV = None
    st.session_state.RDW = None
    st.session_state.WBC = None

st.markdown("</div>", unsafe_allow_html=True)

# Categorical inputs section
st.markdown("**Anamnez Bilgileri**")
cat_col1, cat_col2, cat_col3 = st.columns(3)
with cat_col1:
    tur = st.selectbox("Tür", options=[None, 1, 0], format_func=lambda x: "Seçiniz" if x is None else ("Köpek" if x == 1 else "Kedi"), key="tur")
with cat_col2:
    inkordinasyon = st.selectbox("İnkordinasyon", options=[None, 1, 0], format_func=lambda x: "Seçiniz" if x is None else ("Var" if x == 1 else "Yok"), key="inkordinasyon")
with cat_col3:
    ishal = st.selectbox("İshal", options=[None, 1, 0], format_func=lambda x: "Seçiniz" if x is None else ("Var" if x == 1 else "Yok"), key="ishal")

# Categorical inputs continued
cat_col4, cat_col5, cat_col6 = st.columns(3)
with cat_col4:
    istahsızlık = st.selectbox("İştahsızlık", options=[None, 1, 0], format_func=lambda x: "Seçiniz" if x is None else ("Var" if x == 1 else "Yok"), key="istahsızlık")
with cat_col5:
    kusma = st.selectbox("Kusma", options=[None, 1, 0], format_func=lambda x: "Seçiniz" if x is None else ("Var" if x == 1 else "Yok"), key="kusma")
with cat_col6:
    solunum_guclugu = st.selectbox("Solunum Güçlüğü", options=[None, 1, 0], format_func=lambda x: "Seçiniz" if x is None else ("Var" if x == 1 else "Yok"), key="solunum_guclugu")

# Numeric inputs section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("**Hemogram Değerleri**")
num_col1, num_col2, num_col3 = st.columns(3)
with num_col1:
    GRAN = st.number_input("GRAN", value=None, format="%.2f", key="GRAN")
    LYM = st.number_input("LYM", value=None, format="%.2f", key="LYM")
    MCH = st.number_input("MCH", value=None, format="%.2f", key="MCH")
with num_col2:
    GRAN_A = st.number_input("GRAN_A", value=None, format="%.2f", key="GRAN_A")
    LYM_A = st.number_input("LYM_A", value=None, format="%.2f", key="LYM_A")
    MCHC = st.number_input("MCHC", value=None, format="%.2f", key="MCHC")
with num_col3:
    MON = st.number_input("MON", value=None, format="%.2f", key="MON")
    HCT = st.number_input("HCT", value=None, format="%.2f", key="HCT")
    MCV = st.number_input("MCV", value=None, format="%.2f", key="MCV")

# Remaining numeric inputs
num_col4, num_col5, num_col6 = st.columns(3)
with num_col4:
    RDW = st.number_input("RDW", value=None, format="%.2f", key="RDW")
with num_col5:
    WBC = st.number_input("WBC", value=None, format="%.2f", key="WBC")

# Centered prediction button
if st.button("Tahmin Et", key="predict"):
    # Validate input fields for empty values
    numeric_inputs = {
        "GRAN": st.session_state.GRAN, "GRAN_A": st.session_state.GRAN_A, "LYM": st.session_state.LYM, 
        "LYM_A": st.session_state.LYM_A, "MON": st.session_state.MON, "HCT": st.session_state.HCT, 
        "MCH": st.session_state.MCH, "MCHC": st.session_state.MCHC, "MCV": st.session_state.MCV, 
        "RDW": st.session_state.RDW, "WBC": st.session_state.WBC
    }
    categorical_inputs = {
        "Tür": st.session_state.tur, "İnkordinasyon": st.session_state.inkordinasyon, "İshal": st.session_state.ishal,
        "İştahsızlık": st.session_state.istahsızlık, "Kusma": st.session_state.kusma, "Solunum Güçlüğü": st.session_state.solunum_guclugu
    }

    # Check for missing numeric values
    missing_numeric_values = [name for name, value in numeric_inputs.items() if value is None]
    # Check for missing categorical selections
    missing_categorical_values = [name for name, value in categorical_inputs.items() if value is None]

    # Display warnings for missing values
    if missing_numeric_values or missing_categorical_values:
        if missing_numeric_values:
            st.warning(f"Lütfen {', '.join(missing_numeric_values)} değerlerini doldurunuz.")
        if missing_categorical_values:
            st.warning(f"Lütfen {', '.join(missing_categorical_values)} seçeneklerini seçiniz.")
    else:
        # Prepare data for model prediction
        data = [[st.session_state.tur, st.session_state.GRAN, st.session_state.GRAN_A, st.session_state.LYM, 
                 st.session_state.LYM_A, st.session_state.MON, st.session_state.HCT, st.session_state.MCH, 
                 st.session_state.MCHC, st.session_state.MCV, st.session_state.RDW, st.session_state.WBC, 
                 st.session_state.inkordinasyon, st.session_state.ishal, st.session_state.istahsızlık, 
                 st.session_state.kusma, st.session_state.solunum_guclugu]]
        prediction = model.predict(data)[0]

        # Display the prediction result centered
        st.markdown("<h2 style='text-align: center;'>Tahmin Sonucu: {}</h2>".format(prediction), unsafe_allow_html=True)
