import streamlit as st
from home_backend import handle_file_upload, confirm_and_upload_data
import uuid
from helper_functions import style_markdown2, select_subregion, select_sub_subregion, select_sub_sub_subregion

def initialize_home_session_state():
    if 'confirm_data' not in st.session_state:
        st.session_state.confirm_data = None

def main():
    initialize_home_session_state()
    style_markdown2()
    st.markdown('<div class="upload-title">Orvosi Röntgenkép Adatbázis</div>', unsafe_allow_html=True)

    patient_id = str(uuid.uuid4())
    st.text_input("Beteg azonosító", patient_id, disabled=True)

    st.markdown('<div class="file-upload-instruction">Kérem húzzon az alábbi ablakra vagy válasszon ki a fájlkezelőn keresztül egy röntgenképet (Max 15 MB)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Fájl kiválasztása", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

    if uploaded_file is not None:
        uploaded_file = handle_file_upload(uploaded_file)

    if uploaded_file:
        col1, col2 = st.columns(2)
        with col1:
            type = st.radio("Válassza ki a típusát", ["Normál", "Törött", "Egyéb"], key="type")
            if type == "Egyéb": 
                type = st.selectbox("Specifikálás (Egyéb)", ["Luxatio", "Subluxatio", "Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Cysta",  "Malignus Tumor", "Benignus Tumor", "Metastasis", "Rheumatoid Arthritis","Genetikai/Veleszületett", "Egyéb"])
                if type in ["Malignus Tumor", "Benignus Tumor", "Genetikai/Veleszületett", "Egyéb"]:
                    type = st.text_input("Adja meg a specifikus típust (Egyéb)")

        with col2:
            view = st.radio("Válassza ki a nézetet", ["AP", "Lateral", "Egyéb"], key="view")
            if view == "Egyéb":
                view = st.selectbox("Specifikálás (Egyéb Nézet)", ["Ferde", "PA", "Speciális"])
                if view == "Speciális":
                    view = st.text_input("Adja meg a specifikus nézetet (Speciális)")

        # Main and sub region in one row
        col3, col4 = st.columns(2)
        with col3:
            main_region = st.selectbox("Fő régió", ["Felső végtag", "Alsó végtag", "Gerinc", "Koponya", "Mellkas", "Has"])
        with col4:
            sub_region = select_subregion(main_region)

        # Sub-subregion and sub-sub-subregion in one row
        col5, col6 = st.columns(2)
        with col5:
            sub_sub_region = select_sub_subregion(sub_region)
        with col6:
            sub_sub_sub_region = select_sub_sub_subregion(sub_sub_region)

        if type != "Normál":
            complications = st.multiselect("Komplikációk (többet is választhat)", ["Nyílt", "Darabos", "Avulsio", "Luxatio", "Subluxatio", "Idegsérülés", "Nagyobb Érsérülés", "Szalagszakadás", "Meniscus Sérülés", "Epiphysis Sérülés", "Fertőzés"])
            associated_conditions = st.multiselect("Társuló Kórállapotok (többet is választhat)", ["Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Cysta", "Rheumatoid Arthritis",  "Metastasis", "Malignus Tumor", "Benignus Tumor", "Genetikai"])

        age = st.select_slider("Életkor (opcionális)", options=["NA"] + list(range(0, 121)), value="NA")
        age_group = ""
        if age != "NA":
            age = int(age)
            age_group = "Gyermek" if age <= 18 else "Felnőtt"

        comment = st.text_area("Megjegyzés (opcionális)", key="comment", value="")

        if st.button("Feltöltés"):
            upload_data = {
                "patient_id": patient_id,
                "type": type,
                "view": view,
                "main_region": main_region,
                "sub_region": sub_region if type != "Normál" else "",
                "sub_sub_region": sub_sub_region if sub_sub_region != "NA" else "",
                "sub_sub_sub_region": sub_sub_sub_region if sub_sub_sub_region != "NA" else "",
                "age": age,
                "age_group": age_group,
                "comment": comment,
                "file": uploaded_file,
                "complications": complications if type != "Normál" else [],
                "associated_conditions": associated_conditions if type != "Normál" else []
            }
            st.session_state.confirm_data = upload_data
            st.experimental_rerun()

        if st.session_state.confirm_data:
            confirm_and_upload_data(st.session_state.confirm_data)

    if st.experimental_get_query_params().get("scroll_to") == ["confirmation"]:
        st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
