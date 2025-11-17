import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="VeinPay • Biometrics",
    page_icon="🖐️",
    layout="wide"
)

# Inject custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Home", "Register", "Match"],
        icons=["house", "person-plus", "fingerprint"],
        menu_icon="cast",
        default_index=0,
    )

# ---------------- HOME PAGE ----------------
if selected == "Home":
    st.markdown("<h1 style='text-align:center;'>🖐️ VeinPay</h1>", unsafe_allow_html=True)

    st.markdown("""
        <h3 style="text-align:center; color:gray;">
            Next-Gen Contactless Vein Authentication using AI + MobileNetV2
        </h3>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("""
        **VeinPay** uses near-infrared vein patterns and AI embeddings  
        for high-security, frictionless, spoof-resistant authentication  
        designed for:
        - Payments  
        - Access Control  
        - Identity Verification  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fd1sr9z1pdl3mb7.cloudfront.net%2Fwp-content%2Fuploads%2F2025%2F09%2F09152614%2Flotte-palm-vein-pay-1024x683.jpg&f=1&nofb=1&ipt=eb88899a9d6806093d5c55ad6ec70f37ca722567d9b8a794d1a5e012f01b7b02", use_container_width=True)
