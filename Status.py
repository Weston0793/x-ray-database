import streamlit as st
from firebase_helpers import get_counts, get_progress_summary
import uuid
import sqlite3
import time

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
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="tracker-title">Státusz követése</div>', unsafe_allow_html=True)

    counts, data = get_counts()
    summary = get_progress_summary(counts)

    # Calculate grand total progress correctly
    total_done = 0
    for region in summary:
        total_done += summary[region]["progress"]

    total_tasks = 4600  # Set the total number of tasks to 4600 as required

    if total_tasks > 0:
        grand_total_progress = (total_done / total_tasks) * 100
    else:
        grand_total_progress = 0

    st.markdown(f"**Fázis 1 Státusz: {total_done}/{int(total_tasks)} ({int(grand_total_progress)}%)**")
    st.progress(grand_total_progress / 100)

    # Region and subregion progress
    for main_region, sub_regions in counts.items():
        main_done = summary[main_region]["progress"]
        main_total_tasks = len(sub_regions) * 200  # Each subregion should have 200 tasks in total
        if main_total_tasks > 0:
            main_progress = (main_done / main_total_tasks) * 100
        else:
            main_progress = 0

        st.subheader(main_region)
        st.markdown(f"**{main_region} Státusz: {main_done}/{main_total_tasks} ({int(main_progress)}%)**")
        st.progress(main_progress / 100)  # st.progress expects a value between 0 and 1
        
        for sub_region, view_types in sub_regions.items():
            sub_done = sum(view_types.values())
            sub_total_tasks = 200  # Each subregion has 200 tasks
            if sub_total_tasks > 0:
                sub_progress = (sub_done / sub_total_tasks) * 100
            else:
                sub_progress = 0

            st.markdown(f"**{sub_region} Státusz: {sub_done}/{sub_total_tasks} ({int(sub_progress)}%)**")
            st.progress(sub_progress / 100)  # st.progress expects a value between 0 and 1
            
            for view_type, count in view_types.items():
                percentage = (count / 200) * 100  # Assuming each subregion has 200 tasks
                if count > 0:
                    st.markdown(f"{view_type}: {count}/200 ({int(percentage)}%)")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
