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
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="search-title">Képek keresése</div>', unsafe_allow_html=True)

    predefined_types = ["", "Törött", "Normál", "Luxatio", "Subluxatio", "Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Malignus Tumor", "Benignus Tumor", "Metastasis", "Rheumatoid Arthritis", "Cysta", "Genetikai/Veleszületett", "Egyéb"]
    predefined_views = ["", "AP", "Lateral", "Ferde", "PA", "Speciális"]
    associated_conditions = ["Nyílt", "Darabos", "Avulsio", "Luxatio", "Subluxatio", "Idegsérülés", "Nagyobb Érsérülés", "Szalagszakadás", "Meniscus Sérülés", "Epiphysis Sérülés", "Fertőzés", "Cysta", "Tumor", "Genetikai"]

    search_type = st.selectbox("Típus keresése", predefined_types)
    search_view = st.selectbox("Nézet keresése", predefined_views)
    search_main_region = st.selectbox("Fő régió keresése", ["", "Felső végtag", "Alsó végtag", "Gerinc", "Koponya"])

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
    search_age = st.slider("Életkor keresése", min_value=0, max_value=120, step=1, format="%d")

    page = st.number_input("Oldal", min_value=1, step=1, value=1)
    items_per_page = 10

    if st.button("Keresés"):
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
            query_filters.append(('age', '==', search_age))

        for filter_field, filter_op, filter_value in query_filters:
            results = results.where(filter_field, filter_op, filter_value)

        docs = results.stream()
        file_paths = []

        all_docs = list(docs)
        total_docs = len(all_docs)
        total_pages = (total_docs + items_per_page - 1) // items_per_page

        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_docs = all_docs[start_idx:end_idx]

        for doc in page_docs:
            data = doc.to_dict()
            st.image(data['url'], caption=f"{data['type']}, {data['view']}, {data['main_region']}, {data['sub_region']}")
            file_paths.append(data['url'])

        st.write(f"Összesen {total_docs} találat. {total_pages} oldal.")

        if page > 1:
            if st.button("Előző oldal", key="prev_page"):
                st.session_state.page = page - 1
                st.experimental_rerun()

        if page < total_pages:
            if st.button("Következő oldal", key="next_page"):
                st.session_state.page = page + 1
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
