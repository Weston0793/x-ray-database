import streamlit as st
from firebase_helpers import save_image
from Styles import upload_markdown
import uuid
from helper_functions import (
    select_main_type, select_view, select_main_region, select_gender,
    select_subregion, select_sub_subregion, select_sub_sub_subregion,
    select_sub_sub_sub_subregion, select_finger, select_complications,
    select_associated_conditions, ao_classification, neer_classification, gartland_classification
)

# Function to handle file uploads
def handle_file_upload(uploaded_file):
    if uploaded_file.size > 15 * 1024 * 1024:
        st.error("A kép mérete nem lehet nagyobb, mint 15 MB.")
        return None
    else:
        return uploaded_file

def confirm_and_upload_data(upload_data):
    if upload_data['age'] == "NA":
        age_group = st.radio("Kérem válassza ki az életkori csoportot", ["Gyermek", "Felnőtt"])
        upload_data['age_group'] = age_group

    st.markdown('---')
    st.markdown('<div class="confirmation-title">Kérlek, a feltöltéshez erősítsd meg a következő adatokat:</div>', unsafe_allow_html=True)

    cols = st.columns(2)

    with cols[0]:
        if upload_data["patient_id"]:
            st.markdown(f'**<span class="highlight">Beteg azonosító:</span>** {upload_data["patient_id"]}', unsafe_allow_html=True)
        if upload_data["main_type"]:
            st.markdown(f'**<span class="highlight">Típus:</span>** {upload_data["main_type"]}', unsafe_allow_html=True)
        if upload_data["sub_type"]:
            st.markdown(f'**<span class="highlight">Specifikus típus:</span>** {upload_data["sub_type"]}', unsafe_allow_html=True)
        if upload_data["sub_sub_type"]:
            st.markdown(f'**<span class="highlight">Legspecifikusabb típus:</span>** {upload_data["sub_sub_type"]}', unsafe_allow_html=True)
        if upload_data["gender"]:
            st.markdown(f'**<span class="highlight">Nem:</span>** {upload_data["gender"]}', unsafe_allow_html=True)
        if upload_data["age"] != "NA":
            st.markdown(f'**<span class="highlight">Életkor:</span>** {upload_data["age"]}', unsafe_allow_html=True)

    with cols[1]:
        if upload_data["view"]:
            st.markdown(f'**<span class="highlight">Nézet:</span>** {upload_data["view"]}', unsafe_allow_html=True)
        if upload_data["sub_view"]:
            st.markdown(f'**<span class="highlight">Specifikus nézet:</span>** {upload_data["sub_view"]}', unsafe_allow_html=True)
        if upload_data["sub_sub_view"]:
            st.markdown(f'**<span class="highlight">Legspecifikusabb nézet:</span>** {upload_data["sub_sub_view"]}', unsafe_allow_html=True)
        if upload_data["age_group"]:
            st.markdown(f'**<span class="highlight">Életkori Csoport:</span>** {upload_data["age_group"]}', unsafe_allow_html=True)
        if upload_data["comment"]:
            st.markdown(f'**<span class="highlight">Megjegyzés:</span>** {upload_data["comment"]}', unsafe_allow_html=True)
        if upload_data["complications"]:
            st.markdown(f'**<span class="highlight">Komplikációk:</span>** {", ".join(upload_data["complications"])}', unsafe_allow_html=True)
        if upload_data["associated_conditions"]:
            st.markdown(f'**<span class="highlight">Társuló Kórállapotok:</span>** {", ".join(upload_data["associated_conditions"])}', unsafe_allow_html=True)

    st.markdown('### Kiválasztott régiók', unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, region in enumerate(upload_data["regions"]):
        col = cols[idx % 2]
        with col:
            st.markdown(f"**<span class='highlight'>Régió {idx + 1}:</span>**", unsafe_allow_html=True)
            if region['main_region']:
                st.markdown(f"**<span class='highlight'>Fő régió:</span>** {region['main_region']}", unsafe_allow_html=True)
            if region['side']:
                st.markdown(f"**<span class='highlight'>Oldal:</span>** {region['side']}", unsafe_allow_html=True)
            if region['sub_region']:
                st.markdown(f"**<span class='highlight'>Alrégió:</span>** {region['sub_region']}", unsafe_allow_html=True)
            if region['sub_sub_region']:
                st.markdown(f"**<span class='highlight'>Részletes régió:</span>** {region['sub_sub_region']}", unsafe_allow_html=True)
            if region['sub_sub_sub_region']:
                st.markdown(f"**<span class='highlight'>Legpontosabb régió:</span>** {region['sub_sub_sub_region']}", unsafe_allow_html=True)
            if region['finger']:
                st.markdown(f"**<span class='highlight'>Ujj:</span>** {region['finger']}", unsafe_allow_html=True)
            if region['sub_sub_sub_sub_region']:
                st.markdown(f"**<span class='highlight'>Legrészletesebb régió:</span>** {region['sub_sub_sub_sub_region']}", unsafe_allow_html=True)

            if region.get("classification"):
                for classification_name, details in region["classification"].items():
                    if "name" in details and "severity" in details:
                        st.markdown(f"**<span class='highlight'>Osztályozás:</span>** {details['name']}", unsafe_allow_html=True)
                        st.markdown(f"**<span class='highlight'>Súlyosság:</span>** {details['severity']}", unsafe_allow_html=True)
                        if "subseverity" in details:
                            st.markdown(f"**<span class='highlight'>Alsúlyosság:</span>** {details['subseverity']}", unsafe_allow_html=True)

    st.markdown('---')
    
    with st.container():
        
        # Add a button for confirming and uploading
        if st.button("Megerősít és Feltölt", key="confirm_upload", help="Kattintson a feltöltés megerősítéséhez"):
            if upload_data:  # Check if upload_data exists and is not empty
                try:
                    save_image(
                        patient_id=upload_data["patient_id"],
                        files=upload_data["files"],
                        main_type=upload_data["main_type"],
                        sub_type=upload_data["sub_type"],
                        sub_sub_type=upload_data["sub_sub_type"],
                        view=upload_data["view"],
                        sub_view=upload_data["sub_view"],
                        sub_sub_view=upload_data["sub_sub_view"],
                        gender=upload_data["gender"],  # Gender added here
                        age=upload_data["age"],
                        age_group=upload_data["age_group"],
                        comment=upload_data["comment"],
                        complications=upload_data["complications"],
                        associated_conditions=upload_data["associated_conditions"],
                        regions=upload_data["regions"]
                    )
                    st.success("Kép sikeresen feltöltve!")
                    st.session_state["confirm_data"] = None
                    st.experimental_set_query_params(scroll_to="confirmation")
                except Exception as e:
                    st.error(f"Hiba a kép mentésekor: {e}")
                    st.session_state["confirm_data"] = None
            else:
                st.error("Nincs feltöltendő adat!")
