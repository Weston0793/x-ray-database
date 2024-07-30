import os
import uuid
import io
import zipfile
import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st
import requests
import datetime

# Initialize Firebase
def initialize_firebase():
    if not firebase_admin._apps:
        firebase_config = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }

        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred, {
            'storageBucket': f"{firebase_config['project_id']}.appspot.com"
        })

initialize_firebase()
db = firestore.client()
bucket = storage.bucket()

# Upload file to Firebase Storage
def upload_to_storage(file_path, destination_blob_name):
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url

# Download file from Firebase Storage
def download_from_storage(source_blob_name, destination_file_name):
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

# Save image and metadata to Firestore and Firebase Storage
def save_image(patient_id, files, main_type, sub_type, sub_sub_type, view, sub_view, sub_sub_view, age, age_group, gender, comment, complications, associated_conditions, regions):
    db = firestore.client()
    for file in files:
        filename = file.name
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join("/tmp", unique_filename)

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        public_url = upload_to_storage(file_path, unique_filename)

        doc_ref = db.collection('images').document(unique_filename)
        doc_ref.set({
            'patient_id': patient_id,
            'filename': unique_filename,
            'main_type': main_type,
            'sub_type': sub_type,
            'sub_sub_type': sub_sub_type,
            'view': view,
            'sub_view': sub_view,
            'sub_sub_view': sub_sub_view,
            'gender': gender,
            'age': age,
            'age_group': age_group,
            'comment': comment,
            'url': public_url,
            'complications': complications,
            'associated_conditions': associated_conditions,
            'regions': regions
        })

        # Ensure to delete the file after upload to save space
        os.remove(file_path)
        
def create_zip(file_paths, metadata_list=None):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for idx, file_url in enumerate(file_paths):
            file_name = f"image_{idx}.jpg"
            zip_file.writestr(file_name, download_file(file_url))
            if metadata_list:
                metadata_name = f"metadata_{idx}.txt"
                metadata_content = "\n".join([f"{key}: {value}" for key, value in metadata_list[idx].items()])
                zip_file.writestr(metadata_name, metadata_content)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def download_file(url):
    response = requests.get(url)
    return response.content
    
def save_comment(name, comment):
    doc_ref = db.collection('comments').document()
    doc_ref.set({
        'name': name,
        'comment': comment,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def get_comments(start, limit):
    comments_ref = db.collection('comments').order_by('timestamp', direction=firestore.Query.DESCENDING).offset(start).limit(limit)
    docs = comments_ref.stream()
    comments = [{'name': doc.to_dict().get('name'), 'comment': doc.to_dict().get('comment'), 'timestamp': doc.to_dict().get('timestamp')} for doc in docs]
    for comment in comments:
        if isinstance(comment['timestamp'], datetime.datetime):
            comment['timestamp'] = comment['timestamp'].astimezone().replace(tzinfo=None)
    return comments

def get_counts():
    counts = {
        "Felső végtag": {"Váll": {}, "Humerus": {}, "Könyök": {}, "Alkar": {}, "Csukló": {}, "Kéz": {}},
        "Alsó végtag": {"Medence": {}, "Pelvis": {}, "Femur": {}, "Térd": {}, "Lábszár": {}, "Boka": {}, "Láb": {}},
        "Gerinc": {"Cervicalis": {}, "Thoracalis": {}, "Lumbalis": {}, "Sacrum": {}, "Coccyx": {}},
        "Koponya": {"Arckoponya": {}, "Koponyaalap": {}, "Mandibula": {}, "Calvaria":{}},
        "Mellkas": {"Borda": {}, "Sternum": {}},
    }
    views = ["AP", "Lateral"]
    main_types = ["Normál", "Törött"]

    data = []

    docs = db.collection('images').stream()
    for doc in docs:
        doc_data = doc.to_dict()
        patient_id = doc_data.get('patient_id')
        regions = doc_data.get('regions', [])
        view = doc_data.get('view')
        main_type = doc_data.get('main_type')

        patient_region_counts = {}

        for region in regions:
            main_region = region.get('main_region')
            sub_region = region.get('sub_region')
            if main_region in counts and sub_region in counts[main_region]:
                key = f"{main_type}_{view}"
                if main_region not in patient_region_counts:
                    patient_region_counts[main_region] = {}
                if sub_region not in patient_region_counts[main_region]:
                    patient_region_counts[main_region][sub_region] = set()
                patient_region_counts[main_region][sub_region].add(key)

        for main_region in patient_region_counts:
            for sub_region in patient_region_counts[main_region]:
                for key in patient_region_counts[main_region][sub_region]:
                    if key not in counts[main_region][sub_region]:
                        counts[main_region][sub_region][key] = 0
                    counts[main_region][sub_region][key] += 1
                    data.append([main_region, sub_region, view, main_type, counts[main_region][sub_region][key]])

    return counts, data

def get_progress_summary(counts):
    summary = {}
    for main_region, sub_regions in counts.items():
        summary[main_region] = {"total": 0, "progress": 0, "subregions": {}}
        for sub_region, view_types in sub_regions.items():
            sub_region_total = 0
            sub_region_progress = 0
            for view_type, count in view_types.items():
                sub_region_total += 50
                sub_region_progress += count
            summary[main_region]["total"] += sub_region_total
            summary[main_region]["progress"] += sub_region_progress
            summary[main_region]["subregions"][sub_region] = {"total": sub_region_total, "count": sub_region_progress}
    return summary
