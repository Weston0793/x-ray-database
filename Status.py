import streamlit as st
from firebase_helpers import get_counts, get_progress_summary
import sqlite3
import os

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
    for row in data:
        if len(row) >= 5:
            main_region, sub_region, view, type_, count = row[:5]
            try:
                count = int(count)  # Ensure count is an integer
                c.execute('INSERT INTO status (main_region, sub_region, view_type, count, percentage) VALUES (?, ?, ?, ?, ?)', 
                          (main_region, sub_region, f"{type_}_{view}", count, row[5] if len(row) > 5 else 0))
            except ValueError:
                st.error(f"Invalid count value for {main_region}-{sub_region}-{type_}-{view}: {count}")
        else:
            st.error(f"Invalid row data: {row}")
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

def main():
    st.markdown(
        """
        <style>
        .tracker-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            border: 2px solid black;
            padding: 10px;
            margin-bottom: 20px;
        }
        .sub-region-title {
            margin-left: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
        .view-type {
            margin-left: 40px;
            font-style: italic;
        }
        .update-note {
            font-size: 16px;
            text-align: center;
            color: red;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="tracker-title">Státusz követése</div>', unsafe_allow_html=True)
    st.markdown('<div class="update-note">Kérjük, várjon kb. 10 másodpercet a frissítéshez</div>', unsafe_allow_html=True)

    # Check if the local database exists
    if not os.path.exists(DB_PATH):
        create_db()
        data_exists = False
    else:
        data_exists = True

    if st.button('Frissítés') or not data_exists:
        counts, data = get_counts()
        summary = get_progress_summary(counts)
        update_db(data)
        st.success('Adatok frissítve!')
    else:
        counts, summary = fetch_summary_from_db()

    # Calculate grand total progress correctly using count values
    total_done = 0
    total_tasks = 0
    for region in summary:
        for sub_region in summary[region]["subregions"]:
            total_done += summary[region]["subregions"][sub_region]["count"]
            total_tasks += 200  # Each subregion has 200 tasks

    if total_tasks > 0:
        grand_total_progress = (total_done / total_tasks) * 100
    else:
        grand_total_progress = 0

    st.markdown(f"**Fázis 1 Státusz: {total_done}/{int(total_tasks)} ({grand_total_progress:.1f}%)**")
    st.progress(grand_total_progress / 100)

    # Region and subregion progress
    for main_region, sub_regions in counts.items():
        main_done = sum(summary[main_region]["subregions"][sub]["count"] for sub in sub_regions)  # Use count instead of progress
        main_total_tasks = len(sub_regions) * 200  # Each subregion should have 200 tasks in total
        if main_total_tasks > 0:
            main_progress = (main_done / main_total_tasks) * 100
        else:
            main_progress = 0

        st.subheader(main_region)
        st.markdown(f"**{main_region} Státusz: {main_done}/{main_total_tasks} ({main_progress:.1f}%)**")
        st.progress(main_progress / 100)  # st.progress expects a value between 0 and 1
        
        for sub_region, view_types in sub_regions.items():
            sub_done = sum(view_types.values())
            sub_total_tasks = 200  # Each subregion has 200 tasks
            if sub_total_tasks > 0:
                sub_progress = (sub_done / sub_total_tasks) * 100
            else:
                sub_progress = 0

            st.markdown(f"**{sub_region} Státusz: {sub_done}/{sub_total_tasks} ({sub_progress:.1f}%)**")
            st.progress(sub_progress / 100)  # st.progress expects a value between 0 and 1
            
            for view_type, count in view_types.items():
                percentage = (count / 50) * 100  # Assuming each view type within a subregion has 50 tasks
                st.markdown(f"{view_type}: {count}/50 ({percentage:.1f}%)")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
