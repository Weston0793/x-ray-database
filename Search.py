import streamlit as st
from google.cloud import firestore
from firebase_helpers import db, create_zip
import uuid
from google.api_core.exceptions import GoogleAPICallError
from search_backend import perform_search
from helper_functions import (
    select_main_type, select_view, select_gender, select_main_region, select_subregion, 
    select_sub_subregion, select_sub_sub_subregion, select_sub_sub_sub_subregion, 
    select_complications, select_associated_conditions,
    ao_classification, neer_classification, gartland_classification
)
from Styles import search_markdown

def initialize_session_state():
    if 'search_button_clicked' not in st.session_state:
        st.session_state.search_button_clicked = False
    if 'query_params' not in st.session_state:
        st.session_state.query_params = {
            "search_button_clicked": False,
            "main_type": "",
            "sub_type": "",
            "sub_sub_type": "",
            "view": "",
            "sub_view": "",
            "sub_sub_view": "",
            "gender": "",
            "main_region": "",
            "sub_region": "",
            "sub_sub_region": "",
            "sub_sub_sub_region": "",
            "sub_sub_sub_sub_region": "",
            "complications": [],
            "associated_conditions": [],
            "age_filter_active": False,
            "age": "",
            "age_group": "",
            "page": 1,
            "items_per_page": 10,
            "classifications": {}
        }

def search_section():
    initialize_session_state()
    search_markdown()
    st.markdown('<div class="search-title">Képek keresése</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        main_type, sub_type, sub_sub_type = select_main_type()
    with col2:
        view, sub_view, sub_sub_view = select_view()
    with col3:
        gender = select_gender()

    col4, col5 = st.columns(2)
    with col4:
        main_region = select_main_region()
    with col5:
        sub_region = select_subregion(main_region)

    col6, col7, col8 = st.columns(3)
    with col6:
        sub_sub_region = select_sub_subregion(sub_region)
    with col7:
        sub_sub_sub_region = select_sub_sub_subregion(sub_sub_region)
    with col8:
        sub_sub_sub_sub_region = select_sub_sub_sub_subregion(sub_sub_sub_region)

    classification_types = st.multiselect("Válassza ki az osztályozás típusát (többet is választhat)", ["AO", "Gartland", "Neer"])
    
    classifications = {}
    if "AO" in classification_types:
        ao_name, ao_severity, ao_subseverity = ao_classification(sub_sub_region)
        if ao_name and ao_severity and ao_subseverity:
            classifications["AO"] = {"name": ao_name, "severity": ao_severity, "subseverity": ao_subseverity}
    
    if "Gartland" in classification_types:
        gartland_name, gartland_severity, gartland_description = gartland_classification()
        if gartland_name and gartland_severity:
            classifications["Gartland"] = {"name": gartland_name, "severity": gartland_severity, "description": gartland_description}
    
    if "Neer" in classification_types:
        neer_name, neer_severity, neer_description = neer_classification(sub_sub_region)
        if neer_name and neer_severity:
            classifications["Neer"] = {"name": neer_name, "severity": neer_severity, "description": neer_description}

    complications = select_complications()
    associated_conditions = select_associated_conditions()

    age_filter_active = st.checkbox("Életkor keresése (intervallum)", value=st.session_state.query_params["age_filter_active"])
    age_group = st.selectbox("Életkori csoport keresése", ["", "Gyermek", "Felnőtt"], index=["", "Gyermek", "Felnőtt"].index(st.session_state.query_params["age_group"]))

    if age_filter_active:
        if age_group == "Gyermek":
            age = st.slider("Életkor keresése (intervallum)", min_value=0, max_value=18, value=(0, 18), step=1, format="%d")
        elif age_group == "Felnőtt":
            age = st.slider("Életkor keresése (intervallum)", min_value=19, max_value=120, value=(19, 120), step=1, format="%d")
        else:
            try:
                age_value = eval(st.session_state.query_params["age"]) if st.session_state.query_params["age"] else (0, 120)
            except ValueError:
                age_value = (0, 120)
            age = st.slider("Életkor keresése (intervallum)", min_value=0, max_value=120, value=age_value, step=1, format="%d")
    else:
        age = None

    col10, col11 = st.columns(2)
    with col10:
        page = st.number_input("Oldal", min_value=1, step=1, value=st.session_state.query_params["page"])
    with col11:
        items_per_page = st.selectbox("Találatok száma oldalanként", options=[10, 25, 50, 100], index=[10, 25, 50, 100].index(st.session_state.query_params["items_per_page"]))

    search_button_clicked = st.button("Keresés", key="search_button")

    if search_button_clicked:
        page = 1
        st.session_state.search_button_clicked = True
        st.session_state.query_params = {
            "search_button_clicked": True,
            "main_type": main_type,
            "sub_type": sub_type,
            "sub_sub_type": sub_sub_type,
            "view": view,
            "sub_view": sub_view,
            "sub_sub_view": sub_sub_view,
            "gender": gender,
            "main_region": main_region,
            "sub_region": sub_region,
            "sub_sub_region": sub_sub_region,
            "sub_sub_sub_region": sub_sub_sub_region,
            "sub_sub_sub_sub_region": sub_sub_sub_sub_region,
            "complications": complications,
            "associated_conditions": associated_conditions,
            "age_filter_active": age_filter_active,
            "age": str(age) if age else "",
            "age_group": age_group,
            "page": page,
            "items_per_page": items_per_page,
            "classifications": classifications
        }
        st.experimental_rerun()

    if st.session_state.search_button_clicked:
        perform_search(st.session_state.query_params)

if __name__ == "__main__":
    search_section()
