# streamlit_app/utils.py

import streamlit as st
from pymongo import MongoClient
from config import MONGO_URI
import pandas as pd


def get_mongo_client():
    try:
        client = MongoClient(MONGO_URI)
        return client
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {e}")
        return None


def show_analytics_page():
    st.markdown("<div class='page-title'>Analytics</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-text'>Overview of registered users and verification activity.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    client = get_mongo_client()
    if client is None:
        st.error("Could not connect to MongoDB. Check MONGO_URI.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    db = client["veinpay_db"]
    users_collection = db["users"]

    try:
        total_users = users_collection.count_documents({})
        st.metric(label="Total Registered Users", value=total_users)

        # Show last 10 users (if they have user_id field)
        docs = list(users_collection.find({}, {"_id": 0, "user_id": 1, "created_at": 1}).sort("_id", -1).limit(10))
        if docs:
            df = pd.DataFrame(docs)
            st.markdown("<h4 class='section-label'>Recently Registered Users</h4>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No users registered yet.")
    except Exception as e:
        st.error(f"Error reading analytics: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
