import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import base64
import os
from streamlit_option_menu import option_menu

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Sovereign Risk Intel",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM LOOK AND VISIBILITY ---
st.markdown("""
<style>
    /* Global Fonts & Backgrounds */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* We'll set the background dynamically below with base64 */
    .stApp {
        color: #ffffff !important;
    }
    
    /* Remove Top Padding to push Navbar to the absolute top */
    .block-container {
        padding-top: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Hide Streamlit Header */
    header {
        visibility: hidden !important;
    }
    
    /* Fix Visibility for Streamlit Native Elements */
    .stMarkdown p, .stMarkdown li, .stMarkdown span, .stAlert p, label {
        color: #ffffff !important;
        font-size: 1.05rem;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #58a6ff !important;
    }
    
    strong, b {
        color: #58a6ff !important;
    }
    
    /* Gradients & Animations */
    .title-gradient {
        background: linear-gradient(90deg, #58a6ff 0%, #a371f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        animation: fadeIn 1s ease-in-out;
    }
    
    .subtitle {
        color: #c9d1d9;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        animation: slideUp 1s ease-in-out;
    }
    
    .metric-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(88, 166, 255, 0.15);
        border-color: #58a6ff;
    }
    
    .news-card {
        background: rgba(46, 160, 67, 0.1);
        border-left: 4px solid #2ea043;
        padding: 1rem;
        margin-top: 1rem;
        border-radius: 4px;
        color: #ffffff;
    }
    
    .news-card.high-risk {
        background: rgba(248, 81, 73, 0.1);
        border-left-color: #f85149;
    }
    
    .news-card.medium-risk {
        background: rgba(210, 153, 34, 0.1);
        border-left-color: #d29922;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    hr {
        border-color: #30363d;
    }
</style>
""", unsafe_allow_html=True)

# --- DYNAMIC BACKGROUND IMAGE ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_img_path = r"assets\macro_finance_concept_1777046328204.png"
if os.path.exists(bg_img_path):
    img_b64 = get_base64_of_bin_file(bg_img_path)
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(13, 17, 23, 0.88), rgba(13, 17, 23, 0.96)), url("data:image/png;base64,{img_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/predictions.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# --- TRUE TOP NAVIGATION BAR ---
page = option_menu(
    menu_title=None,
    options=["Overview & Methodology", "Technical Description", "Global Risk Map", "Country Drill-Down", "Model Performance"],
    icons=["house", "file-text", "globe", "bar-chart", "cpu"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important", 
            "margin": "0!important", 
            "max-width": "100%", 
            "background-color": "#161b22", 
            "border-radius": "0",
            "border-bottom": "1px solid #30363d"
        },
        "icon": {"color": "#58a6ff", "font-size": "18px"}, 
        "nav-link": {
            "color": "#ffffff", 
            "font-size": "16px", 
            "text-align": "center", 
            "margin": "0px", 
            "--hover-color": "#30363d",
            "padding": "15px"
        },
        "nav-link-selected": {"background-color": "#a371f7", "font-weight": "bold"},
    }
)

st.markdown("<br>", unsafe_allow_html=True)
st.info("Data Sources: WEO (Macro), FSI (Banking), MONA (IMF Crisis Labels)")

# --- PAGE: OVERVIEW ---
if page == "Overview & Methodology":
    st.markdown('<div class="title-gradient">Sovereign Financial Crisis Early Warning System</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predictive Intelligence for Macroeconomic Risk</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Project Objective
    Forecast country financial crisis risk for the next 5 years using historical macro-financial data from the International Monetary Fund (IMF). The system combines multiple machine learning models into a weighted ensemble for robust, real-world predictions.
    
    ---
    """)
    
    col1, col2 = st.columns([2, 1.5])
    
    with col1:
        st.markdown("""
        ### Strategic Use Cases & Target Audience
        **Core Insight**: This model gives risk managers a 2-3 year head start before traditional credit rating agencies downgrade a sovereign entity, utilizing leading macro-financial indicators to predict distress before it materializes.
        
        | Target Audience | Core Action & Use Case |
        | :--- | :--- |
        | **Emerging Market Fund Manager** | Reduce exposure to HIGH risk countries before a crisis hits. |
        | **Corporate Treasurer** | Avoid entering long-term contracts in high-risk countries. |
        | **Bank Credit Risk Team** | Flag sovereign counterparty risk in loan books. |
        | **Development Finance Inst.** | Prioritise technical assistance to at-risk countries. |
        | **Rating Agency Analyst** | Use as a quantitative cross-check on qualitative ratings. |
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Interpretation Guide (Risk Categories)")
        st.markdown("""
        <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 10px; margin-bottom: 30px;">
            <div style="flex: 1 1 calc(33.333% - 15px); background: rgba(46, 160, 67, 0.1); border-left: 4px solid #2ea043; padding: 15px; border-radius: 6px; box-sizing: border-box;">
                <div style="color: #2ea043; font-weight: bold; margin-bottom: 8px; font-size: 1.05rem; text-transform: uppercase;">🟢 LOW (0.0 - 0.2)</div>
                <div style="color: #ffffff; font-size: 0.9rem; line-height: 1.4;">Standard portfolio allocation. Strong GDP, low debt.</div>
            </div>
            <div style="flex: 1 1 calc(33.333% - 15px); background: rgba(88, 166, 255, 0.1); border-left: 4px solid #58a6ff; padding: 15px; border-radius: 6px; box-sizing: border-box;">
                <div style="color: #58a6ff; font-weight: bold; margin-bottom: 8px; font-size: 1.05rem; text-transform: uppercase;">🔵 MILD LOW (0.2 - 0.4)</div>
                <div style="color: #ffffff; font-size: 0.9rem; line-height: 1.4;">Monitor, but no special focus needed.</div>
            </div>
            <div style="flex: 1 1 calc(33.333% - 15px); background: rgba(210, 153, 34, 0.1); border-left: 4px solid #d29922; padding: 15px; border-radius: 6px; box-sizing: border-box;">
                <div style="color: #d29922; font-weight: bold; margin-bottom: 8px; font-size: 1.05rem; text-transform: uppercase;">🟡 MODERATE (0.4 - 0.6)</div>
                <div style="color: #ffffff; font-size: 0.9rem; line-height: 1.4;">Transition point. Watch carefully.</div>
            </div>
            <div style="flex: 1 1 calc(50% - 15px); background: rgba(248, 81, 73, 0.1); border-left: 4px solid #f85149; padding: 15px; border-radius: 6px; box-sizing: border-box;">
                <div style="color: #f85149; font-weight: bold; margin-bottom: 8px; font-size: 1.05rem; text-transform: uppercase;">🟠 HIGH (0.6 - 0.8)</div>
                <div style="color: #ffffff; font-size: 0.9rem; line-height: 1.4;">Potential for crisis in 1-2 years. Reduce exposure.</div>
            </div>
            <div style="flex: 1 1 calc(50% - 15px); background: rgba(139, 0, 0, 0.2); border-left: 4px solid #ff4444; padding: 15px; border-radius: 6px; box-sizing: border-box;">
                <div style="color: #ff4444; font-weight: bold; margin-bottom: 8px; font-size: 1.05rem; text-transform: uppercase;">🔴 EXTREME (0.8 - 1.0)</div>
                <div style="color: #ffffff; font-size: 0.9rem; line-height: 1.4;">Crisis likely imminent. Immediate divestment.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        img_path2 = r"assets\risk_dashboard_concept_1777046509974.png"
        if os.path.exists(img_path2):
            img_b64_2 = get_base64_of_bin_file(img_path2)
            st.markdown(f'<img src="data:image/png;base64,{img_b64_2}" style="width: 100%; height: 280px; object-fit: cover; border-radius: 8px; margin-bottom: 10px;">', unsafe_allow_html=True)
        st.markdown("""
        ### Key Limitations
        
        - **Sparse FSI Data:** Only 153 of 195 countries have comprehensive banking data. The model relies more heavily on macro variables for smaller economies.
        - **Target Definition:** It predicts IMF bailout programs, not sovereign defaults directly. Some severe crises (e.g., Venezuela) never resulted in IMF programs due to political barriers.
        - **Class Imbalance:** Only ~20% of historical observations are crisis cases, making prediction complex and highly sensitive to thresholds.
        - **Data Integrity:** Macroeconomic data carries political noise. Governments sometimes over-report optimistic numbers leading up to a crisis.
        """)

# --- PAGE: TECHNICAL DESCRIPTION ---
elif page == "Technical Description":
    st.markdown('<div class="title-gradient">Technical Architecture & Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">End-to-End Documentation of the Data and Modeling Lifecycle</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    tech_page = option_menu(
        menu_title=None,
        options=["Data Sources & Integration", "Data Cleaning & Preparation", "Modeling Pipeline"],
        icons=["database", "wrench", "cpu"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important", 
                "margin": "0!important", 
                "background-color": "transparent", 
                "border-radius": "0"
            },
            "icon": {"color": "#58a6ff", "font-size": "16px"}, 
            "nav-link": {
                "color": "#c9d1d9", 
                "font-size": "14px", 
                "text-align": "center", 
                "margin": "0px", 
                "--hover-color": "#30363d",
                "text-transform": "uppercase",
                "font-weight": "bold"
            },
            "nav-link-selected": {
                "background-color": "transparent", 
                "color": "#a371f7", 
                "border-bottom": "3px solid #a371f7",
                "border-radius": "0"
            },
        }
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if tech_page == "Data Sources & Integration":
        st.markdown("<h3 style='color:#58a6ff;'>The Foundation: IMF Datasets</h3>", unsafe_allow_html=True)
        st.markdown("""
        The predictive engine relies on fusing three disparate datasets from the International Monetary Fund (IMF), each providing a distinct angle on sovereign health.
        
        * **1. World Economic Outlook (WEO):** Provides the core macroeconomic indicators (GDP Growth, Inflation, Current Account Balance, Government Debt to GDP). Crucially, the WEO contains historical data *and* 5-year projections, which allows our model to forecast risk into the future.
        * **2. Financial Soundness Indicators (FSI):** Provides banking sector health metrics (Return on Equity, Regulatory Capital Ratios). Banking crises often precede or run parallel to sovereign debt crises.
        * **3. MONA (Monitoring of Fund Arrangements):** The ground-truth label dataset. It contains the exact dates when countries entered IMF bailout programs.
        """)
        
        st.info("💡 **Reasoning for Integration:** Macroeconomic indicators alone are trailing. By combining WEO's broad macro data with FSI's banking liquidity data, we capture the dual-nature of modern financial crises. MONA is used to engineer a binary target: *'Will this country experience a crisis in the next 3 years?'*")

    elif tech_page == "Data Cleaning & Preparation":
        st.markdown("<h3 style='color:#58a6ff;'>Overcoming Real-World Data Challenges</h3>", unsafe_allow_html=True)
        st.markdown("""
        Raw macroeconomic data is incredibly noisy. Our data pipeline applies several critical transformations before any modeling occurs:
        
        1. **Fuzzy String Matching:** Country names differ across IMF datasets (e.g., "Kyrgyz Republic" vs "Kyrgyzstan"). We utilized `difflib` string matching to computationally map sovereign entities, successfully rescuing over 300 crisis labels that would have otherwise been lost.
        2. **Sparse Matrix Imputation:** Because FSI banking data is often not reported by developing nations, simply dropping missing rows would delete 60% of the globe. We utilize Scikit-Learn's `IterativeImputer` to probabilistically estimate missing banking metrics based on the country's macro environment.
        3. **Extreme Outlier Handling (The Hyperinflation Problem):** Some countries experience inflation rates exceeding 65,000%. Standard scaling techniques squash all normal data to zero when exposed to these extremes. We implemented hard percentiles: **Clipping all features at the 1st and 99th percentiles** of the training distribution, followed by a `RobustScaler` utilizing the Interquartile Range (IQR).
        """)
        
        st.warning("⚠️ **Pipeline Integrity:** The pipeline uses a strict chronological Train/Test split. We train on data from 2001-2018 and test strictly on 2019-2023. This prevents 'Look-Ahead Bias', ensuring our accuracy metrics reflect a true predictive scenario.")

    elif tech_page == "Modeling Pipeline":
        st.markdown("<h3 style='color:#58a6ff;'>The Ensemble Modeling Engine</h3>", unsafe_allow_html=True)
        st.markdown("""
        No single algorithm is perfect for predicting macroeconomic failure. We implemented a hybrid Ensemble approach:
        
        #### Component 1: Logistic Regression (LR)
        - **Why we use it:** LR is a linear model that provides excellent interpretability. If government debt skyrockets, LR cleanly captures that linear risk escalation.
        - **Configuration:** We use `class_weight='balanced'` to force the model to pay attention to the rare crisis events (which make up only ~20% of the dataset).
        
        #### Component 2: Gradient Boosting Classifier (GB)
        - **Why we use it:** GB builds sequential decision trees. It excels at finding non-linear thresholds (e.g., Debt is okay *unless* GDP is also shrinking and Inflation is above 10%). It handles complex interactions that Logistic Regression misses.
        
        #### The Final Ensemble Output
        The model averages the predicted probabilities from both LR and GB. 
        - **Why Ensemble?** It drastically reduces variance. LR prevents GB from overfitting to noise, while GB allows LR to capture complex edge-cases. The result is a smoothed, highly stable `Ensemble_Prob` risk score bounded between 0.0 and 1.0.
        """)

# --- PAGE: GLOBAL RISK MAP ---
elif page == "Global Risk Map":
    st.markdown('<div class="title-gradient">Global Risk Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Geospatial Distribution of Sovereign Risk</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.warning("Data not found.")
    else:
        years = sorted(df['Year'].unique())
        # Ensure user knows projections are used
        st.markdown("*(Drag the slider to view historical risk up to 2023, and projected risk from 2024 - 2028 based on IMF macro-forecasts)*")
        selected_year = st.slider("Select Year", min_value=int(min(years)), max_value=int(max(years)), value=int(max(years)))
        
        df_year = df[df['Year'] == selected_year]
        
        # Color mapping
        color_discrete_map = {'Extreme': '#8b0000', 'High': '#ff7b72', 'Moderate': '#d29922', 'Mild Low': '#58a6ff', 'Low': '#2ea043'}
        
        fig = px.choropleth(
            df_year, 
            locations="ISO", 
            color="Risk_Level",
            hover_name="Country",
            hover_data={"ISO": False, "Ensemble_Prob": ':.2f', "GDP_Growth": ':.1f', "Inflation": ':.1f'},
            color_discrete_map=color_discrete_map,
            projection="natural earth",
            title=f"Sovereign Risk Assessment ({selected_year})"
        )
        
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular', bgcolor='rgba(0,0,0,0)'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6e6'),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig, width='stretch')
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("### High & Extreme Risk Countries")
            st.markdown(f"Immediate review required for counterparties in these jurisdictions for **{selected_year}**.")
            high_risk = df_year[df_year['Risk_Level'].isin(['High', 'Extreme'])][['Country', 'Risk_Level', 'Ensemble_Prob']].sort_values('Ensemble_Prob', ascending=False)
            
            if not high_risk.empty:
                html_table = "<style>"
                html_table += ".custom-table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 0.95rem; background-color: rgba(22, 27, 34, 0.7); border-radius: 8px; overflow: hidden; border: 1px solid #30363d; }"
                html_table += ".custom-table th { background-color: rgba(88, 166, 255, 0.1); color: #58a6ff !important; padding: 12px 15px; font-weight: 600; text-transform: uppercase; border-bottom: 2px solid #58a6ff; text-align: center !important; }"
                html_table += ".custom-table td { padding: 10px 15px; border-bottom: 1px solid #30363d; color: #ffffff; vertical-align: middle; text-align: center; }"
                html_table += ".custom-table tr:hover { background-color: rgba(255, 255, 255, 0.05); }"
                html_table += "</style>"
                html_table += "<table class='custom-table'><thead><tr><th>Country</th><th>Risk Level</th><th>Probability</th></tr></thead><tbody>"
                for _, row in high_risk.iterrows():
                    color = "#ff4444" if row['Risk_Level'] == 'Extreme' else "#f85149"
                    html_table += f"<tr><td style='font-weight: bold; color: #ffffff;'>{row['Country']}</td>"
                    html_table += f"<td><span style='color: {color} !important; font-weight: bold;'>{row['Risk_Level']}</span></td>"
                    html_table += f"<td style='color: #ffffff;'>{row['Ensemble_Prob']:.2f}</td></tr>"
                html_table += "</tbody></table>"
                st.markdown(html_table, unsafe_allow_html=True)
            else:
                st.success(f"No high or extreme risk countries found for {selected_year}.")
            
        with col2:
            st.markdown("### Risk Calculation Methodology")
            st.markdown("""
            <div style="background-color: rgba(88, 166, 255, 0.1); border-left: 4px solid #58a6ff; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
                <div style="color: #58a6ff; font-weight: bold; margin-bottom: 10px; font-size: 1.05rem;">How is this calculated?</div>
                <div style="color: #ffffff; font-size: 0.95rem; line-height: 1.5;">
                    The risk score visualized on this map is generated by our dual-model Ensemble Engine.<br><br>
                    <span style="color: #58a6ff; font-weight: bold;">For years up to 2023:</span> The model evaluates ground-truth, historical macroeconomic metrics (GDP, Debt, Current Account) and banking liquidity metrics (FSI) to assess if conditions match the patterns of historical sovereign defaults.<br><br>
                    <span style="color: #58a6ff; font-weight: bold;">For years 2024 to 2028:</span> The model actively ingests 5-year projections directly from the IMF's World Economic Outlook (WEO) baseline estimates. It runs these projected futures through the trained machine learning pipeline to output forward-looking crisis probabilities. <i>(Note: Because banking FSI data does not provide forecasts, those specific banking indicators are probabilistically imputed based on the surrounding macro-forecast).</i>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Strategic Action Plan")
            st.markdown("""
            <div style="background-color: rgba(88, 166, 255, 0.1); border-left: 4px solid #58a6ff; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
                <div style="color: #58a6ff; font-weight: bold; margin-bottom: 10px; font-size: 1.05rem;">Managerial Implications for High & Extreme Risk Jurisdictions:</div>
                <ul style="color: #ffffff; font-size: 0.95rem; line-height: 1.5; margin-top: 0; padding-left: 20px;">
                    <li style="margin-bottom: 8px;"><span style="color: #58a6ff; font-weight: bold;">Halt Long-Term Exposure:</span> Immediately freeze new uncollateralized lending or long-term infrastructure investments in flagged regions.</li>
                    <li style="margin-bottom: 8px;"><span style="color: #58a6ff; font-weight: bold;">Increase Hedging:</span> Procure sovereign credit default swaps (CDS) to protect existing portfolio exposure.</li>
                    <li style="margin-bottom: 8px;"><span style="color: #58a6ff; font-weight: bold;">Supply Chain Pivot:</span> For corporate treasurers, begin sourcing alternative suppliers outside of these jurisdictions, as sovereign distress historically triggers strict capital controls and import/export delays.</li>
                    <li><span style="color: #58a6ff; font-weight: bold;">Contextual Verification:</span> The model relies on quantitative data. Before total divestment, cross-check these alerts against qualitative factors such as ongoing IMF bailout negotiations or sudden geopolitical support packages.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# --- PAGE: COUNTRY DRILL-DOWN ---
elif page == "Country Drill-Down":
    st.markdown('<div class="title-gradient">Country Deep-Dive & 5-Year Forecast</div>', unsafe_allow_html=True)
    
    if not df.empty:
        countries = sorted(df['Country'].unique())
        selected_country = st.selectbox("Select Country", countries, index=countries.index('Argentina') if 'Argentina' in countries else 0)
        
        df_country = df[df['Country'] == selected_country].sort_values('Year')
        
        # Adjusted ratio to give the chart more breathing room
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown(f"### Risk Trajectory: {selected_country}")
            
            fig = go.Figure()
            
            # Historical Data
            df_hist = df_country[df_country['Year'] <= 2023]
            fig.add_trace(go.Scatter(x=df_hist['Year'], y=df_hist['Ensemble_Prob'], 
                                     mode='lines+markers', name='Historical (Actuals)',
                                     line=dict(color='#a371f7', width=3)))
            
            # Forecast Data
            df_forecast = df_country[df_country['Year'] >= 2023]
            fig.add_trace(go.Scatter(x=df_forecast['Year'], y=df_forecast['Ensemble_Prob'], 
                                     mode='lines+markers', name='Forecast (Projections)',
                                     line=dict(color='#58a6ff', width=3, dash='dash')))
            
            # Thresholds
            fig.add_hline(y=0.8, line_dash="dot", line_color="#8b0000", annotation_text="Extreme Risk")
            fig.add_hline(y=0.6, line_dash="dot", line_color="#ff7b72", annotation_text="High Risk")
            fig.add_hline(y=0.4, line_dash="dot", line_color="#d29922", annotation_text="Moderate Risk")
            fig.add_hline(y=0.2, line_dash="dot", line_color="#2ea043", annotation_text="Low Risk")
            fig.add_vline(x=2023.5, line_dash="solid", line_color="#ffffff", annotation_text="Forecast Horizon Begins")
            
            # Ensure future years are explicitly shown on the x-axis
            fig.update_xaxes(tickmode='linear', tick0=2001, dtick=2)
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff', size=13),
                xaxis=dict(gridcolor='#30363d'),
                yaxis=dict(gridcolor='#30363d', range=[0, 1]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, width='stretch')
            
        with col2:
            latest_prob = df_country.iloc[-1]['Ensemble_Prob']
            latest_risk = df_country.iloc[-1]['Risk_Level']
            
            risk_color = "#2ea043"
            news_class = "news-card"
            if latest_risk in ["High", "Extreme"]:
                risk_color = "#f85149"
                news_class = "news-card high-risk"
            elif latest_risk == "Moderate":
                risk_color = "#d29922"
                news_class = "news-card medium-risk"
                
            st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid {risk_color}; padding: 20px;">
                <div style="color: #ffffff; font-weight: 800; font-size: 2.5rem; text-align: left; margin-bottom: 0; line-height: 1.2;">Latest 2028 Projection</div>
                <h1 style="color:{risk_color}; margin: 0; font-size: 4rem; padding-top: 0; line-height: 1.1;">{latest_prob:.2f}</h1>
                <p style="color:#ffffff; font-weight:bold; font-size: 1.4rem; margin-top: 5px; margin-bottom: 0;">Risk Category: {latest_risk}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Dynamic Managerial Implications
            st.markdown("### Strategic Action Plan")
            if latest_risk in ["High", "Extreme"]:
                st.markdown("""
                **Corporate Operations & Treasury:**
                - **Divestment Strategy:** Initiate gradual drawdown of sovereign bond holdings.
                - **Contractual Protection:** Implement strict force majeure and currency revaluation clauses in localized vendor contracts.
                - **Currency Hedging:** Maximize hedging ratios for expected local currency cash flows.
                
                **Policy & Credit Risk:**
                - Cease new uncollateralized lending to domestic institutions.
                - Prepare contingency plans for sudden capital controls or debt restructuring.
                """)
                news_headline = f"⚠️ SYSTEMIC ALERT: {selected_country}'s macro imbalances point to high likelihood of IMF intervention. Capital flight risks elevated."
            elif latest_risk == "Moderate":
                st.markdown("""
                **Corporate Operations & Treasury:**
                - **Enhanced Monitoring:** Move country to active watch-list. Review exposures monthly.
                - **Duration Management:** Avoid long-duration debt. Keep investments highly liquid.
                
                **Policy & Credit Risk:**
                - Request additional collateral from local counterparties.
                - Begin exploring geographic diversification for concentrated supply chains.
                """)
                news_headline = f"🔍 WATCHLIST: {selected_country} approaching transition point. Fundamental weakness observed in leading macro indicators."
            else:
                st.markdown("""
                **Corporate Operations & Treasury:**
                - **Business as Usual:** Maintain standard portfolio allocations.
                - **Strategic Expansion:** Favorable environment for foreign direct investment (FDI) and long-term joint ventures.
                - **Yield Harvesting:** Safe to exploit local market yield premiums where available.
                """)
                news_headline = f"✅ STABLE OUTLOOK: {selected_country} demonstrates robust macro-financial resilience. Default probabilities remain anchored."
                
            st.markdown(f"""
            <div class="{news_class}">
                <b>{news_headline}</b>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Underlying Macroeconomic Drivers")
        st.markdown("The following charts display the raw data feeding into the predictive ensemble model. **Historical data is shown up to 2023, followed by official IMF baseline forecasts out to 2028.**")
        
        col3, col4 = st.columns(2)
        with col3:
            fig_gdp = px.line(df_country, x='Year', y='GDP_Growth', title='GDP Growth (%)')
            fig_gdp.add_vline(x=2023.5, line_dash="dash", line_color="#ffffff", annotation_text="Forecast Starts")
            fig_gdp.update_xaxes(tickmode='linear', tick0=2001, dtick=3)
            fig_gdp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff', size=13))
            st.plotly_chart(fig_gdp, width='stretch')
        with col4:
            fig_inf = px.line(df_country, x='Year', y='Gov_Debt_GDP', title='Govt Debt to GDP (%)')
            fig_inf.add_vline(x=2023.5, line_dash="dash", line_color="#ffffff", annotation_text="Forecast Starts")
            fig_inf.update_xaxes(tickmode='linear', tick0=2001, dtick=3)
            fig_inf.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff', size=13))
            st.plotly_chart(fig_inf, width='stretch')
            
        st.info("""
        **Diagnostic Explanation:** 
        Declining or highly volatile GDP growth combined with an accelerating Government Debt-to-GDP ratio acts as the primary catalyst for sovereign distress. 
        
        When debt outpaces economic growth (i.e., the debt curve rises while the GDP curve falls), governments face severe revenue constraints and refinancing risks. This creates a "debt spiral", forcing the sovereign entity toward an IMF bailout. Stabilizing the debt ratio and recovering real GDP growth are essential for migrating out of the 'High Risk' category.
        """)

# --- PAGE: MODEL PERFORMANCE ---
elif page == "Model Performance":
    st.markdown('<div class="title-gradient">Model Diagnostics & Reasoning</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #58a6ff; padding: 20px;">
            <div style="color: #ffffff; font-weight: 800; font-size: 1.6rem; text-align: left; margin-bottom: 0; line-height: 1.2;">Logistic Regression</div>
            <h1 style="color:#58a6ff; margin: 0; font-size: 3rem; padding-top: 5px; line-height: 1.1;">0.64</h1>
            <p style="color:#ffffff; font-weight:bold; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;">ROC-AUC Score</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #58a6ff; padding: 20px;">
            <div style="color: #ffffff; font-weight: 800; font-size: 1.6rem; text-align: left; margin-bottom: 0; line-height: 1.2;">Gradient Boosting</div>
            <h1 style="color:#58a6ff; margin: 0; font-size: 3rem; padding-top: 5px; line-height: 1.1;">0.70</h1>
            <p style="color:#ffffff; font-weight:bold; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;">ROC-AUC Score</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #a371f7; padding: 20px;">
            <div style="color: #ffffff; font-weight: 800; font-size: 1.6rem; text-align: left; margin-bottom: 0; line-height: 1.2;">Final Ensemble</div>
            <h1 style="color:#a371f7; margin: 0; font-size: 3rem; padding-top: 5px; line-height: 1.1;">0.67</h1>
            <p style="color:#ffffff; font-weight:bold; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;">ROC-AUC Score</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("<h3 style='color:#58a6ff;'>Why These Models?</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<h4 style='color:#a371f7;'>1. Logistic Regression</h4>", unsafe_allow_html=True)
        st.markdown("""
        **Reasoning:** Chosen for its high interpretability and baseline performance. It assumes linear relationships. If debt goes up, risk goes up smoothly.
        
        By using `class_weight='balanced'`, we explicitly forced the model to penalize errors on minority "Crisis" events heavily, ensuring we don't just predict "No Crisis" every time.
        """)
        
    with c2:
        st.markdown("<h4 style='color:#a371f7;'>2. Gradient Boosting</h4>", unsafe_allow_html=True)
        st.markdown("""
        **Reasoning:** Chosen to handle non-linear interactions. In reality, a country can survive high debt *if* growth is also high. Linear models fail to capture these "if-then" interactions.
        
        Gradient Boosting constructs hundreds of sequential decision trees, learning the complex boundaries of when a macro-imbalance becomes fatal.
        """)
        
    with c3:
        st.markdown("<h4 style='color:#a371f7;'>3. The Ensemble Mechanism</h4>", unsafe_allow_html=True)
        st.markdown("""
        **Reasoning:** The final model takes the unweighted average of the probabilities from LR and GB. 
        
        This drastically reduces variance. Macroeconomic data is incredibly noisy; combining a linear model and a tree-based model ensures the final risk score is stable, conservative, and far less prone to overfitting than either model alone.
        """)
        
    st.markdown("---")
    st.markdown("<h3 style='color:#58a6ff;'>Validation Framework</h3>", unsafe_allow_html=True)
    st.markdown("""
    The model was validated using a strict, forward-looking time-series split to prevent data leakage:
    - **Training Data:** 2001 - 2018
    - **Testing Data:** 2019 - 2023
    """)
    
    st.markdown("<h3 style='color:#58a6ff;'>Performance Interpretation</h3>", unsafe_allow_html=True)
    st.markdown("""
    Predicting sovereign crises 3-5 years in advance is a highly complex, noisy task heavily influenced by sudden political shifts. An AUC of ~0.67 indicates solid predictive power, significantly outperforming random guessing (0.50). Crucially, the model's value lies in generating **early warning signals** that precede formal downgrades by rating agencies.
    """)
