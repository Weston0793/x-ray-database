import streamlit as st
from upload_backend import handle_file_upload, confirm_and_upload_data
import uuid
from helper_functions import (
    select_main_type, select_view, select_gender, select_main_region, 
    select_subregion, select_sub_subregion, select_sub_sub_subregion, 
    select_sub_sub_sub_subregion, select_finger, select_complications, 
    select_associated_conditions, ao_classification, neer_classification, gartland_classification
)
from Styles import upload_markdown
from upload_functions import (
    initialize_home_session_state, reset_session_state,
    display_region, display_images
)

def main():
    if 'patient_id' not in st.session_state:
        initialize_home_session_state()
    
    upload_markdown()
    st.markdown('<div class="upload-title">Röntgenkép feltöltése</div>', unsafe_allow_html=True)

    st.text_input("Beteg azonosító", st.session_state.patient_id, disabled=True)

    st.markdown('<div class="file-upload-instruction">Kérem húzzon az alábbi ablakra egy anonimizált röntgenképet vagy válassza ki a fájlkezelőn keresztül!  (Max. méret/file: 15 MB)</div>', unsafe_allow_html=True)
    st.session_state.allow_multiple_uploads = st.checkbox("Több kép feltöltése", value=st.session_state.get('allow_multiple_uploads', False))

    if st.session_state.allow_multiple_uploads:
        st.warning("Ugyanazokkal a címkékkel lesz jelölve az összes kép!")

    uploaded_files = st.file_uploader("Fájl kiválasztása", type=["jpg", "jpeg", "png"], accept_multiple_files=st.session_state.allow_multiple_uploads, key=st.session_state.get('file_uploader_key', str(uuid.uuid4())))
    if uploaded_files:
        if not isinstance(uploaded_files, list):
            uploaded_files = [uploaded_files]

        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = []

        if not st.session_state.allow_multiple_uploads:
            st.session_state.uploaded_files = [handle_file_upload(uploaded_files[0])]
        else:
            for uploaded_file in uploaded_files:
                if uploaded_file.name not in [f.name for f in st.session_state.uploaded_files]:
                    st.session_state.uploaded_files.append(handle_file_upload(uploaded_file))

    display_images()

    col1, col2, col3 = st.columns(3)
    with col1:
        main_type, sub_type, sub_sub_type = select_main_type()

    with col2:
        view, sub_view, sub_sub_view = select_view()

    with col3:
        gender = select_gender()

    col_checkbox, col_button = st.columns([1, 1])
    with col_checkbox:
        st.session_state.multi_region = st.checkbox("Több régió jelölése", value=st.session_state.get('multi_region', False))
    
    with col_button:
        if st.session_state.multi_region:
            if st.button("Új régió hozzáadása") and not st.session_state.get('new_region_blocked', False):
                previous_region = st.session_state.regions[-1] if st.session_state.get('regions') else None
                new_region = previous_region.copy() if previous_region else {
                    'main_region': None,
                    'side': None,
                    'sub_region': None,
                    'sub_sub_region': None,
                    'sub_sub_sub_region': None,
                    'sub_sub_sub_sub_region': None,
                    'finger': None,
                    'editable': True,
                    'classification': None,
                    'severity': None,
                    'subseverity': None
                }
                new_region['editable'] = True  # Ensure the new region starts as editable
                if 'regions' not in st.session_state:
                    st.session_state.regions = []
                st.session_state.regions.append(new_region)
                st.success("Új régió hozzáadva")
                st.session_state.new_region_blocked = True
                st.rerun()
            elif st.session_state.new_region_blocked:
                st.error("Mentse a jelenlegi régiót mielőtt újat hozna létre.")

    if 'regions' in st.session_state:
        for idx, region in enumerate(st.session_state.regions):
            st.markdown(f"**Régió {idx + 1}:**")
            if 'editable' not in region:
                region['editable'] = True
            st.session_state.regions[idx] = display_region(region, idx)
            if st.session_state.multi_region:
                col_region_save_modify_delete = st.columns([1, 1, 1])
                with col_region_save_modify_delete[0]:
                    if region['editable']:
                        if st.button(f"Régió {idx + 1} mentése", key=f"save_region_{idx}"):
                            region['editable'] = False
                            st.session_state.new_region_blocked = False
                            st.rerun()
                with col_region_save_modify_delete[1]:
                    if not region['editable']:
                        if st.button(f"Régió {idx + 1} módosítása", key=f"modify_region_{idx}"):
                            region['editable'] = True
                            st.rerun()
                with col_region_save_modify_delete[2]:
                    if st.button(f"Régió {idx + 1} törlése", key=f"delete_region_{idx}"):
                        st.session_state.regions.pop(idx)
                        st.rerun()

            sub_sub_region = region.get('sub_sub_region', None)
            
            if sub_sub_region:
                classification_types = st.multiselect(
                    f"Válassza ki az osztályozás típusát (többet is választhat/régió) {idx+1}",
                    ["AO", "Gartland", "Neer"],
                    key=f"classification_types_{idx}"
                )

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

                region['classification'] = classifications

    age = st.select_slider("Életkor (opcionális)", options=["NA"] + list(range(0, 121)), value="NA")
    age_group = ""
    if age != "NA":
        age = int(age)
        age_group = "Gyermek" if age <= 18 else "Felnőtt"

    if main_type != "Normál":
        complications = select_complications()
        associated_conditions = select_associated_conditions()

    comment = st.text_area("Megjegyzés (opcionális)", key="comment", value="")

    if st.button("Feltöltés", key="upload_button"):
        try:
            upload_data = {
                "patient_id": st.session_state.patient_id,
                "main_type": main_type,
                "sub_type": sub_type,
                "sub_sub_type": sub_sub_type,
                "view": view,
                "sub_view": sub_view,
                "sub_sub_view": sub_sub_view,
                "gender": gender,
                "age": age,
                "age_group": age_group,
                "comment": comment,
                "files": st.session_state.uploaded_files,
                "complications": complications if main_type != "Normál" else [],
                "associated_conditions": associated_conditions if main_type != "Normál" else [],
                "regions": st.session_state.regions
            }
            st.session_state.confirm_data = upload_data
            st.success("Adatok sikeresen mentve. Kérem erősítse meg a feltöltést.")
            st.rerun()
        except Exception as e:
            st.error(f"Hiba történt a mentés során: {e}")

    if st.session_state.get('confirm_data'):
        confirm_and_upload_data(st.session_state.confirm_data)


    if st.button("Reset"):
        reset_session_state()
        st.session_state.file_uploader_key = str(uuid.uuid4())
        st.rerun()

if __name__ == "__main__":
    main()
