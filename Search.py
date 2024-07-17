import streamlit as st
from google.cloud import firestore
from firebase_helpers import db, create_zip
import uuid
from google.api_core.exceptions import GoogleAPICallError

def main():
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
    associated_conditions = ["Nyílt", "Darabos", "Avulsio", "Luxatio", "Subluxatio", "Idegsérülés", "Nagyobb Érsérülés", "Szalagszakadás", "Meniscus Sérülés", "Epiphysis Sérülés", "Fertőzés", "Cysta", "Tumor", "Genetikai"]

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

    search_conditions = st.multiselect("Társuló Komplikációk keresése", associated_conditions)

    # Age filter with checkbox
    age_filter_active = st.checkbox("Életkor keresése (intervallum)")
    if age_filter_active:
        search_age = st.slider("Életkor keresése (intervallum)", min_value=0, max_value=120, value=(0, 18), step=1, format="%d")
    else:
        search_age = None

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
            "conditions": search_conditions,
            "age_filter_active": age_filter_active,
            "age": str(search_age) if search_age else "",
            "page": page,
            "items_per_page": items_per_page
        }
        st.experimental_rerun()

    if 'search_button_clicked' in st.session_state:
        query_params = st.session_state.query_params
        search_type = query_params.get("type", "")
        search_view = query_params.get("view", "")
        search_main_region = query_params.get("main_region", "")
        search_sub_region = query_params.get("sub_region", "")
        search_conditions = query_params.get("conditions", [])
        age_filter_active = query_params.get("age_filter_active", False)
        search_age_str = query_params.get("age", "")
        search_age = eval(search_age_str) if search_age_str else None
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
        if search_conditions:
            for condition in search_conditions:
                query_filters.append(('associated_conditions', 'array_contains', condition))
        if search_age is not None:
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
                    st.markdown(f'<div class="result-image"><img src="{data["url"]}" alt="{data["type"]}, {data["view"]}, {data["main_region"]}, {data["sub_region"]}" style="width:100%;"><br><strong>{data["type"]}, {data["view"]}, {data["main_region"]}, {data["sub_region"]}</strong></div>', unsafe_allow_html=True)
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
                    # Show information about the files before creating the zip
                    num_files = len(all_docs)
                    st.write(f"Fájlok száma: {num_files}")
                    # Calculate total size (dummy calculation, replace with actual size calculation if needed)
                    total_size_mb = num_files * 0.1  # Assuming each file is approximately 0.1 MB
                    st.write(f"Becsült teljes méret: {total_size_mb:.2f} MB")
                    
                    st.write("A ZIP fájl készítése folyamatban...")

                    zip_buffer = create_zip([doc.to_dict()['url'] for doc in all_docs], [doc.to_dict() for doc in all_docs])  # Include metadata in the zip
                    st.download_button(
                        label="Letöltés",
                        data=zip_buffer,
                        file_name="all_images.zip",
                        mime="application/zip"
                    )
                st.markdown('</div>', unsafe_allow_html=True)
        except GoogleAPICallError as e:
            st.error("Hiba történt a keresés végrehajtása közben. Kérjük, próbálja meg újra később.")

if __name__ == "__main__":
    main()
