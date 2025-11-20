# streamlit_app/app.py

import streamlit as st
from register_page import show_register_page
from match_page import show_match_page
from utils import show_analytics_page

# Must be first Streamlit call
st.set_page_config(
    page_title="VeinPay",
    layout="wide",
)


# Load custom CSS
def load_css():
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("styles.css not found. Using default Streamlit styling.")


load_css()


def show_home_page():
    st.markdown("<div class='page-title'>VeinPay</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='sub-text'>
            Contactless palm vein–based authentication designed to replace cards, cash and PINs 
            with secure, internal biometrics.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        <h2 class='section-header'>Overview</h2>
        <p>
            VeinPay is a biometric authentication system that uses sub-dermal palm vein patterns 
            instead of cards, phones, or PINs. Vein patterns are internal to the body and require 
            live blood flow, making them extremely hard to forge or steal.
        </p>

        <p>
            In this MVP, we implemented a full software stack: image preprocessing, deep feature 
            extraction using MobileNetV2, similarity-based matching, secure embedding storage in 
            MongoDB, and a modern Streamlit-based dashboard.
        </p>

        <h2 class='section-header'>How It Addresses the Problem</h2>
        <table class='comparison-table'>
            <tr>
                <th>Existing Issue</th>
                <th>VeinPay Solution</th>
            </tr>
            <tr>
                <td>Cards and phones can be lost, stolen or cloned.</td>
                <td>Vein patterns are internal and require live blood flow, making them inherently secure.</td>
            </tr>
            <tr>
                <td>Fraud through PIN theft or card skimming.</td>
                <td>No PINs or physical credentials are required.</td>
            </tr>
            <tr>
                <td>Unreliable or slow authentication flows.</td>
                <td>MobileNetV2-based embeddings provide fast, accurate similarity scoring.</td>
            </tr>
            <tr>
                <td>Privacy risks when storing raw biometric images.</td>
                <td>We store only feature embeddings, not raw images, preserving privacy.</td>
            </tr>
        </table>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        <h2 class='section-header'>Technologies Used</h2>
        <ul>
            <li><b>FastAPI</b> for high-performance backend APIs</li>
            <li><b>TensorFlow MobileNetV2</b> for deep feature embeddings</li>
            <li><b>OpenCV</b> and <b>scikit-image</b> for preprocessing and vein enhancement</li>
            <li><b>MongoDB</b> for secure embedding storage</li>
            <li><b>Streamlit</b> with custom CSS for the user interface</li>
            <li><b>Docker</b> (optional) for MongoDB local deployment</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# Sidebar navigation
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Register", "Match", "Analytics"],
    index=0,
)


if menu == "Home":
    show_home_page()
elif menu == "Register":
    show_register_page()
elif menu == "Match":
    show_match_page()
elif menu == "Analytics":
    show_analytics_page()
