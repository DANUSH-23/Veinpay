import streamlit as st
from pymongo import MongoClient
from config import MONGO_URI
import pandas as pd

def show_analytics_page():
    st.markdown("<div class='page-title'>Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Live database analytics from MongoDB.</div>", unsafe_allow_html=True)

    client = MongoClient(MONGO_URI)
    db = client["veinpay_db"]
    users = db["users"]

    total = users.count_documents({})
    with_embed = users.count_documents({"embedding": {"$exists": True}})

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Total Users", total)
    col2.metric("Users with Embeddings", with_embed)

    st.markdown("---")

    # recent 10 users
    data = list(users.find({}, {"_id": 0}).sort("_id", -1).limit(10))
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No users found in database.")

    st.markdown("</div>", unsafe_allow_html=True)
