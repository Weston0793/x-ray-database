import streamlit as st
import sqlite3
from sqlite3 import Error
import os
from PIL import Image
import shutil
import uuid

# Ellenőrizzük, hogy az 'images' mappa létezik-e, ha nem, hozzuk létre
if not os.path.exists("images"):
    os.makedirs("images")

# SQLite adatbázis létrehozása
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        st.error(f"Error creating connection: {e}")
        return None

def create_table(conn):
    try:
        sql_create_images_table = """CREATE TABLE IF NOT EXISTS images (
                                        id integer PRIMARY KEY,
                                        patient_id text NOT NULL,
                                        filename text NOT NULL,
                                        type text,
                                        view text,
                                        main_region text,
                                        sub_region text,
                                        age integer,
                                        comment text
                                    );"""
        cur = conn.cursor()
        cur.execute(sql_create_images_table)
        conn.commit()
    except Error as e:
        st.error(f"Error creating table: {e}")

def check_database(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='images';")
        table_exists = cur.fetchone()
        return table_exists is not None
    except Error as e:
        st.error(f"Error checking database: {e}")
        return False

def initialize_database():
    if os.path.exists(database):
        conn = create_connection(database)
        if conn:
            if not check_database(conn):
                conn.close()
                st.info("Existing database seems to be corrupted. Renaming the old database and creating a new one.")
                shutil.move(database, f"{database}.backup")
                conn = create_connection(database)
                if conn:
                    create_table(conn)
                    conn.close()
            else:
                conn.close()
        else:
            st.error("Error! Cannot create the database connection.")
    else:
        conn = create_connection(database)
        if conn:
            create_table(conn)
            conn.close()

database = "images.db"
initialize_database()

# Egyedi beteg azonosító létrehozása
def generate_patient_id():
    return str(uuid.uuid4())

# Kép mentése
def save_image(patient_id, file, type, view, main_region, sub_region, age, comment):
    filename = file.name
    file_path = os.path.join("images", filename)
    try:
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        conn = create_connection(database)
        if conn:
            try:
                sql = '''INSERT INTO images(patient_id, filename, type, view, main_region, sub_region, age, comment)
                         VALUES(?,?,?,?,?,?,?,?)'''
                cur = conn.cursor()
                cur.execute(sql, (patient_id, filename, type, view, main_region, sub_region, age, comment))
                conn.commit()
            except Error as e:
                st.error(f"Error saving image data to database: {e}")
            finally:
                conn.close()
    except PermissionError as e:
        st.error(f"Permission error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

# Streamlit alkalmazás
st.title("Kép feltöltése és címkézése")

# Beteg azonosító létrehozása vagy kiválasztása
patient_id = st.text_input("Beteg azonosító (hagyja üresen új beteg esetén)", generate_patient_id())

uploaded_file = st.file_uploader("Válassz egy képet", type=["jpg", "jpeg", "png"])

# Típus kiválasztása
type = st.selectbox("Típus", ["Törött", "Normál", "Egyéb"])
if type == "Egyéb":
    type_comment = st.text_input("Specifikálás (Egyéb)")
else:
    type_comment = ""

# Nézet kiválasztása
view = st.selectbox("Nézet", ["AP", "Lateral", "Egyéb"])
if view == "Egyéb":
    view_comment = st.text_input("Specifikálás (Egyéb Nézet)")
else:
    view_comment = ""

# Fő régió kiválasztása
main_region = st.selectbox("Fő régió", ["Felső végtag", "Alsó végtag", "Gerinc", "Koponya"])

# Alrégió kiválasztása
if main_region == "Felső végtag":
    sub_region = st.selectbox("Alrégió", ["Váll", "Felkar", "Könyök", "Alkar", "Csukló", "Kéz", "Clavicula", "Scapula", "Ulna", "Radius"])
elif main_region == "Alsó végtag":
    sub_region = st.selectbox("Alrégió", ["Csípő", "Comb", "Térd", "Tibia", "Fibula", "Boka", "Láb"])
elif main_region == "Gerinc":
    sub_region = st.selectbox("Alrégió", ["Nyaki", "Háti", "Ágyéki", "Kereszt- és farokcsonti"])
elif main_region == "Koponya":
    sub_region = st.selectbox("Alrégió", ["Arckoponya", "Agykoponya", "Állkapocs"])
else:
    sub_region = ""

age = st.number_input("Életkor", min_value=0, max_value=120, step=1, format="%d", key="age", value=0)
comment = st.text_area("Megjegyzés", key="comment", value="")

if st.button("Feltöltés"):
    if uploaded_file and type and view and main_region and sub_region:
        try:
            full_comment = comment + " " + type_comment + " " + view_comment
            save_image(patient_id, uploaded_file, type, view, main_region, sub_region, age, full_comment)
            st.success("Kép sikeresen feltöltve!")
        except Exception as e:
            st.error(f"Hiba a kép mentésekor: {e}")
    else:
        st.error("Tölts fel egy képet és add meg a szükséges információkat.")

# Keresés és megjelenítés
st.header("Képek keresése")
search_labels = st.text_input("Keresés címkék alapján (vesszővel elválasztva)")

# Típus kiválasztása kereséshez
search_type = st.selectbox("Típus keresése", ["", "Törött", "Normál"])

# Nézet kiválasztása kereséshez
search_view = st.selectbox("Nézet keresése", ["", "AP", "Lateral"])

# Fő régió kiválasztása kereséshez
search_main_region = st.selectbox("Fő régió keresése", ["", "Felső végtag", "Alsó végtag", "Gerinc", "Koponya"])

# Alrégió kiválasztása kereséshez
if search_main_region == "Felső végtag":
    search_sub_region = st.selectbox("Alrégió keresése", ["", "Váll", "Felkar", "Könyök", "Alkar", "Csukló", "Kéz", "Clavicula", "Scapula", "Ulna", "Radius"])
elif search_main_region == "Alsó végtag":
    search_sub_region = st.selectbox("Alrégió keresése", ["", "Csípő", "Comb", "Térd", "Tibia", "Fibula", "Boka", "Láb"])
elif search_main_region == "Gerinc":
    search_sub_region = st.selectbox("Alrégió keresése", ["", "Nyaki", "Háti", "Ágyéki", "Kereszt- és farokcsonti"])
elif search_main_region == "Koponya":
    search_sub_region = st.selectbox("Alrégió keresése", ["", "Arckoponya", "Agykoponya", "Állkapocs"])
else:
    search_sub_region = ""

if st.button("Keresés"):
    conn = create_connection(database)
    if conn:
        try:
            cur = conn.cursor()
            query = "SELECT filename, type, view, main_region, sub_region FROM images WHERE 1=1"
            values = []
            if search_labels:
                for label in search_labels.split(","):
                    query += " AND (type LIKE ? OR view LIKE ? OR main_region LIKE ? OR sub_region LIKE ?)"
                    values.extend([f"%{label.strip()}%", f"%{label.strip()}%", f"%{label.strip()}%", f"%{label.strip()}%"])
            if search_type:
                query += " AND type = ?"
                values.append(search_type)
            if search_view:
                query += " AND view = ?"
                values.append(search_view)
            if search_main_region:
                query += " AND main_region = ?"
                values.append(search_main_region)
            if search_sub_region:
                query += " AND sub_region = ?"
                values.append(search_sub_region)

            cur.execute(query, values)
            rows = cur.fetchall()
            for i, row in enumerate(rows[:10]):  # Csak az első 10 kép megjelenítése
                st.image(os.path.join("images", row[0]), caption=f"{row[1]}, {row[2]}, {row[3]}, {row[4]}")
            if len(rows) > 10:
                st.info(f"Összesen {len(rows)} kép található. Kérjük, szűkítse a keresést.")
        except Error as e:
            st.error(f"Hiba a keresés közben: {e}")
        finally:
            conn.close()
    else:
        st.error("Cannot connect to the database.")

# Számláló készítése
def get_counts(conn):
    counts = {
        "Felső végtag": {"Váll": {}, "Felkar": {}, "Könyök": {}, "Alkar": {}, "Csukló": {}, "Kéz": {}, "Clavicula": {}, "Scapula": {}, "Ulna": {}, "Radius": {}},
        "Alsó végtag": {"Csípő": {}, "Comb": {}, "Térd": {}, "Tibia": {}, "Fibula": {}, "Boka": {}, "Láb": {}},
        "Gerinc": {"Nyaki": {}, "Háti": {}, "Ágyéki": {}, "Kereszt- és farokcsonti": {}},
        "Koponya": {"Arckoponya": {}, "Agykoponya": {}, "Állkapocs": {}}
    }
    views = ["AP", "Lateral"]
    types = ["Normál", "Törött"]

    for main_region in counts:
        for sub_region in counts[main_region]:
            for view in views:
                for type in types:
                    cur = conn.cursor()
                    cur.execute(f"SELECT COUNT(*) FROM images WHERE main_region=? AND sub_region=? AND view=? AND type=?", 
                                (main_region, sub_region, view, type))
                    count = cur.fetchone()[0]
                    total = 50  # Maximum 50 kép szükséges minden kombinációból
                    percentage = (count / total) * 100
                    counts[main_region][sub_region][f"{type}_{view}"] = percentage

    return counts

conn = create_connection(database)
if conn:
    counts = get_counts(conn)
    for main_region, sub_regions in counts.items():
        st.subheader(main_region)
        for sub_region, view_types in sub_regions.items():
            st.text(sub_region)
            cols = st.columns(2)  # Csak az AP és Lateral nézeteket jelenítjük meg
            for i, (view_type, percentage) in enumerate(view_types.items()):
                color = "normal" if percentage >= 100 else "inverse"
                cols[i % 2].metric(view_type, f"{percentage:.2f}%", delta_color=color)
    conn.close()
else:
    st.error("Cannot connect to the database.")
