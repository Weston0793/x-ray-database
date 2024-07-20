import streamlit as st
from firebase_helpers import initialize_firebase, save_comment, get_comments
import random

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
    st.title("Elérhetőség")

    st.write("""
    ### Kapcsolat
    - **Email:** aba.lorincz@gmail.com
    - **Telefon:** +36 30 954 2176
    - **Cím:** Department of Thermophysiology, Institute for Translational Medicine, Medical School, University of Pécs, 12 Szigeti Street, 7624 Pécs, Hungary
    """)

    st.write("### Kommentek")
    
    if 'name' not in st.session_state:
        st.session_state.name = generate_funny_name()

    col1, col2 = st.columns([4, 1])
    with col1:
        name = st.text_input("Név", value=st.session_state.name)
    with col2:
        if st.button("Új nevet kérek!"):
            st.session_state.name = generate_funny_name()
            name = st.session_state.name

    comment = st.text_area("Komment")

    if st.button("Küldés"):
        if comment:
            save_comment(name, comment)
            st.success("Köszönjük a hozzászólást!")
        else:
            st.error("A komment mező nem lehet üres!")

    # Display last comments with navigation
    st.write("### Legutóbbi Kommentek")
    
    if 'page' not in st.session_state:
        st.session_state.page = 0

    page = st.session_state.page
    comments = get_comments(page * 2, 2)

    if comments:
        for c in comments:
            st.write(f"**{c['name']}**: {c['comment']}")
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
