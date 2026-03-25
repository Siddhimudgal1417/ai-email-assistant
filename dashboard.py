import streamlit as st
import os
import sys
from datetime import datetime

# Add src to path for backend imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from gmail_service import get_unread_emails
from agent import process_email_with_ai

# 1. Page Configuration
st.set_page_config(
    page_title="Executive AI | Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Performance Optimization: Caching
# This prevents 429 Rate Limit errors by storing AI results in memory
@st.cache_data(show_spinner=False, ttl=3600)
def get_cached_ai_result(body):
    return process_email_with_ai(body)

# 3. Custom CSS for Dark Mode
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #1e2130;
        border: 1px solid #4a90e2;
        padding: 15px;
        border-radius: 12px;
    }
    [data-testid="stMetricLabel"] { color: #9ea4b0 !important; font-weight: bold; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }
    .stExpander {
        border: 1px solid #343746 !important;
        background-color: #161b22 !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar
with st.sidebar:
    st.title("⚙️ Control Center")
    st.write("System: **v1.1.0-stable**")
    st.divider()
    
    if st.button("🔄 Sync Inbox", use_container_width=True, type="primary"):
        # Clear cache on manual sync to fetch fresh data
        st.cache_data.clear()
        st.rerun()
    
    st.write("---")
    st.caption(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")
    st.caption("Engine: Gemini 2.0 Flash")

# 5. Main UI
st.title("⚡ AI Email Assistant")
st.write("Automated intent extraction and scheduling.")

# Fetch Emails
emails = get_unread_emails()
num_unread = len(emails)

# Metrics Row
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("Unread", num_unread)
with col_m2:
    st.metric("Status", "Active", "Free Tier")
with col_m3:
    st.metric("Quota", "Optimized", "Cached")

st.divider()

# 6. Content Logic
if not emails:
    st.balloons()
    st.success("🎉 **Inbox Zero!** You are all caught up.")
else:
    st.subheader(f"📬 Pending Analysis ({num_unread})")
    
    for msg in emails:
        with st.expander(f"✉️ {msg['subject']} — from {msg['sender']}"):
            col_body, col_ai = st.columns([1, 1])
            
            with col_body:
                st.markdown("**Original Email:**")
                st.info(msg['body'] if msg['body'] else "*(Empty Body)*")
            
            with col_ai:
                st.markdown("**AI Interpretation:**")
                
                # Check if body exists before calling AI
                if msg['body']:
                    with st.spinner("Analyzing..."):
                        # Use the CACHED function here
                        result = get_cached_ai_result(msg['body'])
                    
                    intent = result.get("intent", "UNKNOWN")
                    
                    if intent == "SCHEDULING":
                        st.success(f"🎯 **Intent:** {intent}")
                        st.json(result)
                        st.button("Confirm Calendar Entry", key=f"btn_{msg['id']}")
                    elif intent == "ERROR":
                        st.error(f"⚠️ {result.get('message')}")
                    else:
                        st.warning(f"📝 **Intent:** {intent}")
                        st.json(result)
                else:
                    st.warning("No content to analyze.")

# 7. Footer Logs
st.divider()
st.caption("🛠️ **Engineer Logs:** Cache-hit ratio enabled | Rate-limit throttling active.")