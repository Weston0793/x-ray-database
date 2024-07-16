import streamlit as st

class MultiPage:
    def __init__(self):
        self.pages = []

    def add_page(self, title, func):
        self.pages.append({
            "title": title,
            "function": func
        })

    def run(self):
        page = st.sidebar.selectbox(
            'Navigáció',
            self.pages,
            format_func=lambda page: page['title']
        )
        page['function']()
