import streamlit as st
import pandas as pd
import requests
from groq import Groq
import os
from datetime import datetime

# Streamlit Page Configuration
st.set_page_config(page_title="AI Lead Scraper Pro", page_icon="🚀", layout="wide")

# Automatically create the history folder if it doesn't exist
FOLDER_HISTORY = "history"
if not os.path.exists(FOLDER_HISTORY):
    os.makedirs(FOLDER_HISTORY)

# ==========================================
# MASTER LICENSE PASSWORD
# ==========================================
PASSWORD_LISENSI = "LEADMASTER2026"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Simple Gatekeeper License Login Page
if not st.session_state["authenticated"]:
    st.container()
    st.title("🔒 Access Locked - AI Lead Scraper Pro")
    st.caption("This software is protected by a commercial license. Please enter your access password.")
    
    password_input = st.text_input("Enter License Password:", type="password")
    if st.button("Unlock Application 🔓", type="primary"):
        if password_input == PASSWORD_LISENSI:
            st.session_state["authenticated"] = True
            st.success("Access Granted!")
            st.rerun()
        else:
            st.error("Invalid License Password! Please contact support to get your access key.")
    st.stop()

# ==========================================
# MAIN INTERFACE (ACCESSIBLE POST-LOGIN)
# ==========================================

# Create Navigation Tabs
tab_main, tab_history, tab_support = st.tabs(["🔍 Scraper & AI Writer", "📜 History Results", "📨 Customer Support"])

# ------------------------------------------
# TAB 1: MAIN MENU (SCRAPER & AI)
# ------------------------------------------
with tab_main:
    st.title("🚀 AI Google Maps Scraper & Cold Email Writer")
    st.caption("Extract REAL local business data from Google Maps and auto-generate highly persuasive cold email pitches via AI.")

    # --- SIDEBAR: API KEY CONFIGURATION ---
    st.sidebar.header("🔑 API Key Settings")
    serp_api_key = st.sidebar.text_input("1. Enter SerpApi Key (Google Maps):", type="password", key="serp_key")
    st.sidebar.markdown("[Get Free SerpApi Key](https://serpapi.com)")

    groq_api_key = st.sidebar.text_input("2. Enter Groq API Key:", type="password", key="groq_key")
    st.sidebar.markdown("[Get Free Groq API Key](https://groq.com)")

    if st.sidebar.button("Logout / Lock App 🚪"):
        st.session_state["authenticated"] = False
        st.rerun()

    # --- MAIN INPUT FORM ---
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

    # --- EXECUTION BUTTON ---
    if st.button("Start Scrape & Generate Emails 🔍", type="primary"):
        if not serp_api_key or not groq_api_key:
            st.error("Please enter both API Keys in the sidebar first!")
        else:
            local_results = []
            start_index = 0
            
            with st.spinner("Fetching live data from Google Maps... Please wait..."):
                while len(local_results) < limit:
                    search_query = f"{keyword} {location}"
                    url = f"https://serpapi.com/search.json?engine=google_maps&q={search_query}&start={start_index}&api_key={serp_api_key}"
                    
                    try:
                        response = requests.get(url)
                        search_results = response.json()
                        current_page_results = search_results.get("local_results", [])
                        
                        if not current_page_results:
                            break
                        
                        for place in current_page_results:
                            has_web = place.get("website")
                            if only_no_website and has_web:
                                continue
                            local_results.append(place)
                            
                        start_index += 20
                        if len(current_page_results) < 20 or len(local_results) >= limit:
                            break
                    except Exception as e:
                        st.error(f"Failed to connect to Google Maps: {str(e)}")
                        break
                
                local_results = local_results[:limit]
                
                if not local_results:
                    st.warning("No business leads found matching your criteria or filters.")
                else:
                    results = []
                    for i, place in enumerate(local_results, 1):
                        results.append({
                            "No": i,
                            "Business Name": place.get("title", "N/A"),
                            "Phone": place.get("phone", "No Phone Number"),
                            "Website": place.get("website", "No Website"),
                            "Rating": place.get("rating", "N/A"),
                            "Reviews": f"{place.get('reviews', 0)} reviews",
                            "Address": place.get("address", "N/A")
                        })
                    
                    try:
                        client = Groq(api_key=groq_api_key)
                        my_bar = st.progress(0, text="Initializing AI email generation engine...")
                        total_data = len(results)
                        
                        for index, item in enumerate(results):
                            persentase = int(((index + 1) / total_data) * 100)
                            my_bar.progress(persentase, text=f"🤖 AI processing lead {index+1} of {total_data} ({persentase}%)")
                            
                            web_condition = f"They already have a website: {item['Website']}" if item['Website'] != "No Website" else "They DO NOT have a website yet."
                            
                            prompt = f"""
                            Act as an expert digital marketing agency and B2B copywriter. Write a highly persuasive, conversion-optimized cold email pitch in English for a local business named '{item['Business Name']}' located in {location}.
                            Business Details: {web_condition} with a Google Maps rating of {item['Rating']}.
                            
                            Your Goal & Strategy:
                            - If they DON'T have a website, pitch a high-converting, affordable website design service integrated with an AI Chatbot to capture missing leads.
                            - If they ALREADY have a website, pitch an AI Chatbot integration/optimization service to automate their customer service and boost their daily sales revenue.
                            
                            Do NOT use generic placeholders like [Your Name] or brackets. Sign off the email using 'Growth Agency Admin'. Put a highly clickable Subject Line on the very first line of your output.
                            """
                            
                            completion = client.chat.completions.create(
                                model="llama-3.1-8b-instant", 
                                messages=[{"role": "user", "content": prompt}],
                                temperature=0.7,
                                max_tokens=300
                            )
                            item["AI Generated Cold Email"] = completion.choices[0].message.content
                        
                        my_bar.empty()
                        
                        # Display Dataframe Results
                        df = pd.DataFrame(results)
                        st.success(f"🔥 Successfully scraped {len(df)} live leads and generated AI cold emails!")
                        st.dataframe(df)
                        
                        # --- FITUR: AUTOMATIC FILE BACKUP TO HISTORY ---
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        csv_filename = f"{FOLDER_HISTORY}/leads_{keyword.lower()}_{location.lower()}_{timestamp}.csv"
                        df.to_csv(csv_filename, index=False)
                        
                        # Direct Download Button
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
                                st.text_area("Use the copy icon on the top-right corner of this box to copy text:", value=r["AI Generated Cold Email"], height=200, key=f"text_{r['No']}")

                    except Exception as e:
                        st.error(f"Groq AI API Error: {str(e)}")

# ------------------------------------------
# TAB 2: HISTORY RESULTS CSV
# ------------------------------------------
with tab_history:
    st.title("📜 Lead Generation History Logs")
    st.caption("All your scraped lists and data are safely backed up inside the local history folder automatically.")
    
    files_in_history = [f for f in os.listdir(FOLDER_HISTORY) if f.endswith(".csv")]
    
    if not files_in_history:
        st.info("No query logs found. Your scraped databases will automatically show up here once you run the scraper.")
    else:
        selected_file = st.selectbox("📁 Select a Past Scraped File:", sorted(files_in_history, reverse=True))
        
        if selected_file:
            full_file_path = os.path.join(FOLDER_HISTORY, selected_file)
            df_history = pd.read_csv(full_file_path)
            st.write(f"📄 Showing data from logs: `{selected_file}`")
            st.dataframe(df_history)
            
            csv_data_history = df_history.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Re-Download This Historical CSV File",
                data=csv_data_history,
                file_name=selected_file,
                mime="text/csv",
                key="btn_download_history"
            )

# ------------------------------------------
# TAB 3: CUSTOMER SUPPORT
# ------------------------------------------
with tab_support:
    st.title("📨 Official Developer & Technical Support")
    st.markdown("---")
    st.markdown("### Encountered a Bug or Need a Feature Customization?")
    st.markdown("If you experience software crashes, license configuration errors, or require specialized feature extensions for your marketing agency, please contact our core development team:")
    
    # Premium Branding Support Box
    st.info("📩 **Official Support Email:** admin@kimpuler.com")
    
    st.markdown("""
    **Recommended Email Ticket Format:**
    - **Subject:** [SUPPORT - AI LEAD SCRAPER] License Issue / Technical Bug
    - **Body:** Clearly describe the issue you are facing and attach screenshots of the console log errors if applicable.
    
    *Our support desk is highly active and will respond to technical inquiries within 24 Hours.*
    """)
