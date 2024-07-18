import streamlit as st
from google.cloud import firestore
from firebase_helpers import db, create_zip
import uuid
from google.api_core.exceptions import GoogleAPICallError
from search_backend import perform_search

def search_section():
    st.markdown(
        """
        <style>
        .search-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            border: 2px solid black;
            padding: 10px;
            margin-bottom: 20px;
        }
        .result-image {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 5px;
            margin-bottom: 10px;
        }
        .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 10px 0;
        }
        .button-container button {
            font-size: 18px;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 5px;
            background-color: #4CAF50; /* Green */
            color: white;
            border: none;
            cursor: pointer;
        }
        .button-container button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="search-title">Képek keresése</div>', unsafe_allow_html=True)

    predefined_types = ["", "Törött", "Normál", "Luxatio", "Subluxatio", "Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Malignus Tumor", "Benignus Tumor", "Metastasis", "Rheumatoid Arthritis", "Cysta", "Genetikai/Veleszületett", "Egyéb"]
    predefined_views = ["", "AP", "Lateral", "Ferde", "PA", "Speciális"]

    # Type and view in one row
    col1, col2 = st.columns(2)
    with col1:
        search_type = st.selectbox("Típus keresése", predefined_types)
    with col2:
        search_view = st.selectbox("Nézet keresése", predefined_views)

    # Main and sub region in one row
    col3, col4 = st.columns(2)
    with col3:
        search_main_region = st.selectbox("Fő régió keresése", ["", "Felső végtag", "Alsó végtag", "Gerinc", "Koponya"])
    with col4:
        if search_main_region == "Felső végtag":
            search_sub_region = st.selectbox("Alrégió keresése", ["", "Clavicula", "Scapula", "Váll", "Humerus", "Könyök", "Radius", "Ulna", "Csukló", "Kéz"])
        elif search_main_region == "Alsó végtag":
            search_sub_region = st.selectbox("Alrégió keresése", ["", "Csípő", "Comb", "Térd", "Tibia", "Fibula", "Boka", "Láb"])
        elif search_main_region == "Gerinc":
            search_sub_region = st.selectbox("Alrégió keresése", ["", "Nyaki", "Háti", "Ágyéki", "Kereszt- és farokcsonti"])
        elif search_main_region == "Koponya":
            search_sub_region = st.selectbox("Alrégió keresése", ["", "Arckoponya", "Agykoponya", "Állkapocs"])
        else:
            search_sub_region = ""

    search_complications = st.multiselect("Komplikációk keresése", ["Nyílt", "Darabos", "Avulsio", "Luxatio", "Subluxatio", "Idegsérülés", "Nagyobb Érsérülés", "Szalagszakadás", "Meniscus Sérülés", "Epiphysis Sérülés", "Fertőzés"])
    search_associated_conditions = st.multiselect("Társuló Kórállapotok keresése", ["Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Rheumatoid Arthritis", "Cysta", "Metastasis", "Malignus Tumor", "Benignus Tumor", "Genetikai"])

    # Age filter with checkbox
    age_filter_active = st.checkbox("Életkor keresése (intervallum)")
    if age_filter_active:
        search_age = st.slider("Életkor keresése (intervallum)", min_value=0, max_value=120, value=(0, 18), step=1, format="%d")
    else:
        search_age = None

    search_age_group = st.selectbox("Életkori csoport keresése", ["", "Gyermek", "Felnőtt"])

    # Page and items per page in one row
    col5, col6 = st.columns(2)
    with col5:
        page = st.number_input("Oldal", min_value=1, step=1, value=1)
    with col6:
        items_per_page = st.selectbox("Találatok száma oldalanként", options=[10, 25, 50, 100], index=0)

    # Button for search
    search_button_clicked = st.button("Keresés", key="search_button")

    if search_button_clicked:
        page = 1  # Reset to the first page on new search
        st.session_state.search_button_clicked = True
        st.session_state.query_params = {
            "search_button_clicked": True,
            "type": search_type,
            "view": search_view,
            "main_region": search_main_region,
            "sub_region": search_sub_region,
            "complications": search_complications,
            "associated_conditions": search_associated_conditions,
            "age_filter_active": age_filter_active,
            "age": str(search_age) if search_age else "",
            "age_group": search_age_group,
            "page": page,
            "items_per_page": items_per_page
        }
        st.experimental_rerun()

    if 'search_button_clicked' in st.session_state:
        perform_search(st.session_state.query_params)

if __name__ == "__main__":
    search_section()
