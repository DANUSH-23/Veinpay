import streamlit as st
from register_page import show_register_page
from match_page import show_match_page
from utils import show_analytics_page

# Streamlit Page Config
st.set_page_config(
    page_title="VeinPay",
    layout="wide",
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# -------------------------------------------------------
# HOME PAGE CONTENT
# -------------------------------------------------------
def show_home_page():
    # Title
    st.markdown("<div class='page-title'>VeinPay</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='sub-text'>
            Secure, next-generation biometric payment authentication powered by AI.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ---------------- GLASS CARD ----------------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <h2 class='section-header'>Overview</h2>

        <p>
            VeinPay is a next-generation biometric payment authentication platform designed 
            to eliminate the need for physical cards, cash, smartphones, or PINs. It leverages 
            palm-vein recognition — one of the most secure and forgery-proof biometric 
            modalities — to enable instant, contactless and private identity verification.
        </p>

        <p>
            Using near-infrared (NIR) imaging, the system captures and analyzes unique vein 
            structures beneath the skin. These sub-dermal patterns require live blood flow and 
            cannot be photographed, duplicated, stolen, or forged — making VeinPay inherently 
            secure and highly reliable.
        </p>

        <h2 class='section-header'>How It Addresses the Problem</h2>

        <table class='comparison-table'>
            <tr>
                <th>Existing Issue</th>
                <th>VeinPay Solution</th>
            </tr>
            <tr>
                <td>Cards and phones can be lost, stolen or cloned</td>
                <td>Internal vein biometrics cannot be copied or forged</td>
            </tr>
            <tr>
                <td>Fraud through PIN theft or card skimming</td>
                <td>Eliminates physical credentials and PIN dependence</td>
            </tr>
            <tr>
                <td>Slow or unreliable authentication systems</td>
                <td>AI-based embedding + optimized processing ensures instant verification</td>
            </tr>
            <tr>
                <td>Traditional systems risk privacy breaches</td>
                <td>Decentralized storage + encryption protect sensitive data</td>
            </tr>
        </table>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ---------------- TECHNOLOGIES GLASS CARD ----------------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        <h2 class='section-header'>Technologies Used</h2>

        <ul>
            <li><b>FastAPI</b> backend</li>
            <li><b>TensorFlow MobileNetV2</b> for embedding extraction</li>
            <li><b>OpenCV + scikit-image</b> for preprocessing and vein extraction</li>
            <li><b>MongoDB</b> for user embedding storage</li>
            <li><b>Streamlit</b> as the UI layer</li>
            <li><b>Docker</b> (optional) for MongoDB local instance</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Register", "Match", "Analytics"],
)


# -------------------------------------------------------
# PAGE ROUTING LOGIC
# -------------------------------------------------------
if menu == "Home":
    show_home_page()

elif menu == "Register":
    show_register_page()

elif menu == "Match":
    show_match_page()

elif menu == "Analytics":
    show_analytics_page()
