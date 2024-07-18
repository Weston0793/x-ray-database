import streamlit as st
from firebase_helpers import save_image
from home_backend import handle_file_upload, confirm_and_upload_data
import uuid

def main():
    st.markdown(
        """
        <style>
        .upload-title {
            font-size: 24px;
            font-weight: bold;
            color: black;
            margin-bottom: 20px;
            text-align: center;
            border: 2px solid black;
            padding: 10px;
        }
        .center-button {
            display: flex;
            justify-content: center;
        }
        .upload-button, .confirm-button {
            font-size: 24px;
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            border: none;
            cursor: pointer;
            border: 2px solid black;
            margin: 10px;
        }
        .upload-button:hover, .confirm-button:hover {
            background-color: #45a049;
        }
        .confirmation-box {
            padding: 20px;
            margin-top: 20px;
            text-align: center;
        }
        .confirmation-title, .confirmation-text {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .file-upload-instruction {
            font-size: 18px;
            font-weight: bold;
            color: black;
            margin-bottom: 20px;
            text-align: center;
            border: 2px solid black;
            padding: 10px;
            background-color: #f9f9f9;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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
                type = st.selectbox("Specifikálás (Egyéb)", ["Luxatio", "Subluxatio", "Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Malignus Tumor", "Benignus Tumor", "Metastasis", "Rheumatoid Arthritis", "Cysta", "Genetikai/Veleszületett", "Egyéb"])
                if type in ["Malignus Tumor", "Benignus Tumor", "Genetikai/Veleszületett", "Egyéb"]:
                    type = st.text_input("Adja meg a specifikus típust (Egyéb)")
        
        with col2:
            view = st.radio("Válassza ki a nézetet", ["AP", "Lateral", "Egyéb"], key="view")
            if view == "Egyéb":
                view = st.selectbox("Specifikálás (Egyéb Nézet)", ["Ferde", "PA", "Speciális"])
                if view == "Speciális":
                    view = st.text_input("Adja meg a specifikus nézetet (Speciális)")

        if type != "Normál":
            complications = st.multiselect("Komplikációk (többet is választhat)", ["Nyílt", "Darabos", "Avulsio", "Luxatio", "Subluxatio", "Idegsérülés", "Nagyobb Érsérülés", "Szalagszakadás", "Meniscus Sérülés", "Epiphysis Sérülés", "Fertőzés"])
            associated_conditions = st.multiselect("Társuló Kórállapotok (többet is választhat)", ["Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Rheumatoid Arthritis", "Cysta", "Metastasis", "Malignus Tumor", "Benignus Tumor", "Genetikai"])

        col3, col4 = st.columns(2)
        with col3:
            main_region = st.selectbox("Fő régió", ["Felső végtag", "Alsó végtag", "Gerinc", "Koponya"])

        with col4:
            if main_region == "Felső végtag":
                sub_region = st.selectbox("Alrégió", ["Clavicula", "Scapula", "Váll", "Humerus", "Könyök", "Radius", "Ulna", "Csukló", "Kéz"])
            elif main_region == "Alsó végtag":
                sub_region = st.selectbox("Alrégió", ["Csípő", "Comb", "Térd", "Tibia", "Fibula", "Boka", "Láb"])
            elif main_region == "Gerinc":
                sub_region = st.selectbox("Alrégió", ["Nyaki", "Háti", "Ágyéki", "Kereszt- és farokcsonti"])
            elif main_region == "Koponya":
                sub_region = st.selectbox("Alrégió", ["Arckoponya", "Agykoponya", "Állkapocs"])
            else:
                sub_region = ""

        age = st.select_slider("Életkor (opcionális)", options=["NA"] + list(range(0, 121)), value="NA")
        age_group = ""
        if age != "NA":
            age = int(age)
            age_group = "Gyermek" if age <= 18 else "Felnőtt"

        comment = st.text_area("Megjegyzés (opcionális)", key="comment", value="")

        if "confirm_data" not in st.session_state:
            st.session_state["confirm_data"] = None

        if st.button("Feltöltés"):
            if uploaded_file and type and view and main_region and sub_region:
                upload_data = {
                    "patient_id": patient_id,
                    "type": type,
                    "view": view,
                    "main_region": main_region,
                    "sub_region": sub_region,
                    "age": age,
                    "age_group": age_group,
                    "comment": comment,
                    "file": uploaded_file,
                    "complications": complications if type != "Normál" else [],
                    "associated_conditions": associated_conditions if type != "Normál" else []
                }
                st.session_state["confirm_data"] = upload_data
                st.rerun()

        if st.session_state["confirm_data"]:
            confirm_and_upload_data(st.session_state["confirm_data"])

    if st.experimental_get_query_params().get("scroll_to") == ["confirmation"]:
        st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
