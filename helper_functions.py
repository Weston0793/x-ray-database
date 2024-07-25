import streamlit as st

def select_main_type():
    main_type = st.radio("Válassza ki a típusát", ["Normál", "Törött", "Egyéb"], key="main_type")
    sub_type = ""
    sub_sub_type = ""
    if main_type == "Egyéb":
        sub_type = st.selectbox("Specifikálás (Egyéb)", [
            "Luxatio", "Subluxatio", "Szalagszakadás", "Osteoarthritis", "Osteoporosis", 
            "Osteomyelitis", "Cysta", "Álízűlet", "Malignus Tumor", "Benignus Tumor", 
            "Metastasis", "Rheumatoid Arthritis", "Genetikai/Veleszületett", "Implant", "Egyéb"
        ])
        if sub_type in ["Malignus Tumor", "Benignus Tumor", "Genetikai/Veleszületett", "Egyéb"]:
            sub_sub_type = st.text_input("Adja meg a specifikus típust (Egyéb)")
    return main_type, sub_type, sub_sub_type

def select_view():
    view = st.radio("Válassza ki a nézetet", ["AP", "Lateral", "Egyéb"], key="view")
    sub_view = ""
    sub_sub_view = ""
    if view == "Egyéb":
        sub_view = st.selectbox("Specifikálás (Egyéb Nézet)", ["Ferde", "PA", "Speciális"])
        if sub_view == "Speciális":
            sub_sub_view = st.text_input("Adja meg a specifikus nézetet (Speciális)")
    return view, sub_view, sub_sub_view

def select_main_region():
    main_region = st.selectbox("Fő régió", ["Felső végtag", "Alsó végtag", "Gerinc", "Koponya", "Mellkas", "Has"])
    return main_region

def select_complications():
    complications = st.multiselect("Komplikációk (többet is választhat)", [
        "Elmozdulás", "Intraarticularis", "Nyílt", "Fragmentált", "Avulsio", "Luxatio", "Subluxatio", 
        "Idegsérülés", "Nagyobb Érsérülés", "Szalagszakadás", 
        "Meniscus Sérülés", "Epiphysis Sérülés", "Fertőzés"
    ])
    return complications

def select_associated_conditions():
    associated_conditions = st.multiselect("Társuló Kórállapotok (többet is választhat)", [
        "Osteoarthritis", "Osteoporosis", "Osteomyelitis", "Cysta", "Álízűlet", "Implant",
        "Rheumatoid Arthritis", "Metastasis", "Malignus Tumor", 
        "Benignus Tumor", "Genetikai"
    ])
    return associated_conditions

def select_subregion(main_reg):
    regions = {
        "Felső végtag": ["", "Váll", "Humerus", "Könyök", "Alkar", "Csukló", "Kéz"],
        "Alsó végtag": ["", "Medence", "Csípő", "Femur", "Térd", "Lábszár", "Boka", "Láb"],
        "Gerinc": ["", "Cervicalis", "Thoracalis", "Lumbaris", "Sacralis", "Coccygealis"],
        "Koponya": ["", "Arckoponya", "Agykoponya", "Mandibula"],
        "Mellkas": ["", "Borda", "Sternum", "Tüdő", "Szív"],
        "Has": ["", "Máj", "Lép", "Vese", "Bél", "Hólyag"]
    }
    return st.selectbox("Régió", regions.get(main_reg, [""]))

def select_sub_subregion(sub_reg):
    sub_regions = {
        "Váll": ["", "Clavicula", "Scapula", "Proximális humerus"],
        "Humerus": ["", "Humerus diaphysis"],
        "Könyök": ["", "Distalis humerus", "Proximalis ulna", "Proximalis radius"],
        "Alkar": ["", "Ulna diaphysis", "Radius diaphysis", "Mindkét csont", "Nightstick", "Essex-Lopresti", "Galeazzi", "Monteggia"],
        "Csukló": ["", "Distalis radius", "Distalis ulna", "Carpus"],
        "Kéz": ["", "Metacarpus", "Pollex", "Phalanx"],
        "Pelvis": ["", "Ramus Pubicus ",  "Anterior inferior csípőtövis avulsio",  "Anterior superior csípőtövis (ASIS) avulsio", "Duverney", "Malgaigne", "Windswept pelvis", "Pelvic bucket handle", "Medencei elégtelenség", "Nyitott könyv"],
        "Csípő": ["", "Acetabulum", "Proximalis femur", "Femur fej", "Femur nyak", "Trochanterikus"],
        "Femur": ["", "Femur diaphysis", "Distalis femur", "Bisphosphonáthoz kapcsolódó"],
        "Térd": ["", "Avulsio", "Patella",  "Proximalis tibia", "Proximalis fibula"],
        "Lábszár": ["", "Tibia diaphysis", "Fibula diaphysis", "Tuberositas tibiae avulsio", "Maisonneuve"],
        "Boka": ["", "Distalis tibia", "Distalis fibula", "Bimalleolaris", "Trimalleolaris", "Triplane", "Tillaux", "Bosworth", "Pilon", "Wagstaffe-Le Fort"],
        "Láb": ["", "Tarsus", "Metatarsus", "Hallux", "Lábujjak"]
    }
    return st.selectbox("Alrégió", sub_regions.get(sub_reg, [""]))
    
def select_sub_sub_subregion(sub_sub_reg):
    sub_sub_regions = {
        "Clavicula": ["", "Perifériás harmad", "Középső harmad", "Centrális harmad"],
        "Scapula": ["", "Scapula nyúlványok", "Scapula test", "Scapula nyak", "Cavitas glenoidalis", "Kombinált/Romos"],
        "Proximalis humerus": ["", "Humerus nyak", "Tuberculum majus", "Tuberculum minus", "Humerus fej", "Hill-Sachs", "Fordított Hill-Sachs"],
        "Distalis humerus": ["", "Supracondylaris", "Humerus condylus", "Epicondylus", "Capitellum"], 
        "Proximalis ulna": ["", "Olecranon", "Coronoid processus"], 
        "Proximalis radius": ["", "Radius fej", "Radius nyak"],
        "Distalis radius": ["", "Chauffeur", "Colles", "Smith", "Barton", "Fordított Barton"],
        "Distalis ulna": ["", "Processus styloideus ulnae"], 
        "Carpus": ["", "Scaphoideum", "Lunatum", "Capitatum", "Triquetrum", "Pisiforme", "Hamatum", "Trapesoideum", "Trapesium"],
        "Metacarpus": ["",  "Boxer", "Fordított Bennett"],
        "Pollex": ["", "Distalis phalanx", "Proximalis phalanx", "Gamekeeper's Thumb", "Epibasal", "Rolando", "Bennett"],
        "Phalanx": ["", "Distalis phalanx", "Középső phalanx", "Proximalis phalanx"],
        "Avulsio": ["", "Lig. cruciatum anterior avulsio", " Lig. cruciatum posterior avulsio", "Arcuatus komplex avulsio (arcuatus jel)", "Biceps femoris avulsio", "Lig. iliotibiale avulsio", "Semimembranosus tendon avulsio","Segond", "Fordított Segond", "Stieda (MCL avulsion fracture)"],
        "Proximalis tibia": ["", "Tibia plateau"],
        "Proximalis fibula": ["", "Fibula fej", "Fibula nyak"],
        "Tarsus": ["", "Chopart", "Calcaneus", "Talus", "Naviculare", "Medialis cuneiformis", "Középső cuneiformis", "Lateral cuneiformis", "Cuboideum"],
        "Metatarsus": ["", "March", "Lisfranc törés-luxatio", "V. metatarsus stressz törés", "Jones", "Pseudo-Jones", "V. metatarsus proximalis avulsio"]
    }
    return st.selectbox("Részletes régió", sub_sub_regions.get(sub_sub_reg, [""]))

def select_sub_sub_sub_subregion(sub_sub_sub_reg):
    sub_sub_sub_regions = {
        "Nyúlványtörések": ["", "Acromion", "Coracoid processus"],
        "Scapula nyak": ["", "Stabil", "Instabil"],
        "Cavitas glenoidalis": ["", "Bankart", "Fordított Bankart"],
        "Humerus nyak": ["", "Collum anatomicum", "Collum chirurgicum"], 
        "Humerus condylus": ["", "Medialis", "Lateralis"],
        "Epicondylus": ["", "Medialis", "Lateralis"],
        "Supracondylaris": ["", "Extensio", "Flexio"],
        "Scaphoideum": ["", "De Quervain", ],
        "Hamatum": ["", "Hamulus"],
        "Distalis phalanx": ["", "Basis", "Corpus", "Caput", "Jersey Finger", "Mallet Finger", "Seymour"],
        "Középső phalanx": ["", "Basis", "Corpus", "Caput", "Volar Plate avulsio", "Pilon"],
        "Proximalis phalanx": ["", "Basis", "Corpus", "Caput"],
        "Femur nyak": ["", "Subcapitalis", "Transcervicalis", "Basicervicalis"],
        "Trochanterikus": ["", "Pertrochanterikus", "Intertrochanterikus", "Subtrochanterikus"],
        "Calcaneus": ["", "Lover's", "Calcaneus tuberositas avulsio"],
        "Talus": ["", "Talus fej", "Talus test", "Talus nyak", "Talus kupola", "Posterior talus processus", "Lateralis talus processus", "Aviator astragalus"],
        "Cuboideum": ["","Nutcracker"],
    }
    return st.selectbox("Legrészletes régió", sub_sub_sub_regions.get(sub_sub_sub_reg, [""]))  
    
def select_finger(sub_sub_regions):
    side = st.selectbox("Oldal", ["Bal", "Jobb"])
    
    finger = None
    if sub_sub_regions in ["Metacarpus", "Phalanx", "Metatarsus", "Lábujjak", "Pollex", "Hallux"]:
        if sub_sub_regions in ["Pollex", "Hallux"]:
            finger = "I"
        elif sub_sub_regions in ["Phalanx", "Lábujjak"]:
            finger = st.selectbox("Ujj", ["II", "III", "IV", "V"])   
        else:
            finger = st.selectbox("Ujj", ["I", "II", "III", "IV", "V"])
    return finger, side

def ao_classification(sub_sub_reg):
    ao_classes = {
        "Proximalis humerus": {
            "11A": "Extraarticularis, egyrészű",
            "11B": "Extraarticularis, két rész",
            "11C": "Ízületi vagy négy rész",
        },
         "Humerus diaphysis": {
            "12A": "Egyszerű",
            "12B": "Ék",
            "12C": "Többrészű"
        },
        "Distalis humerus": {
            "13A": "Extraarticularis",
            "13B": "Részleges ízületi",
            "13C": "Teljes ízületi"
        },
        "Proximalis femur": {
            "31A": "Trochantericus régió",
            "31B": "Femur nyak",
            "31C": "Femur fej"
        },
        "Femur diaphysis": {
            "32A": "Egyszerű",
            "32B": "Ék",
            "32C": "Többrészű"
        },
        "Distalis femur": {
            "33A": "Extraarticularis",
            "33B": "Részleges ízületi",
            "33C": "Teljes ízületi"
        },
        "Proximalis tibia": {
            "41A": "Extraarticularis",
            "41B": "Részleges ízületi",
            "41C": "Teljes ízületi"
        },
        "Tibia diaphysis": {
            "42A": "Egyszerű",
            "42B": "Ék",
            "42C": "Többrészű"
        },
        "Distalis tibia": {
            "43A": "Extraarticularis",
            "43B": "Részleges ízületi",
            "43C": "Teljes ízületi"
        },
        "Proximalis radius": {
            "2R1A": "Extraarticularis",
            "2R1B": "Részleges ízületi",
            "2R1C": "Teljes ízületi"
        },
        "Radius diaphysis": {
            "2R2A": "Egyszerű",
            "2R2B": "Ék",
            "2R2C": "Többrészű"
        },
        "Distalis radius": {
            "2R3A": "Extraarticularis",
            "2R3B": "Részleges ízületi",
            "2R3C": "Teljes ízületi"
        },
        "Proximalis ulna": {
            "2U1A": "Extraarticularis",
            "2U1B": "Részleges ízületi",
            "2U1C": "Teljes ízületi"
        },
        "Ulna diaphysis": {
            "2U2A": "Egyszerű",
            "2U2B": "Ék",
            "2U2C": "Többrészű"
        },
        "Distalis ulna": {
            "2U3A": "Extraarticularis",
            "2U3B": "Részleges ízületi",
            "2U3C": "Teljes ízületi"
        }
    }

    ao_type_options = [f"{key} - {value}" for key, value in ao_classes.get(sub_sub_reg, {}).items()]
    if not ao_type_options:
        return None, None, None

    ao_type = st.selectbox("AO klasszifikáció típusa", ao_type_options)
    if not ao_type:
        return None, None, None

    ao_severity = ao_type.split(" - ")[0]
    ao_subtype = st.selectbox("AO altípus részletezése", get_ao_subtype_details(ao_severity))
    
    classification_name = "AO klasszifikáció"
    ao_subseverity = ao_subtype
    
    return classification_name, ao_severity, ao_subseverity

def get_ao_subtype_details(ao_type):
    details = {
        "11A": {
            "1": "Tuberosity",
            "2": "Sebészeti nyak",
            "3": "Vertikális"
        },
        "11B": {
            "1": "Sebészeti nyak"
        },
        "11C": {
            "1": "Anatómiai nyak",
            "3": "Anatómiai nyak metafízis töréssel"
        },
        "12A": {
            "1": "Spirális",
            "2": "Ferde (≥ 30°)",
            "3": "Keresztirányú (< 30°)"
        },
        "12B": {
            "2": "Ép ék",
            "3": "Töredezett ék"
        },
        "12C": {
            "2": "Ép szegmentális",
            "3": "Töredezett szegmentális"
        },
        "13A": {
            "1": "Avulsio",
            "2": "Egyszerű",
            "3": "Ék vagy többrészű"
        },
        "13B": {
            "1": "Laterális sagittális",
            "2": "Mediális sagittális",
            "3": "Frontal/coronal plane"
        },
        "13C": {
            "1": "Egyszerű ízületi, egyszerű metafízis",
            "2": "Egyszerű ízületi, ék vagy többrészű metafízis",
            "3": "Többrészű ízületi, ék vagy többrészű metafízis"
        },
        "31A": {
            "1": "Egyszerű pertrochantericus",
            "2": "Többrészű pertrochantericus",
            "3": "Intertrochantericus (fordított dőlésszög)"
        },
        "31B": {
            "1": "Subcapitalis",
            "2": "Transcervicalis",
            "3": "Basicervicalis"
        },
        "31C": {
            "1": "Hasadék",
            "2": "Benyomódás"
        },
        "32A": {
            "1": "Spirális",
            "2": "Ferde (≥ 30°)",
            "3": "Keresztirányú (< 30°)"
        },
        "32B": {
            "2": "Ép ék",
            "3": "Töredezett ék"
        },
        "32C": {
            "2": "Ép szegmentális",
            "3": "Töredezett szegmentális"
        },
        "33A": {
            "1": "Avulsio",
            "2": "Egyszerű",
            "3": "Ék vagy többrészű"
        },
        "33B": {
            "1": "Lateral condyle, sagittal",
            "2": "Medial condyle, sagittal",
            "3": "Frontal/coronal"
        },
        "33C": {
            "1": "Egyszerű ízületi, egyszerű metafízis",
            "2": "Egyszerű ízületi, ék vagy többrészű metafízis",
            "3": "Többrészű ízületi, egyszerű, ék vagy többrészű metafízis"
        },
        "41A": {
            "1": "Avulsio",
            "2": "Egyszerű",
            "3": "Ék vagy többrészű"
        },
        "41B": {
            "1": "Hasadék",
            "2": "Benyomódás",
            "3": "Hasadék benyomódással"
        },
        "41C": {
            "1": "Egyszerű ízületi, egyszerű metafízis",
            "2": "Egyszerű ízületi, ék vagy többrészű metafízis",
            "3": "Többrészű ízületi, többrészű metafízis"
        },
        "42A": {
            "1": "Spirális",
            "2": "Ferde (≥ 30°)",
            "3": "Keresztirányú (< 30°)"
        },
        "42B": {
            "2": "Ép ék",
            "3": "Töredezett ék"
        },
        "42C": {
            "2": "Ép szegmentális",
            "3": "Töredezett szegmentális"
        },
        "43A": {
            "1": "Egyszerű",
            "2": "Ék",
            "3": "Többrészű"
        },
        "43B": {
            "1": "Hasadék",
            "2": "Hasadék benyomódással",
            "3": "Benyomódás"
        },
        "43C": {
            "1": "Egyszerű ízületi, egyszerű metafízis",
            "2": "Egyszerű ízületi, többrészű metafízis",
            "3": "Többrészű ízületi és többrészű metafízis"
        },
        "2R1A": {
            "1": "Bicipital tuberosity avulsio",
            "2": "Nyak, egyszerű",
            "3": "Nyak, többrészű"
        },
        "2R1B": {
            "1": "Egyszerű",
            "3": "Töredezett"
        },
        "2R1C": {
            "1": "Egyszerű",
            "3": "Többrészű"
        },
        "2R2A": {
            "1": "Spirális",
            "2": "Ferde (≥ 30°)",
            "3": "Keresztirányú (< 30°)"
        },
        "2R2B": {
            "2": "Ép ék",
            "3": "Töredezett ék"
        },
        "2R2C": {
            "2": "Ép szegmentális",
            "3": "Töredezett szegmentális"
        },
        "2R3A": {
            "1": "Radialis styloid avulsio",
            "2": "Egyszerű",
            "3": "Ék vagy többrészű"
        },
        "2R3B": {
            "1": "Sagittalis",
            "2": "Dorsalis perem (Barton's)",
            "3": "Volar perem (reverse Barton's, Goyrand-Smith's II)"
        },
        "2R3C": {
            "1": "Egyszerű ízületi és metafízis",
            "2": "Többrészű metafízis",
            "3": "Többrészű ízületi, egyszerű vagy többrészű metafízis"
        },
        "2U1A": {
            "1": "Triceps insertion avulsio",
            "2": "Egyszerű metafízis",
            "3": "Többrészű metafízis"
        },
        "2U1B": {
            "1": "Olecranon",
            "2": "Coronoid"
        },
        "2U1C": {
            "3": "Olecranon és coronoid"
        },
        "2U2A": {
            "1": "Spirális",
            "2": "Ferde (≥ 30°)",
            "3": "Keresztirányú (< 30°)"
        },
        "2U2B": {
            "2": "Ép ék",
            "3": "Töredezett ék"
        },
        "2U2C": {
            "2": "Ép szegmentális",
            "3": "Töredezett szegmentális"
        },
        "2U3A": {
            "1": "Styloid process",
            "2": "Egyszerű",
            "3": "Többrészű"
        },
        "2U3B": {
            "1": "Részleges ízületi"
        },
        "2U3C": {
            "1": "Teljes ízületi"
        }
    }
    return [f"{key} - {value}" for key, value in details.get(ao_type, {}).items()]

def neer_classification(sub_sub_reg):
    neer_classes = {
        "Proximalis humerus": {
            "I": "Egy része érintett (<1 cm elmozdulás, <45° szög)",
            "II": "Két része érintett (tuberositas majus/minor törés, nyak törés)",
            "III": "Három része érintett (fej, nyak, tuberositas)",
            "IV": "Négy része érintett (fej, nyak, tuberositas majus és minor)"
        },
        "Distalis humerus": {
            "I": "Medial Epicondyle",
            "II": "Lateral Epicondyle",
            "III": "Capitellum",
            "IV": "Trochlea"
        },
        "Humerus diaphysis": {
            "I": "Spirális törés",
            "II": "Ferde törés",
            "III": "Keresztirányú törés",
            "IV": "Komplex törés"
        },
        "Proximalis femur": {
            "I": "Subcapitalis törés",
            "II": "Transcervicalis törés",
            "III": "Basicervicalis törés",
            "IV": "Intertrochanterikus törés"
        },
        "Distalis femur": {
            "I": "Condylar törés",
            "II": "Intercondylar törés",
            "III": "Supracondylar törés",
            "IV": "Complex törés"
        }
    }

    neer_type = st.selectbox("Neer osztályozás típusa", neer_classes.get(sub_sub_reg, {}).keys())
    neer_description = neer_classes.get(sub_sub_reg, {}).get(neer_type, "")
    
    classification_name = "Neer osztályozás"
    severity = neer_type
    description = neer_description
    
    return classification_name, severity, description

def gartland_classification():
    gartland_types = {
        "I": "Nem elmozdult törés",
        "II": "Elmozdult törés, intakt hátsó cortex",
        "III": "Teljes elmozdult törés, nincs érintkezés a cortikálisok között",
        "IV": "Elmozdult törés instabil minden síkban"
    }
    
    gartland_type = st.selectbox("Gartland osztályozás", gartland_types.keys())
    gartland_description = gartland_types.get(gartland_type, "")
    
    classification_name = "Gartland osztályozás"
    severity = gartland_type
    description = gartland_description
    
    return classification_name, severity, description
