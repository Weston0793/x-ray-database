import streamlit as st
from google.cloud import firestore
from firebase_helpers import db, create_zip
import uuid
from google.api_core.exceptions import GoogleAPICallError
from search_backend import perform_search
from helper_functions import style_markdown, select_subregion, select_sub_subregion, select_sub_sub_subregion

def search_section():
    style_markdown()
    st.markdown('<div class="search-title">Képek keresése</div>', unsafe_allow_html=True)

    types = ["", "Normál", "Törött", "Egyéb"]
    views = ["", "AP", "Lateral", "Ferde", "PA", "Speciális"]
    regions = ["", "Felső végtag", "Alsó végtag", "Gerinc", "Koponya", "Mellkas", "Has"]

    # Type and view in one row
    col1, col2 = st.columns(2)
    with col1:
        type_sel = st.selectbox("Típus", types)
    with col2:
        view_sel = st.selectbox("Nézet", views)

    # Main and sub region in one row
    col3, col4 = st.columns(2)
    with col3:
        main_reg = st.selectbox("Fő régió", regions)
    with col4:
        sub_reg = select_subregion(main_reg)

    # Sub-subregion and sub-sub-subregion in one row
    col5, col6 = st.columns(2)
    with col5:
        sub_sub_reg = select_sub_subregion(sub_reg)
    with col6:
        sub_sub_sub_reg = select_sub_sub_subregion(sub_sub_reg)

    # Multiselects for complications and associated conditions
    comp = st.multiselect("Komplikációk", ["Nyílt", "Darabos", "Avulsio", "Luxatio", "Subluxatio", "Idegsérülés", "Nagyobb Érsérülés", "Szalagszakadás", "Meniscus Sérülés", "Epiphysis Sérülés", "Fertőzés"])
    cond = st.multiselect("Kórállapotok", ["Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Rheumatoid Arthritis", "Cysta", "Metastasis", "Malignus Tumor", "Benignus Tumor", "Genetikai"])

    # Age filter with checkbox
    age_flt = st.checkbox("Életkor (intervallum)")
    age_rng = st.slider("Életkor (intervallum)", min_value=0, max_value=120, value=(0, 18), step=1, format="%d") if age_flt else None

    age_grp = st.selectbox("Életkori csoport", ["", "Gyermek", "Felnőtt"])

    # Page and items per page in one row
    col7, col8 = st.columns(2)
    with col7:
        page = st.number_input("Oldal", min_value=1, step=1, value=1)
    with col8:
        items_pp = st.selectbox("Találatok/Oldal", options=[10, 25, 50, 100], index=0)

    # Initialize session state if not exists
    if 'q_params' not in st.session_state:
        st.session_state.q_params = {}

    # Button for search
    if st.button("Keresés", key="search_btn"):
        page = 1  # Reset to the first page on new search
        st.session_state.q_params = {
            "type": type_sel,
            "view": view_sel,
            "main_reg": main_reg,
            "sub_reg": sub_reg,
            "sub_sub_reg": sub_sub_reg,
            "sub_sub_sub_reg": sub_sub_sub_reg,
            "comp": comp,
            "cond": cond,
            "age_flt": age_flt,
            "age_rng": str(age_rng) if age_rng else "",
            "age_grp": age_grp,
            "page": page,
            "items_pp": items_pp
        }
        st.experimental_rerun()

    if 'q_params' in st.session_state:
        perform_search(st.session_state.q_params)

if __name__ == "__main__":
    search_section()
