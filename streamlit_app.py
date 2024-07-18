import streamlit as st
from multipage import MultiPage
from Home import main as home
from Search import search_section as search
from Status import main as status
from Contact import main as contact

app = MultiPage()

# Add all your applications (pages) here
app.add_page("Kép feltöltése", home)
app.add_page("Képek keresése", search)
app.add_page("Státusz", status)
app.add_page("Elérhetőség", contact)

# The main app
app.run()
