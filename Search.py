import streamlit as st
from firebase_helpers import db, create_zip
import uuid

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
    search_button_clicked = st.button("Keresés")

    if search_button_clicked:
        page = 1  # Reset to the first page on new search
        st.experimental_set_query_params(
            search_button_clicked=True,
            type=search_type,
            view=search_view,
            main_region=search_main_region,
            sub_region=search_sub_region,
            conditions=search_conditions,
            age_filter_active=age_filter_active,
            age=search_age,
            page=page,
            items_per_page=items_per_page
        )
        st.experimental_rerun()

    # Get query params to manage pagination and search state
    query_params = st.experimental_get_query_params()
    if 'search_button_clicked' in query_params:
        search_type = query_params.get("type", [""])[0]
        search_view = query_params.get("view", [""])[0]
        search_main_region = query_params.get("main_region", [""])[0]
        search_sub_region = query_params.get("sub_region", [""])[0]
        search_conditions = query_params.get("conditions", [])
        age_filter_active = query_params.get("age_filter_active", [""])[0] == "True"
        search_age = eval(query_params.get("age", ["(0, 18)"])[0])
        page = int(query_params.get("page", [1])[0])
        items_per_page = int(query_params.get("items_per_page", [10])[0])

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
            query_filters.append(('age', '>=', search_age[0]))
            query_filters.append(('age', '<=', search_age[1]))

        for filter_field, filter_op, filter_value in query_filters:
            results = results.where(filter_field, filter_op, filter_value)

        docs = results.stream()
        file_paths = []

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

            st.write(f"Összesen {total_docs} találat. {total_pages} oldal.")

            col7, col8 = st.columns(2)
            with col7:
                if page > 1:
                    if st.button("Előző oldal", key="prev_page"):
                        st.experimental_set_query_params(
                            search_button_clicked=True,
                            type=search_type,
                            view=search_view,
                            main_region=search_main_region,
                            sub_region=search_sub_region,
                            conditions=search_conditions,
                            age_filter_active=age_filter_active,
                            age=search_age,
                            page=page-1,
                            items_per_page=items_per_page
                        )
                        st.experimental_rerun()
            with col8:
                if page < total_pages:
                    if st.button("Következő oldal", key="next_page"):
                        st.experimental_set_query_params(
                            search_button_clicked=True,
                            type=search_type,
                            view=search_view,
                            main_region=search_main_region,
                            sub_region=search_sub_region,
                            conditions=search_conditions,
                            age_filter_active=age_filter_active,
                            age=search_age,
                            page=page+1,
                            items_per_page=items_per_page
                        )
                        st.experimental_rerun()

            if file_paths:
                zip_buffer = create_zip([data['url'] for data in (doc.to_dict() for doc in all_docs)])
                st.download_button(
                    label="Képek letöltése ZIP-ben",
                    data=zip_buffer,
                    file_name="images.zip",
                    mime="application/zip"
                )

if __name__ == "__main__":
    main()
