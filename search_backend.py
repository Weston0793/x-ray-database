import streamlit as st
from firebase_helpers import db, create_zip
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import firestore
import uuid

def perform_search(query_params):
    search_type = query_params.get("main_type", "")
    search_sub_type = query_params.get("sub_type", "")
    search_sub_sub_type = query_params.get("sub_sub_type", "")
    search_view = query_params.get("view", "")
    search_sub_view = query_params.get("sub_view", "")
    search_sub_sub_view = query_params.get("sub_sub_view", "")
    search_gender = query_params.get("gender", "")
    search_main_region = query_params.get("main_region", "")
    search_sub_region = query_params.get("sub_region", "")
    search_sub_sub_region = query_params.get("sub_sub_region", "")
    search_sub_sub_sub_region = query_params.get("sub_sub_sub_region", "")
    search_sub_sub_sub_sub_region = query_params.get("sub_sub_sub_sub_region", "")
    search_complications = query_params.get("complications", [])
    search_associated_conditions = query_params.get("associated_conditions", [])
    search_classifications = query_params.get("classifications", {})
    age_filter_active = query_params.get("age_filter_active", False)
    search_age_str = query_params.get("age", "")
    search_age = eval(search_age_str) if search_age_str else None
    search_age_group = query_params.get("age_group", "")
    page = int(query_params.get("page", 1))
    items_per_page = int(query_params.get("items_per_page", 10))

    results = db.collection('images')
    query_filters = []

    if search_type:
        query_filters.append(('main_type', '==', search_type))
    if search_sub_type:
        query_filters.append(('sub_type', '==', search_sub_type))
    if search_sub_sub_type:
        query_filters.append(('sub_sub_type', '==', search_sub_sub_type))
    if search_view:
        query_filters.append(('view', '==', search_view))
    if search_sub_view:
        query_filters.append(('sub_view', '==', search_sub_view))
    if search_sub_sub_view:
        query_filters.append(('sub_sub_view', '==', search_sub_sub_view))
    if search_gender:
        query_filters.append(('gender', '==', search_gender))
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

    # Apply general filters
    for filter_field, filter_op, filter_value in query_filters:
        results = results.where(filter_field, filter_op, filter_value)

    try:
        docs = results.stream()
        file_paths = []
        metadata_list = []

        filtered_docs = []
        for doc in docs:
            data = doc.to_dict()
            if any(region_matches(region, search_main_region, search_sub_region, search_sub_sub_region, search_sub_sub_sub_region, search_sub_sub_sub_sub_region, search_classifications) for region in data.get('regions', [])):
                filtered_docs.append(doc)

        total_docs = len(filtered_docs)
        total_pages = (total_docs + items_per_page - 1) // items_per_page

        if total_docs == 0:
            st.warning("Nem található a keresési feltételeknek megfelelő elem.")
        else:
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_docs = filtered_docs[start_idx:end_idx]

            for doc in page_docs:
                data = doc.to_dict()
                display_data(data)
                file_paths.append(data['url'])
                metadata_list.append(data)

            st.write(f"Összesen {total_docs} találat. Oldal: {page} / {total_pages}")

            col10, col11 = st.columns(2)
            with col10:
                if page > 1:
                    if st.button("Előző oldal", key="prev_page"):
                        st.session_state.query_params.update(page=page-1)
                        st.rerun()
            with col11:
                if page < total_pages:
                    if st.button("Következő oldal", key="next_page"):
                        st.session_state.query_params.update(page=page+1)
                        st.rerun()

            st.markdown('<div class="button-container">', unsafe_allow_html=True)
            if st.button("Összes találat letöltése ZIP-ben"):
                num_files = len(filtered_docs)
                st.write(f"Fájlok száma: {num_files}")
                total_size_mb = num_files * 0.1
                st.write(f"Becsült teljes méret: {total_size_mb:.2f} MB")

                st.write("A ZIP fájl készítése folyamatban...")

                zip_buffer = create_zip([doc.to_dict()['url'] for doc in filtered_docs], [doc.to_dict() for doc in filtered_docs])
                st.download_button(
                    label="Letöltés",
                    data=zip_buffer,
                    file_name="all_images.zip",
                    mime="application/zip"
                )
            st.markdown('</div>', unsafe_allow_html=True)
    except GoogleAPICallError as e:
        st.error("Hiba történt a keresés végrehajtása közben. Kérjük, próbálja meg újra később.")

def region_matches(region, main_region, sub_region, sub_sub_region, sub_sub_sub_region, sub_sub_sub_sub_region, classifications):
    if main_region and region.get('main_region') != main_region:
        return False
    if sub_region and region.get('sub_region') != sub_region:
        return False
    if sub_sub_region and region.get('sub_sub_region') != sub_sub_region:
        return False
    if sub_sub_sub_region and region.get('sub_sub_sub_region') != sub_sub_sub_region:
        return False
    if sub_sub_sub_sub_region and region.get('sub_sub_sub_sub_region') != sub_sub_sub_sub_region:
        return False
    if classifications:
        for class_type, class_details in classifications.items():
            classification = region.get('classification', {}).get(class_type, {})
            if "name" in class_details and class_details["name"] and classification.get('name') != class_details["name"]:
                return False
            if "severity" in class_details and class_details["severity"] and classification.get('severity') != class_details["severity"]:
                return False
            if "subseverity" in class_details and class_details["subseverity"] and classification.get('subseverity') != class_details["subseverity"]:
                return False
    return True

def display_data(data):
    col1, col2 = st.columns(2)
    with col1:
        st.image(data['url'], use_column_width=True)
    with col2:
        st.markdown(format_data(data))

def format_data(data):
    def format_field(label, value):
        return f"**{label}:** {value}" if value not in [None, 'N/A', [], ''] else ""

    display_data = "\n".join([
        format_field('Típus', data.get('main_type')),
        format_field('Nézet', data.get('view')),
        format_field('Életkor', data.get('age')),
        format_field('Életkori csoport', data.get('age_group')),
    ])

    for idx, region in enumerate(data.get('regions', [])):
        region_data = "\n".join([
            f"**Régió {idx + 1}:**",
            format_field('Fő régió', region.get('main_region')),
            format_field('Régió', region.get('sub_region')),
            format_field('Alrégió', region.get('sub_sub_region')),
            format_field('Részletes régió', region.get('sub_sub_sub_region')),
            format_field('Legrészletesebb régió', region.get('sub_sub_sub_sub_region')),
        ])
        display_data += f"\n\n{region_data}"
        if 'classification' in region:
            for class_type, class_details in region['classification'].items():
                classification_data = "\n".join([
                    f"**{class_type} osztályozás:**",
                    format_field('Név', class_details.get('name')),
                    format_field('Főkategória', class_details.get('severity')),
                    format_field('Alkategória', class_details.get('subseverity')),
                ])
                display_data += f"\n{classification_data}"

    return display_data
