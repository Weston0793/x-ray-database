import streamlit as st

class MultiPage:
    def __init__(self):
        self.pages = []

    def add_page(self, title, func, icon=None):
        self.pages.append({
            "title": title,
            "function": func,
            "icon": icon
        })

    def run(self):
        st.sidebar.markdown("<h2 style='text-align: center;'>Navigáció</h2>", unsafe_allow_html=True)
        selected_page = st.sidebar.selectbox(
            '',
            self.pages,
            format_func=lambda page: f"{page['icon']} {page['title']}" if page['icon'] else page['title']
        )
        selected_page['function']()
