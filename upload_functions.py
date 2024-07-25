import uuid
import streamlit as st
from helper_functions import (
    select_main_type, select_view, select_main_region,
    select_subregion, select_sub_subregion, select_sub_sub_subregion,
    select_sub_sub_sub_subregion, select_finger, select_complications,
    select_associated_conditions, ao_classification, neer_classification, gartland_classification
)

def initialize_home_session_state():
    if 'confirm_data' not in st.session_state:
        st.session_state.confirm_data = None
    if 'regions' not in st.session_state:
        st.session_state.regions = [{'main_region': None, 'side': None, 'sub_region': None, 'sub_sub_region': None, 'sub_sub_sub_region': None, 'sub_sub_sub_sub_region': None, 'finger': None, 'editable': True}]
    if 'patient_id' not in st.session_state:
        st.session_state.patient_id = str(uuid.uuid4())
    if 'multi_region' not in st.session_state:
        st.session_state.multi_region = False
    if 'new_region_blocked' not in st.session_state:
        st.session_state.new_region_blocked = False
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'allow_multiple_uploads' not in st.session_state:
        st.session_state.allow_multiple_uploads = False
    if 'file_uploader_key' not in st.session_state:
        st.session_state.file_uploader_key = str(uuid.uuid4())
        
def display_images():
    if not st.session_state.allow_multiple_uploads:
        if st.session_state.uploaded_files:
            st.image(st.session_state.uploaded_files[-1], caption=f"Feltöltött kép: {st.session_state.uploaded_files[-1].name}", use_column_width=True)
    else:
        cols = st.columns(2)
        for idx, file in enumerate(st.session_state.uploaded_files):
            with cols[idx % 2]:
                st.image(file, caption=f"ID: {uuid.uuid4()} - {file.name}", use_column_width=True)

def reset_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_home_session_state()

def display_region(region, idx):
    col3, col4, col5 = st.columns([1, 1, 1])
    with col3:
        if region['editable']:
            region['main_region'] = select_main_region()
        else:
            st.write(f"Fő régió: {region['main_region']}")
    if region['main_region']:
        if region['main_region'] in ["Felső végtag", "Alsó végtag"]:
            with col4:
                if region['editable']:
                    region['side'] = st.selectbox("Oldal", ["Bal", "Jobb"], index=["Bal", "Jobb"].index(region['side']) if region.get('side') else 0)
                else:
                    st.write(f"Oldal: {region['side']}")
        if region['editable']:
            with col5:
                region['sub_region'] = select_subregion(region['main_region'])
        else:
            st.write(f"Régió: {region['sub_region']}")
    if region['sub_region']:
        col6, col7, col8, col9 = st.columns([1, 1, 1, 1])
        with col6:
            if region['editable']:
                region['sub_sub_region'] = select_sub_subregion(region['sub_region'])
            else:
                st.write(f"Alrégió: {region['sub_sub_region']}")
        if region['sub_sub_region']:
            with col7:
                if region['editable']:
                    region['sub_sub_sub_region'] = select_sub_sub_subregion(region['sub_sub_region'])
                else:
                    st.write(f"Részletes régió: {region['sub_sub_sub_region']}")
        if region['sub_sub_sub_region']:
            with col8:
                if region['editable']:
                    region['sub_sub_sub_sub_region'] = select_sub_sub_sub_subregion(region['sub_sub_sub_region'])
                else:
                    st.write(f"Legrészletesebb régió: {region['sub_sub_sub_sub_region']}")
            with col9:
                if region['editable']:
                    if region['sub_sub_sub_region'] in ["Metacarpus", "Phalanx", "Metatarsus", "Lábujjak", "Pollex", "Hallux"]:
                        region['finger'], _ = select_finger(region['sub_sub_sub_region'])
                    else:
                        region['finger'] = None
                else:
                    st.write(f"Ujj: {region['finger']}")
    return region
