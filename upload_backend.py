import streamlit as st
from firebase_helpers import save_image

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

    st.markdown('<div class="confirmation-box">', unsafe_allow_html=True)
    st.markdown('<div class="confirmation-title">Kérlek, a feltöltéshez erősítsd meg a következő adatokat:</div>', unsafe_allow_html=True)
    st.markdown(f'**Beteg azonosító:** {upload_data["patient_id"]}', unsafe_allow_html=True)
    st.markdown(f'**Típus:** {upload_data["main_type"]}', unsafe_allow_html=True)
    if upload_data["sub_type"]:
        st.markdown(f'**Specifikus típus:** {upload_data["sub_type"]}', unsafe_allow_html=True)
    if upload_data["sub_sub_type"]:
        st.markdown(f'**Legspecifikusabb típus:** {upload_data["sub_sub_type"]}', unsafe_allow_html=True)
    st.markdown(f'**Nézet:** {upload_data["view"]}', unsafe_allow_html=True)
    if upload_data["sub_view"]:
        st.markdown(f'**Specifikus nézet:** {upload_data["sub_view"]}', unsafe_allow_html=True)
    if upload_data["sub_sub_view"]:
        st.markdown(f'**Legspecifikusabb nézet:** {upload_data["sub_sub_view"]}', unsafe_allow_html=True)
    st.markdown(f'**Életkor: (opcionális)** {upload_data["age"]}', unsafe_allow_html=True)
    st.markdown(f'**Életkori Csoport:** {upload_data["age_group"]}', unsafe_allow_html=True)
    st.markdown(f'**Megjegyzés: (opcionális)** {upload_data["comment"]}', unsafe_allow_html=True)
    if upload_data["complications"]:
        st.markdown(f'**Komplikációk: (többet is választhat)** {", ".join(upload_data["complications"])}', unsafe_allow_html=True)
    if upload_data["associated_conditions"]:
        st.markdown(f'**Társuló Kórállapotok: (többet is választhat)** {", ".join(upload_data["associated_conditions"])}', unsafe_allow_html=True)

    st.markdown("### Kiválasztott régiók", unsafe_allow_html=True)
    for idx, region in enumerate(upload_data["regions"]):
        st.markdown(f"**Régió {idx + 1}:**", unsafe_allow_html=True)
        st.markdown(f"**Fő régió:** {region['main_region']}", unsafe_allow_html=True)
        if region['side']:
            st.markdown(f"**Oldal:** {region['side']}", unsafe_allow_html=True)
        st.markdown(f"**Alrégió:** {region['sub_region']}", unsafe_allow_html=True)
        if region['sub_sub_region']:
            st.markdown(f"**Részletes régió:** {region['sub_sub_region']}", unsafe_allow_html=True)
        if region['sub_sub_sub_region']:
            st.markdown(f"**Legpontosabb régió:** {region['sub_sub_sub_region']}", unsafe_allow_html=True)
        if region['finger']:
            st.markdown(f"**Ujj:** {region['finger']}", unsafe_allow_html=True)
        if region['sub_sub_sub_sub_region']:
            st.markdown(f"**Legrészletesebb régió:** {region['sub_sub_sub_sub_region']}", unsafe_allow_html=True)

        if region.get("classification"):
            for classification_name, details in region["classification"].items():
                if "name" in details and "severity" in details:
                    st.markdown(f"**Osztályozás:** {details['name']}", unsafe_allow_html=True)
                    st.markdown(f"**Súlyosság:** {details['severity']}", unsafe_allow_html=True)
                    if "subseverity" in details:
                        st.markdown(f"**Alsúlyosság:** {details['subseverity']}", unsafe_allow_html=True)

    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("Megerősít és Feltölt", key="confirm_upload"):
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
    st.markdown('</div>', unsafe_allow_html=True)
