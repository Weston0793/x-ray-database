import streamlit as st
import sqlite3
from firebase_helpers import get_counts, get_progress_summary

DB_PATH = 'status.db'

def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY,
            main_region TEXT,
            sub_region TEXT,
            view_type TEXT,
            count INTEGER,
            percentage REAL
        )
    ''')
    conn.commit()
    conn.close()

def update_db(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM status')  # Clear the table before inserting new data

    all_combinations = []
    main_regions = {
        "Felső végtag": ["Váll", "Humerus", "Könyök", "Alkar", "Csukló", "Kéz"],
        "Alsó végtag": ["Medence", "Pelvis", "Femur", "Térd", "Lábszár", "Boka", "Láb"],
        "Gerinc": ["Cervicalis", "Thoracalis", "Lumbaris", "Sacralis", "Coccygealis"],
        "Koponya": ["Arckoponya", "Agykoponya", "Mandibula"],
        "Mellkas": ["Borda", "Sternum"]
    }
    views = ["AP", "Lateral"]
    main_types = ["Normál", "Törött"]

    for main_region, sub_regions in main_regions.items():
        for sub_region in sub_regions:
            for view in views:
                for main_type in main_types:
                    all_combinations.append((main_region, sub_region, view, main_type, 0))

    for row in data:
        if len(row) >= 5:
            main_region, sub_region, view, main_type, count = row[:5]
            for i, combo in enumerate(all_combinations):
                if combo[:4] == (main_region, sub_region, view, main_type):
                    all_combinations[i] = (main_region, sub_region, view, main_type, count)
                    break

    for combo in all_combinations:
        main_region, sub_region, view, main_type, count = combo
        try:
            count = int(count)  # Ensure count is an integer
            c.execute('INSERT INTO status (main_region, sub_region, view_type, count, percentage) VALUES (?, ?, ?, ?, ?)', 
                      (main_region, sub_region, f"{main_type}_{view}", count, 0))
        except ValueError:
            st.error(f"Invalid count value for {main_region}-{sub_region}-{main_type}-{view}: {count}")

    conn.commit()
    conn.close()

def fetch_from_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT main_region, sub_region, view_type, count FROM status')
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_summary_from_db():
    rows = fetch_from_db()
    counts = {}
    for row in rows:
        main_region = row[0]
        sub_region = row[1]
        view_type = row[2]
        count = row[3]
        try:
            count = int(count)  # Ensure count is an integer
            if main_region not in counts:
                counts[main_region] = {}
            if sub_region not in counts[main_region]:
                counts[main_region][sub_region] = {}
            counts[main_region][sub_region][view_type] = count
        except ValueError:
            st.error(f"Invalid count value in database for {main_region}-{sub_region}-{view_type}: {count}")
    summary = get_progress_summary(counts)
    return counts, summary
