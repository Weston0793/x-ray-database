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

    # Initialize session state if not exists
    if 'q_params' not in st.session_state:
        st.session_state.q_params = {
            "type": "",
            "view": "",
            "main_reg": "",
            "sub_reg": "",
            "sub_sub_reg": "",
            "sub_sub_sub_reg": "",
            "comp": [],
            "cond": [],
            "age_flt": False,
            "age_rng": (0, 18),
            "age_grp": "",
            "page": 1,
            "items_pp": 10
        }

    # Type and view in one row
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.q_params["type"] = st.selectbox("Típus", types, index=types.index(st.session_state.q_params["type"]))
    with col2:
        st.session_state.q_params["view"] = st.selectbox("Nézet", views, index=views.index(st.session_state.q_params["view"]))

    # Main and sub region in one row
    col3, col4 = st.columns(2)
    with col3:
        st.session_state.q_params["main_reg"] = st.selectbox("Fő régió", regions, index=regions.index(st.session_state.q_params["main_reg"]))
    with col4:
        st.session_state.q_params["sub_reg"] = select_subregion(st.session_state.q_params["main_reg"])

    # Sub-subregion and sub-sub-subregion in one row
    col5, col6 = st.columns(2)
    with col5:
        st.session_state.q_params["sub_sub_reg"] = select_sub_subregion(st.session_state.q_params["sub_reg"])
    with col6:
        st.session_state.q_params["sub_sub_sub_reg"] = select_sub_sub_subregion(st.session_state.q_params["sub_sub_reg"])

    # Multiselects for complications and associated conditions
    st.session_state.q_params["comp"] = st.multiselect("Komplikációk", ["Nyílt", "Darabos", "Avulsio", "Luxatio", "Subluxatio", "Idegsérülés", "Nagyobb Érsérülés", "Szalagszakadás", "Meniscus Sérülés", "Epiphysis Sérülés", "Fertőzés"], default=st.session_state.q_params["comp"])
    st.session_state.q_params["cond"] = st.multiselect("Kórállapotok", ["Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Rheumatoid Arthritis", "Cysta", "Metastasis", "Malignus Tumor", "Benignus Tumor", "Genetikai"], default=st.session_state.q_params["cond"])

    # Age filter with checkbox
    st.session_state.q_params["age_flt"] = st.checkbox("Életkor (intervallum)", value=st.session_state.q_params["age_flt"])
    if st.session_state.q_params["age_flt"]:
        st.session_state.q_params["age_rng"] = st.slider("Életkor (intervallum)", min_value=0, max_value=120, value=st.session_state.q_params["age_rng"], step=1, format="%d")

    st.session_state.q_params["age_grp"] = st.selectbox("Életkori csoport", ["", "Gyermek", "Felnőtt"], index=["", "Gyermek", "Felnőtt"].index(st.session_state.q_params["age_grp"]))

    # Page and items per page in one row
    col7, col8 = st.columns(2)
    with col7:
        st.session_state.q_params["page"] = st.number_input("Oldal", min_value=1, step=1, value=st.session_state.q_params["page"])
    with col8:
        st.session_state.q_params["items_pp"] = st.selectbox("Találatok/Oldal", options=[10, 25, 50, 100], index=[10, 25, 50, 100].index(st.session_state.q_params["items_pp"]))

    # Button for search
    if st.button("Keresés", key="search_btn"):
        st.session_state.q_params["page"] = 1  # Reset to the first page on new search
        st.experimental_rerun()

    if 'q_params' in st.session_state:
        perform_search(st.session_state.q_params)

if __name__ == "__main__":
    search_section()
