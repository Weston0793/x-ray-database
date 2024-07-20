import streamlit as st
from firebase_helpers import db, create_zip
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import firestore
import uuid

def perform_search(query_params):
    search_type = query_params.get("type", "")
    search_view = query_params.get("view", "")
    search_main_region = query_params.get("main_region", "")
    search_sub_region = query_params.get("sub_region", "")
    search_sub_sub_region = query_params.get("sub_sub_region", "")
    search_sub_sub_sub_region = query_params.get("sub_sub_sub_region", "")
    search_complications = query_params.get("complications", [])
    search_associated_conditions = query_params.get("associated_conditions", [])
    age_filter_active = query_params.get("age_filter_active", False)
    search_age_str = query_params.get("age", "")
    search_age = eval(search_age_str) if search_age_str else None
    search_age_group = query_params.get("age_group", "")
    page = int(query_params.get("page", 1))
    items_per_page = int(query_params.get("items_per_page", 10))

    results = db.collection('images')
    query_filters = []

    if search_type:
        query_filters.append(('type', '==', search_type))
    if search_view:
        query_filters.append(('view', '==', search_view))
    if search_main_region:
        query_filters.append(('main_region', '==', search_main_region))
    if search_sub_region:
        query_filters.append(('sub_region', '==', search_sub_region))
    if search_sub_sub_region:
        query_filters.append(('sub_sub_region', '==', search_sub_sub_region))
    if search_sub_sub_sub_region:
        query_filters.append(('sub_sub_sub_region', '==', search_sub_sub_sub_region))
    if search_complications:
        for complication in search_complications:
            query_filters.append(('complications', 'array_contains', complication))
    if search_associated_conditions:
        for condition in search_associated_conditions:
            query_filters.append(('associated_conditions', 'array_contains', condition))
    if search_age_group:
        if search_age_group == "Gyermek":
            query_filters.append(('age', '>=', 0))
            query_filters.append(('age', '<=', 18))
        elif search_age_group == "Felnőtt":
            query_filters.append(('age', '>=', 19))
            query_filters.append(('age', '<=', 120))
    if age_filter_active and search_age is not None:
        if isinstance(search_age, tuple):
            query_filters.append(('age', '>=', search_age[0]))
            query_filters.append(('age', '<=', search_age[1]))
        else:
            query_filters.append(('age', '==', search_age))

    for filter_field, filter_op, filter_value in query_filters:
        results = results.where(filter_field, filter_op, filter_value)

    try:
        docs = results.stream()
        file_paths = []
        metadata_list = []

        all_docs = list(docs)
        total_docs = len(all_docs)
        total_pages = (total_docs + items_per_page - 1) // items_per_page

        if total_docs == 0:
            st.warning("Nem található a keresési feltételeknek megfelelő elem.")
        else:
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_docs = all_docs[start_idx:end_idx]

            for doc in page_docs:
                data = doc.to_dict()
                display_data = f"""
                <div class="result-image">
                    <img src="{data['url']}" alt="{data.get('type', 'N/A')}, {data.get('view', 'N/A')}, {data.get('main_region', 'N/A')}, {data.get('sub_region', 'N/A')}" style="width:100%;">
                    <br><strong>Típus: {data.get('type', 'N/A')}</strong>
                    <br><strong>Nézet: {data.get('view', 'N/A')}</strong>
                    <br><strong>Fő régió: {data.get('main_region', 'N/A')}</strong>
                    <br><strong>Régió: {data.get('sub_region', 'N/A')}</strong>
                    <br><strong>Alrégió: {data.get('sub_sub_region', 'N/A')}</strong>
                    <br><strong>Részletes régió: {data.get('sub_sub_sub_region', 'N/A')}</strong>
                    <br><strong>Életkor: {data.get('age', 'N/A')}</strong>
                    <br><strong>Életkori csoport: {data.get('age_group', 'N/A')}</strong>
                    <br><strong>Megjegyzés: {data.get('comment', 'N/A')}</strong>
                    <br><strong>Komplikációk: {", ".join(data.get('complications', []))}</strong>
                    <br><strong>Társuló Kórállapotok: {", ".join(data.get('associated_conditions', []))}</strong>
                </div>
                """
                st.markdown(display_data, unsafe_allow_html=True)
                file_paths.append(data['url'])
                metadata_list.append(data)

            st.write(f"Összesen {total_docs} találat. Oldal: {page} / {total_pages}")

            col7, col8 = st.columns(2)
            with col7:
                if page > 1:
                    if st.button("Előző oldal", key="prev_page"):
                        st.session_state.query_params.update(
                            page=page-1
                        )
                        st.experimental_rerun()
            with col8:
                if page < total_pages:
                    if st.button("Következő oldal", key="next_page"):
                        st.session_state.query_params.update(
                            page=page+1
                        )
                        st.experimental_rerun()

            st.markdown('<div class="button-container">', unsafe_allow_html=True)
            if st.button("Összes találat letöltése ZIP-ben"):
                num_files = len(all_docs)
                st.write(f"Fájlok száma: {num_files}")
                total_size_mb = num_files * 0.1
                st.write(f"Becsült teljes méret: {total_size_mb:.2f} MB")
                
                st.write("A ZIP fájl készítése folyamatban...")

                zip_buffer = create_zip([doc.to_dict()['url'] for doc in all_docs], [doc.to_dict() for doc in all_docs])
                st.download_button(
                    label="Letöltés",
                    data=zip_buffer,
                    file_name="all_images.zip",
                    mime="application/zip"
                )
            st.markdown('</div>', unsafe_allow_html=True)
    except GoogleAPICallError as e:
        st.error("Hiba történt a keresés végrehajtása közben. Kérjük, próbálja meg újra később.")
