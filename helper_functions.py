import streamlit as st
def style_markdown2():
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

def style_markdown():
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

def select_subregion(main_reg):
    regions = {
        "Felső végtag": ["", "Váll", "Humerus", "Könyök", "Alkar", "Csukló", "Kéz"],
        "Alsó végtag": ["", "Medence", "Pelvis", "Femur", "Térd", "Lábszár", "Boka", "Láb"],
        "Gerinc": ["", "Cervicalis", "Thoracalis", "Lumbaris", "Sacralis", "Coccygealis"],
        "Koponya": ["", "Arckoponya", "Agykoponya", "Mandibula"],
        "Mellkas": ["", "Borda", "Sternum", "Tüdő", "Szív"],
        "Has": ["", "Máj", "Lép", "Vese", "Bél", "Hólyag"]
    }
    return st.selectbox("Régió keresése", regions.get(main_reg, [""]))

def select_sub_subregion(sub_reg):
    sub_regions = {
        "Váll": ["", "Clavicula", "Scapula", "Humerus fej", "Proximális humerus", "Humerus nyak"],
        "Humerus": ["", "Humerus diaphysis"],
        "Könyök": ["", "Distalis humerus", "Supracondylaris", "Humerus condylus", "Epicondylus", "Capitellum", "Olecranon", "Coronoid processus"],
        "Alkar": ["", "Ulna", "Radius", "Mindkét csont", "Nightstick", "Essex-Lopresti", "Galeazzi", "Monteggia"],
        "Csukló": ["", "Distalis radius", "Distalis ulna", "Carpus"],
        "Kéz": ["", "Metacarpus", "Pollex", "Phalanx"],
        "Pelvis": ["", "Ramus Pubicus ",  "Anterior inferior iliac csípőtövis avulsio",  "Anterior superior csípőtövis (ASIS) avulsion", "Duverney", "Malgaigne", "Windswept pelvis", "Pelvic bucket handle", "Medencei elégtelenség", "Nyitott könyv"],
        "Csípő": ["", "Acetabulum", "Femur fej", "Femur nyak", "Trochanterikus"],
        "Femur": ["", "Femur diaphysis", "Distalis femur", "Bisphosphonáthoz kapcsolódó"],
        "Térd": ["", "Avulsio", "Patella", "Tibia plateau"],
        "Lábszár": ["", "Tibialis tuberositas avulsio", "Tibia diaphysis", "Fibula diaphysis", "Maisonneuve"],
        "Boka": ["", "Bimallleolaris", "Trimalleolaris", "Triplane", "Tillaux", "Bosworth", "Pilon", "Wagstaffe-Le Fort"],
        "Láb": ["", "Tarsus", "Metatarsus ", "Lábujjak"]
    }
    return st.selectbox("Alrégió keresése", sub_regions.get(sub_reg, [""]))
    
def select_sub_sub_subregion(sub_sub_reg):
    sub_sub_regions = {
        "Clavicula": ["", "Sternoclavicularis", "Középső szakasz", "Acromioclavicularis"],
        "Scapula": ["", "Acromion", "Coracoid processus", "Glenoid"],
        "Humerus fej": ["", "Hill-Sachs", "Fordított Hill-Sachs"],
        "Humerus condylus": ["", "Medialis", "Lateralis"],
        "Epicondylus": ["", "Medialis", "Lateralis"],
        "Supracondylaris": ["", "Extensio", "Flexio"],
        "Distalis radius": ["", "Chauffeur", "Colles", "Smith", "Barton", "Fordított Barton"],
        "Carpus": ["", "Scaphoideum", "Lunatum", "Capitatum", "Triquetrum", "Pisiforme", "Hamatum", "Trapezoidum", "Trapezium"],
        "Metacarpus": ["", "Boxer", "Fordított Bennett"],
        "Pollex": ["", "Gamekeeper's Thumb", "Epibasal", "Rolando", "Bennett"],
        "Phalanx": ["", "Distalis phalanx", "Jersey Finger", "Mallet Finger", "Seymour", "Középső phalanx", "Volar Plate Avulsio", "Pilon", "Proximális phalanx"],
        "Femur nyak": ["", "Subcapitalis", "Transcervicalis", "Basicervicalis"],
        "Trochanterikus": ["", "Pertrochanterikus", "Intertrochanterikus", "Subtrochanterikus"],
        "Avulsio": ["", "Segond", "Fordított Segond", "Anterior cruciatum ligamentum avulsio", "Posterior cruciatum ligamentum avulsio", "Arcuatus komplex avulsio (arcuatus jel)", "Biceps femoris avulsio", "Iliotibial ligamentum avulsio", "Semimembranosus tendon avulsio", "Stieda (MCL avulsion fracture)"],
        "Tarsus": ["", "Chopart", "Calcaneus", "Lover's", "Calcaneus tuberositas avulsio", "Talus test", "Talus kupola osteochondralis", "Posterior talus processus", "Lateralis talus processus", "Talus nyak", "Aviator astragalus", "Talus fej", "Naviculare", "Medialis cuneiformis", "Középső cuneiformis", "Lateral cuneiformis", "Cuboid"],
        "Metatarsus": ["", "March", "Lisfranc törés-luxatio", "Az 5. metatarsus stressz törés", "Jones", "Pseudo-Jones", "Az 5. metatarsus proximalis avulsiós törés"]
    }
    return st.selectbox("Részletes régió keresése", sub_sub_regions.get(sub_sub_reg, [""]))
