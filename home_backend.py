import streamlit as st
from firebase_helpers import save_image

def handle_file_upload(uploaded_file):
    if uploaded_file.size > 15 * 1024 * 1024:
        st.error("A kép mérete nem lehet nagyobb, mint 15 MB.")
        return None
    else:
        st.image(uploaded_file, caption="Feltöltött kép", use_column_width=True)
        return uploaded_file

def confirm_and_upload_data(upload_data):
    if upload_data['age'] == "NA":
        age_group = st.radio("Kérem válassza ki az életkori csoportot", ["Gyermek", "Felnőtt"])
        upload_data['age_group'] = age_group

    st.markdown('<div class="confirmation-box">', unsafe_allow_html=True)
    st.markdown('<div class="confirmation-title">Kérlek, a feltöltéshez erősítsd meg a következő adatokat:</div>', unsafe_allow_html=True)
    st.markdown(f'**Beteg azonosító:** {upload_data["patient_id"]}')
    st.markdown(f'**Típus:** {upload_data["type"]}')
    st.markdown(f'**Nézet:** {upload_data["view"]}')
    st.markdown(f'**Fő régió:** {upload_data["main_region"]}')
    st.markdown(f'**Alrégió:** {upload_data["sub_region"]}')
    st.markdown(f'**Életkor: (opcionális)** {upload_data["age"]}')
    st.markdown(f'**Életkori Csoport:** {upload_data["age_group"]}')
    st.markdown(f'**Megjegyzés: (opcionális)** {upload_data["comment"]}')
    if upload_data["complications"]:
        st.markdown(f'**Komplikációk: (többet is választhat)** {", ".join(upload_data["complications"])}')
    if upload_data["associated_conditions"]:
        st.markdown(f'**Társuló Kórállapotok: (többet is választhat)** {", ".join(upload_data["associated_conditions"])}')

    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("Megerősít és Feltölt", key="confirm_upload"):
        try:
            save_image(**upload_data)
            st.success("Kép sikeresen feltöltve!")
            st.session_state["confirm_data"] = None
            st.experimental_set_query_params(scroll_to="confirmation")
        except Exception as e:
            st.error(f"Hiba a kép mentésekor: {e}")
            st.session_state["confirm_data"] = None
    st.markdown('</div>', unsafe_allow_html=True)
