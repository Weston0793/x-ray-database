import streamlit as st

def home_background():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        .stApp {
            background: linear-gradient(to bottom right, #f0f4f7, #d9e2ec);
            background-attachment: fixed;
            color: #212121;
            font-family: 'Roboto', sans-serif;
        }
        .title {
            font-size: 48px;
            font-weight: 700;
            color: #ffffff;
            text-align: center;
            padding: 20px;
            background: rgba(0, 150, 136, 0.8);
            border-radius: 10px;
            margin-top: 5px;
            text-shadow: 2px 2px 4px #000000;
            animation: fadeInDown 1.5s;
        }
        .subheader {
            font-size: 28px;
            color: #ffffff;
            background: #00796B;
            padding: 5px;
            border-radius: 10px;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        .subsubheader {
            font-size: 22px;
            color: #ffffff;
            background: #004D40;
            padding: 8px;
            border-radius: 8px;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        .content {
            font-size: 16px;
            line-height: 1.2;
            text-align: justify;
            margin: 5px;
            padding: 5px;
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .content ul {
            margin-left: 20px;
        }
        .content li {
            margin-bottom: 10px;
        }
        .content p {
            margin-bottom: 10px;
        }
        .content a {
            color: #00796B;
            text-decoration: none;
        }
        .content a:hover {
            text-decoration: underline;
        }
        @keyframes fadeInDown {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes fadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
def upload_markdown():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        .stApp {
            background: linear-gradient(to bottom right, #f0e6eb, #d9c2cc);
            background-attachment: fixed;
            color: #333333;
            font-family: 'Roboto', sans-serif;
        }
        .upload-title {
            font-size: 36px;
            font-weight: 700;
            color: #ffffff;
            text-align: center;
            padding: 15px;
            background: rgba(128, 0, 64, 0.8);
            border-radius: 8px;
            margin-top: 5px;
            text-shadow: 1px 1px 3px #000000;
            animation: fadeInDown 1.5s;
        }
        .file-upload-instruction {
            font-size: 16px;
            color: #ffffff;
            background: #800040;
            padding: 5px;
            border-radius: 8px;
            margin-top: 5px;
            margin-bottom: 5px;
            text-align: center;
        }
        .confirmation-box {
            background: #f5f5f5;
            border-radius: 5px;
            padding: 5px;
            margin-top: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .confirmation-title {
            font-size: 24px;
            font-weight: 700;
            color: #333333;
            margin-bottom: 10px;
        }
        .center-button {
            text-align: center;
            margin-top: 5px;
        }
        .content {
            font-size: 14px;
            line-height: 1.2;
            text-align: justify;
            margin: 5px;
            padding: 5px;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .content ul {
            margin-left: 5px;
        }
        .content li {
            margin-bottom: 5px;
        }
        .content p {
            margin-bottom: 5px;
        }
        .content a {
            color: #800040;
            text-decoration: none;
        }
        .content a:hover {
            text-decoration: underline;
        }
        .highlight {
            background: #800040;
            color: white;
            padding: 5px;
            border-radius: 5px;
        }
        .checkbox-container label {
            font-weight: bold;
            font-size: 16px;
            color: #800040;
        }
        .stButton button {
            background-color: #800040;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 5px 5px;
            border-radius: 8px;
            text-align: center;
            display: block;
            margin: 5px auto;
            width: 70%;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #4b0029;
        }
        .stTextInput input, .stFileUploader div, .stTextArea textarea {
            font-size: 16px;
            padding: 5px;
            border-radius: 8px;
            border: 1px solid #800040;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        @keyframes fadeInDown {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes fadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def search_markdown():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        .stApp {
            background: linear-gradient(to bottom right, #cdebad, #cdebad);
            background-attachment: fixed;
            color: #333333;
            font-family: 'Roboto', sans-serif;
        }
        .search-title {
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            color: #ffffff;
            background-color: #013208;
            padding: 15px;
            margin-bottom: 5px;
            border-radius: 8px;
            text-shadow: 1px 1px 2px #000000;
            animation: fadeInDown 1.5s;
        }
        .result-image {
            border: 1px solid #007BFF;
            border-radius: 5px;
            padding: 5px;
            margin-bottom: 10px;
        }
        .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 10px 0;
        }
        .button-container button {
            font-size: 18px;
            font-weight: bold;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 8px;
            background-color: #66B2FF; /* Lighter Blue */
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .button-container button:hover {
            background-color: #3399FF;
        }
        .formatted-data {
            font-family: 'Roboto', sans-serif;
            line-height: 1.5;
            color: #333;
            background: #f0f4f7;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            animation: fadeIn 1.5s;
        }
        .formatted-data h4 {
            margin-top: 10px;
            margin-bottom: 5px;
            color: #007BFF;
        }
        .formatted-data p {
            margin: 0;
            padding: 0;
        }
        @keyframes fadeInDown {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes fadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
def status_markdown():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        .stApp {
            background: linear-gradient(to bottom right, #e0e0e0, #f5f5f5);
            background-attachment: fixed;
            color: #333333;
            font-family: 'Roboto', sans-serif;
        }
        .tracker-title {
            font-size: 36px;
            font-weight: 700;
            color: #ffffff;
            text-align: center;
            padding: 15px;
            background: rgba(35, 47, 62, 0.9); /* Navy */
            border-radius: 5px;
            margin-top: 5px;
            text-shadow: 1px 1px 3px #000000;
            animation: fadeInDown 1.5s, pulse 2s infinite;
        }
        .update-note {
            font-size: 18px;
            color: #ffffff;
            text-align: center;
            background: #593b4a ; /* Burgundy */
            padding: 5px;
            border-radius: 5px;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        .grand-total {
            font-size: 28px;
            color: #ffffff;
            background: #233d3e; /* Gold */
            padding: 15px;
            border-radius: 5px;
            margin-top: 5px;
            margin-bottom: 5px;
            text-align: center;
            font-weight: bold;
        }
        .subheader {
            font-size: 20px;
            color: #ffffff;
            background: #5e6b7c; /* Medium navy */
            padding: 8px;
            border-radius: 5px;
            margin-top: 10px;
            margin-bottom: 5px;
            text-align: center;
        }
        .subsubheader {
            font-size: 18px;
            color: #ffffff;
            background: #3b4a59; /* Dark navy */
            padding: 6px;
            border-radius: 5px;
            margin-top: 5px;
            margin-bottom: 5px;
            text-align: center;
        }
        .content {
            font-size: 14px;
            line-height: 1.4;
            text-align: justify;
            margin: 1px;
            padding: 1px;
            background: #ffffff;
            border-radius: 2px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .content ul {
            margin-left: 15px;
        }
        .content li {
            margin-bottom: 8px;
        }
        .content p {
            margin-bottom: 8px;
        }
        .content a {
            color: #8b572a; /* Gold */
            text-decoration: none;
        }
        .content a:hover {
            text-decoration: underline;
        }
        .hover-effect:hover {
            color: #5e6b7c; /* Medium navy */
            transform: scale(1.05);
        }
        .stButton button {
            background-color: #593b4a ; /* Burgundy */
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 8px 8px;
            border-radius: 5px;
            text-align: center;
            display: block;
            margin: 10px auto;
            width: 30%;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #6a451f; /* Darker gold */
        }
        .stTextInput input, .stFileUploader div, .stTextArea textarea {
            font-size: 14px;
            padding: 6px;
            border-radius: 5px;
            border: 1px solid #8b572a; /* Gold */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        @keyframes fadeInDown {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes pulse {
            0%, 100% {
                transform: scale(1); /* Baseline */
            }
            20% {
                transform: scale(0.95); /* Small contraction - atrial systole */
            }
            40% {
                transform: scale(0.85); /* Big contraction - ventricular systole */
            }
        }

        @keyframes fadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def contact_background():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        .stApp {
            background: linear-gradient(to bottom right, #e0eafc, #cfdef3);
            background-attachment: fixed;
            color: #333333;
            font-family: 'Roboto', sans-serif;
        }
        .title {
            font-size: 48px;
            font-weight: 700;
            color: #ffffff;
            text-align: center;
            padding: 20px;
            background: rgba(103, 58, 183, 0.8);
            border-radius: 10px;
            margin-top: 5px;
            text-shadow: 2px 2px 4px #000000;
            animation: fadeInDown 1.5s;
        }
        .subheader {
            font-size: 28px;
            color: #ffffff;
            background: #673AB7;
            padding: 10px;
            border-radius: 10px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .subsubheader {
            font-size: 22px;
            color: #ffffff;
            background: #4527A0;
            padding: 8px;
            border-radius: 8px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .content {
            font-size: 16px;
            line-height: 1.2;
            text-align: justify;
            margin: 10px;
            padding: 10px;
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .content ul {
            margin-left: 10px;
        }
        .content li {
            margin-bottom: 10px;
        }
        .content p {
            margin-bottom: 10px;
        }
        .content a {
            color: #673AB7;
            text-decoration: none;
        }
        .content a:hover {
            text-decoration: underline;
        }
        @keyframes fadeInDown {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes fadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
