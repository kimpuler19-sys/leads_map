# main.py - File utama yang akan dijalankan (tidak diproteksi)
# Streamlit UI dan interaksi pengguna

import streamlit as st
import pandas as pd
from datetime import datetime

# Import semua fungsi dari core.py
from core import (
    verify_gumroad_license,
    verify_demo_access,
    scrape_google_maps,
    format_results,
    process_all_emails,
    save_to_csv,
    get_history_files,
    load_history_file,
    check_auth_status,
    set_auth_status,
    validate_api_keys,
    EXPIRY_DATE
)

# ========================================================
# INITIAL SYSTEM CONFIGURATION
# ========================================================
st.set_page_config(page_title="AI Lead Scraper Pro", page_icon="🚀", layout="wide")

current_date = datetime.now()

# ========================================================
# GATEKEEPER INTERFACE (LOGIN PORTAL)
# ========================================================
if not check_auth_status():
    st.container()
    st.title("🔒 Activation Portal - AI Lead Scraper Pro")
    st.caption("Please select your activation method to unlock the premium dashboard infrastructure.")
    
    auth_tab1, auth_tab2 = st.tabs(["🛒 Gumroad Commercial License", "🧪 Free Demo Access"])
    
    with auth_tab1:
        st.subheader("Activate Commercial Version")
        st.markdown("Enter the unique license key sent to your email after checkout.")
        gumroad_input = st.text_input("Gumroad License Key:", type="password", placeholder="XXXX-XXXX-XXXX-XXXX", key="gum_input")
        
        if st.button("Verify & Activate Full Software 🚀", type="primary", key="btn_gum"):
            if not gumroad_input:
                st.error("License key cannot be empty!")
            else:
                with st.spinner("Verifying license key with Gumroad..."):
                    is_valid, message = verify_gumroad_license(gumroad_input)
                    if is_valid:
                        set_auth_status(True)
                        st.success("Software Activated Successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                        
    with auth_tab2:
        st.subheader("Activate Limited Time Trial")
        
        if current_date > EXPIRY_DATE:
            st.error("❌ The evaluation period for this demo version expired on July 20, 2026. Please upgrade to a commercial license.")
        else:
            st.markdown("Enter your exclusive, single-use demo password provided by the administrator.")
            demo_input = st.text_input("Demo Password Key:", type="password", placeholder="DEMOKEY-XXXX", key="demo_input")
            
            if st.button("Unlock Limited Demo 🔓", type="primary", key="btn_demo"):
                if demo_input:
                    is_valid, message = verify_demo_access(demo_input)
                    if is_valid:
                        set_auth_status(True)
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("Please enter a demo password!")
    st.stop()

# ========================================================
# MAIN WORKSTATION PLATFORM (POST-LOGIN INTERACTION)
# ========================================================
tab_main, tab_history, tab_support = st.tabs(["🔍 Scraper & AI Writer", "📜 History Results", "📨 Customer Support"])

# --------------------------------------------------------
# TAB 1: LIVE EXTRACTOR WORKSTATION
# --------------------------------------------------------
with tab_main:
    st.title("🚀 AI Google Maps Scraper & Cold Email Writer")
    st.caption("Extract REAL local business data from Google Maps and auto-generate highly persuasive cold email pitches via AI.")

    st.sidebar.header("🔑 API Key Settings")
    serp_api_key = st.sidebar.text_input("1. Enter SerpApi Key (Google Maps):", type="password", key="serp_key")
    st.sidebar.markdown("[Get Free SerpApi Key](https://serpapi.com)")

    groq_api_key = st.sidebar.text_input("2. Enter Groq API Key:", type="password", key="groq_key")
    st.sidebar.markdown("[Get Free Groq API Key](https://groq.com)")

    if st.sidebar.button("Logout / Lock App 🚪"):
        set_auth_status(False)
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Business Keyword (e.g., Dentist, Cafe, Restaurant):", "Restaurant")
    with col2:
        location = st.text_input("Location / City (e.g., New York, Los Angeles, London):", "Los Angeles")

    col3, col4 = st.columns(2)
    with col3:
        limit = st.slider("Max Number of Leads to Scrape:", min_value=5, max_value=50, value=10, step=5)
    with col4:
        only_no_website = st.checkbox("🎯 Only show businesses WITHOUT a Website")

    if st.button("Start Scrape & Generate Emails 🔍", type="primary"):
        if not validate_api_keys(serp_api_key, groq_api_key):
            st.error("Please enter both API Keys in the sidebar first!")
        else:
            try:
                with st.spinner("Fetching live data from Google Maps APIs... Please wait..."):
                    local_results = scrape_google_maps(serp_api_key, keyword, location, limit, only_no_website)
                
                if not local_results:
                    st.warning("No business leads matched your specialized criteria or filters.")
                else:
                    results = format_results(local_results)
                    
                    my_bar = st.progress(0, text="Initializing Neural Copywriting Engine...")
                    
                    def update_progress(index, total):
                        percentage = int(((index + 1) / total) * 100)
                        my_bar.progress(percentage, text=f"🤖 AI processing lead {index+1} of {total} ({percentage}%)")
                    
                    results = process_all_emails(groq_api_key, results, location, update_progress)
                    my_bar.empty()
                    
                    df = pd.DataFrame(results)
                    st.success(f"🔥 Successfully scraped {len(df)} live leads and generated AI cold emails!")
                    st.dataframe(df)
                    
                    filename, df = save_to_csv(results, keyword, location)
                    
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Leads Data (CSV)",
                        data=csv_data,
                        file_name=f"premium_leads_{keyword.lower()}_{location.lower()}.csv",
                        mime="text/csv",
                    )
                    
                    st.write("---")
                    st.subheader("📋 View & Copy Individual Email Pitches")
                    for r in results:
                        with st.expander(f"✉️ Pitch for: {r['Business Name']} ({r['Phone']})"):
                            st.text_area("Use the copy icon on the top-right corner of this box to copy text:", 
                                        value=r["AI Generated Cold Email"], height=200, key=f"text_{r['No']}")
                            
            except Exception as e:
                st.error(f"Error: {str(e)}")

# --------------------------------------------------------
# TAB 2: AUDIT LOGS LOGISTICS
# --------------------------------------------------------
with tab_history:
    st.title("📜 Lead Generation History Logs")
    st.caption("All your scraped lists and records are automatically backed up inside the local history folder.")
    
    files_in_history = get_history_files()
    
    if not files_in_history:
        st.info("No logs found. Your scraped databases will automatically show up here once you run a query loop.")
    else:
        selected_file = st.selectbox("📁 Select a Past Scraped File:", sorted(files_in_history, reverse=True))
        
        if selected_file:
            df_history = load_history_file(selected_file)
            st.write(f"📄 Displaying data fields from logs: `{selected_file}`")
            st.dataframe(df_history)
            
            csv_data_history = df_history.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Re-Download This Historical CSV File",
                data=csv_data_history,
                file_name=selected_file,
                mime="text/csv",
                key="btn_download_history"
            )

# --------------------------------------------------------
# TAB 3: CUSTOMER ENGINE SUPPORT TICKETS
# --------------------------------------------------------
with tab_support:
    st.title("📨 Official Developer & Technical Support")
    st.markdown("---")
    st.markdown("### Encountered a Bug or Need a System Extension?")
    st.markdown("If you experience software crashes, license activation errors, or require specialized algorithmic adjustments for your agency ecosystem, reach out directly to the core vendor team:")
    
    st.info("📩 **Official Support Email Desk:** admin@kimpuler.com")
    
    st.markdown("""
    **Recommended Email Ticket Layout Requirements:**
    - **Subject:** [SUPPORT - AI LEAD SCRAPER] License Issue / Technical Bug
    - **Body:** Clearly describe the software behavior and attach system screenshots if applicable.
    
    *Our support systems are operational and will reply to engineering requests within a 24-Hour window.*
    """)