import streamlit as st
from firebase_helpers import initialize_firebase, save_comment, get_comments
import random
import datetime
from Styles import contact_background

# Ensure Firebase is initialized
initialize_firebase()

def generate_funny_name():
    first_parts = ["Fluffy", "Sparkly", "Wiggly", "Silly", "Funky", "Giggles", "Cheery", "Dizzy", "Bouncy", "Jumpy",
                   "Zippy", "Snazzy", "Bubbly", "Quirky", "Jolly", "Peppy", "Giddy", "Chirpy", "Frisky", "Perky",
                   "Whizzy", "Fizzy", "Nifty", "Ducky", "Zappy", "Chipper", "Jazzy", "Snappy", "Zany"]
    second_parts = ["Penguin", "Banana", "Unicorn", "Muffin", "Pickle", "Cupcake", "Bunny", "Monkey", "Noodle", "Puppy",
                    "Sprout", "Pancake", "Mango", "Gizmo", "Taco", "Bubble", "Pudding", "Doodle", "Coconut", "Waffle",
                    "Marshmallow", "Pepper", "Sundae", "Snickers", "Button", "Tinker", "Pebble", "Cookie", "Biscuit"]
    return f"{random.choice(first_parts)} {random.choice(second_parts)}"

def main():
    contact_background()
    
    st.markdown('<h1 class="title">Elérhetőség</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="content">
        <p><strong>Email:</strong> aba.lorincz@gmail.com</p>
        <p><strong>Telefon:</strong> +36 30 954 2176</p>
        <p><strong>Cím:</strong> Thermophysiologia Tanszék, Transzlációs Medicina Intézet, Általános Orvostudományi Kar, Pécsi Tudományegyetem, Szigeti utca 12, 7624 Pécs, Hungary</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="subheader">Kommentszekció</h2>', unsafe_allow_html=True)
    
    if 'name' not in st.session_state:
        st.session_state.name = generate_funny_name()

    col1, col2 = st.columns([4, 1])
    with col1:
        name = st.text_input("Név", value=st.session_state.name)
    with col2:
        if st.button("Új nevet kérek!"):
            with st.spinner('Generating a new name...'):
                st.session_state.name = generate_funny_name()
                name = st.session_state.name

    comment = st.text_area("Komment")

    if st.button("Küldés"):
        if comment:
            with st.spinner('Saving your comment...'):
                save_comment(name, comment)
            st.success("Köszönjük a hozzászólást!", icon="✅")
        else:
            st.error("A komment mező nem lehet üres!", icon="❌")

    st.markdown('<h3 class="subsubheader">Legutóbbi Kommentek</h3>', unsafe_allow_html=True)
    
    if 'page' not in st.session_state:
        st.session_state.page = 0

    page = st.session_state.page
    comments = get_comments(page * 2, 2)

    if comments:
        for c in comments:
            timestamp = c['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            st.markdown(f"<div class='content'><strong>{c['name']}</strong>: {c['comment']} <em>(Posted on: {timestamp})</em></div>", unsafe_allow_html=True)
    else:
        st.write("Nincsenek kommentek.")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("<< Előző", key="prev"):
            if page > 0:
                st.session_state.page -= 1
    with col2:
        st.write(f"Oldal: {page + 1}")
    with col3:
        if st.button("Következő >>", key="next"):
            if len(comments) == 2:
                st.session_state.page += 1

if __name__ == "__main__":
    main()
