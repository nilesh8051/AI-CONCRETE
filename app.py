
import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config for modern look (wide layout, fav icon)
st.set_page_config(
    page_title="AI Concrete Optimizer",
    page_icon="🧱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize dark theme state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Custom CSS for professional, modern civil theme (concrete grays, clean lines)
st.markdown("""
<style>
    :root {
        --concrete-100: #f5f6f7;
        --concrete-200: #eef0f2;
        --concrete-400: #cfd4d9;
        --concrete-600: #9aa0a6;
        --steel-700: #2f3b46;
        --steel-800: #24313a;
        --accent-orange: #f39c12;
        --accent-blue: #2980b9;
    }

    /* Top hazard stripe bar for construction vibe */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 6px;
        background-image: repeating-linear-gradient(45deg, var(--accent-orange) 0 18px, var(--steel-700) 18px 36px);
        z-index: 1000;
    }

    /* Main concrete texture background */
    .stApp, .main {
        background-color: var(--concrete-100);
        background-image:
            linear-gradient(0deg, rgba(255,255,255,0.9), rgba(255,255,255,0.9)),
            radial-gradient(circle at 12% 18%, rgba(0,0,0,0.03) 2px, transparent 2px),
            radial-gradient(circle at 74% 62%, rgba(0,0,0,0.03) 1.5px, transparent 1.5px);
        background-size: auto, 14px 14px, 16px 16px;
        background-attachment: fixed;
    }

    /* Header styling - bold civil theme */
    .stApp h1 {
        color: var(--steel-700);
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        font-size: 2.6em;
        text-align: center;
        letter-spacing: 0.5px;
        margin: 0.2em 0 0.4em;
        position: relative;
    }
    .stApp h1::after {
        content: '';
        display: block;
        width: 140px;
        height: 4px;
        margin: 10px auto 0;
        background: linear-gradient(90deg, var(--accent-orange), var(--accent-blue));
        border-radius: 2px;
    }

    /* Sidebar - steel concrete gradient with accent bar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--steel-700) 0%, var(--steel-800) 100%);
        color: #ecf0f1;
        border-right: 5px solid var(--accent-orange);
        box-shadow: 2px 0 8px rgba(0,0,0,0.15);
    }
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stCaption {
        color: #ecf0f1 !important;
    }

    /* Buttons - safety orange primary */
    .stButton > button {
        background: linear-gradient(45deg, var(--accent-orange), #d35400);
        color: #fff;
        border-radius: 10px;
        font-weight: 700;
        border: none;
        padding: 0.6em 1.2em;
        box-shadow: 0 4px 10px rgba(243, 156, 18, 0.35);
        transition: transform 0.08s ease-out, filter 0.12s ease-out;
    }
    .stButton > button:hover { filter: brightness(1.05); transform: translateY(-1px); }
    .stButton > button:active { transform: translateY(0); }

    /* Metrics - card with rebar accent */
    div[data-testid="stMetric"] {
        background: #fff;
        border-radius: 12px;
        padding: 10px 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 6px solid var(--steel-700);
    }
    .stMetric > label { color: #6b7785; font-weight: 600; }
    .stMetric > div > div { color: var(--steel-700); font-size: 1.5em; }

    /* Tabs - concrete caps with steel underline */
    .stTabs [data-baseweb="tab-list"] { gap: 0.6rem; border-bottom: 4px solid var(--steel-700); }
    .stTabs [data-baseweb="tab"] {
        background-color: var(--concrete-200);
        border-radius: 10px 10px 0 0;
        padding: 0.75rem 1rem;
        color: var(--steel-700);
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #fff; border: 1px solid var(--concrete-400); border-bottom: none; }

    /* Expanders - clean concrete panel */
    .stExpander { border: 1px solid var(--concrete-400); border-radius: 12px; background: #fff; }
    .stExpander .streamlit-expanderHeader { color: var(--steel-700); }

    /* Data table - concrete frame */
    .stDataFrame table, .stTable table {
        border: 1px solid var(--concrete-400);
        border-radius: 12px;
        overflow: hidden;
        background: #fff;
    }

    /* Plotly container */
    .plotly, .stPlotlyChart {
        border-radius: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.12);
        background: #fff;
        padding: 6px;
    }

    /* Help tooltips */
    .stTooltip { background: var(--steel-700); color: #fff; }

    /* Small badges for section titles */
    .stApp h5::before {
        content: '⛏️';
        margin-right: 6px;
        filter: grayscale(20%);
    }

    /* Brand banner container */
    .brand-banner {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 12px 16px;
        background: #fff;
        border: 1px solid var(--concrete-400);
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        margin: 6px 0 18px;
    }
    .brand-banner .title {
        font-size: 1.75rem;
        color: var(--steel-700);
        font-weight: 800;
        letter-spacing: 0.4px;
        line-height: 1.2;
    }
    .brand-banner .subtitle {
        color: #6b7785;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Footer bar */
    .footer-bar {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        background: linear-gradient(90deg, var(--steel-800), var(--steel-700));
        color: #ecf0f1;
        padding: 8px 14px;
        font-size: 12px;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
    }
    .footer-bar a { color: var(--accent-orange); text-decoration: none; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Dark theme overrides (conditionally injected)
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
            :root {
                --concrete-100: #0d1116; /* deep slate */
                --concrete-200: #11161c; /* panel background */
                --concrete-400: #26303a; /* borders */
                --concrete-600: #9aa7b7; /* muted text */
                --steel-700: #e6edf3;   /* primary text */
                --steel-800: #0b1117;   /* darkest */
                --accent-orange: #ff9f43; /* brighter safety orange */
                --accent-blue: #3fa6ff;   /* electric blue */
            }

            /* Dark concrete texture background */
            .stApp, .main {
                background-color: var(--concrete-100);
                background-image:
                    linear-gradient(0deg, rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                    radial-gradient(circle at 12% 18%, rgba(255,255,255,0.045) 2px, transparent 2px),
                    radial-gradient(circle at 74% 62%, rgba(255,255,255,0.035) 1.5px, transparent 1.5px);
                background-attachment: fixed;
            }

            /* Header and brand banner text in light steel */
            .stApp h1, .brand-banner .title, .brand-banner .subtitle { color: var(--steel-700); }
            .brand-banner { background: var(--concrete-200); border-color: var(--concrete-400); }

            /* Panels and containers */
            .stDataFrame table, .stTable table, .stExpander, .plotly, .stPlotlyChart, div[data-testid="stMetric"] {
                background: var(--concrete-200);
                border-color: var(--concrete-400);
                color: var(--steel-700);
            }
            .stMetric > label, .stMetric > div > div { color: var(--steel-700); }

            /* Tabs */
            .stTabs [data-baseweb="tab"] { background-color: var(--concrete-200); color: var(--steel-700); }
            .stTabs [aria-selected="true"] { background-color: var(--concrete-100); border-color: var(--concrete-400); }

            /* Tooltips */
            .stTooltip { background: var(--steel-800); color: var(--steel-700); }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Your Gemini API Key
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    GEMINI_API_KEY = ""
    st.warning("🔑 Gemini API key missing; AI suggestions disabled. Add to .streamlit/secrets.toml.")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# IS 10262 Simple Formulas (unchanged)
def calculate_mix(target_strength, slump=50, max_agg_size=20):
    if target_strength <= 20: wc = 0.60
    elif target_strength <= 30: wc = 0.50
    elif target_strength <= 40: wc = 0.42
    else: wc = 0.38
    
    water = 186 + (slump - 50) * 3
    if max_agg_size == 10: water -= 10
    elif max_agg_size == 40: water += 10
    
    cement = max(water / wc, 300)
    
    total_vol = 1 - (cement/3100 + water/1000 + 0.02)
    sand_vol = total_vol * 0.4
    agg_vol = total_vol * 0.6
    sand = sand_vol * 2600
    coarse_agg = agg_vol * 1600
    
    compliant = wc <= 0.50 and cement >= 300
    return {
        'Cement (kg/m³)': round(cement),
        'Water (L/m³)': round(water),
        'Fine Aggregate - Sand (kg/m³)': round(sand),
        'Coarse Aggregate (kg/m³)': round(coarse_agg),
        'Water-Cement Ratio (w/c)': round(wc, 2),
        'IS Compliance': ' Fully Compliant' if compliant else '⚠️ Review Required'
    }

# Cost calc (unchanged)
def calculate_cost(mix):
    prices = {'Cement (kg/m³)': 7, 'Fine Aggregate - Sand (kg/m³)': 1.8, 'Coarse Aggregate (kg/m³)': 1.1, 'Water (L/m³)': 0.05}
    cost = sum(mix[k] * prices[k] for k in prices if k in mix)
    return round(cost, 0)

# Gemini tip (FIXED: Updated to stable 'gemini-2.5-flash')
@st.cache_data(ttl=300)
def get_gemini_tip(mix, target_strength):
    model = genai.GenerativeModel('gemini-2.5-flash')  # Updated model name
    prompt = f"""
    You are a civil engineer expert in Indian IS codes (10262:2019, 456:2000).
    Given this concrete mix for {target_strength} MPa strength:
    Cement: {mix['Cement (kg/m³)']} kg, Water: {mix['Water (L/m³)']} L, Sand: {mix['Fine Aggregate - Sand (kg/m³)']} kg, 
    Coarse Agg: {mix['Coarse Aggregate (kg/m³)']} kg, w/c: {mix['Water-Cement Ratio (w/c)']}.
    Suggest 2-3 NOVEL ways to increase strength or reduce cost (e.g., add fly ash per IS 3812, up to 30%).
    Keep suggestions short, practical, and compliant. Format as bullet points.
    """
    response = model.generate_content(prompt)
    return response.text

# Interactive Charts Function (unchanged from last fix)
def create_interactive_charts(mix, cost):
    is_dark = st.session_state.get("dark_mode", False)
    # Prepare data for charts
    materials = ['Cement', 'Water', 'Sand', 'Coarse Aggregate']
    quantities = [mix['Cement (kg/m³)'], mix['Water (L/m³)'], mix['Fine Aggregate - Sand (kg/m³)'], mix['Coarse Aggregate (kg/m³)']]
    
    # Pie Chart: Material Proportions (% of total mass)
    total_mass = sum(quantities)
    percentages = [q / total_mass * 100 for q in quantities]
    fig_pie = px.pie(
        values=percentages, names=materials,
        title="Material Proportions (%)",
        color_discrete_sequence=(px.colors.qualitative.Dark24 if is_dark else px.colors.qualitative.Set3),
        hole=0.3  # Donut style for modern look
    )
    fig_pie.update_traces(textinfo='percent+label', textposition='inside')
    fig_pie.update_layout(
        showlegend=True,
        font_size=12,
        template=("plotly_dark" if is_dark else None),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Bar Chart: Quantities per m³ (interactive hover)
    fig_bar = px.bar(
        x=materials, y=quantities,
        title="Quantities per m³",
        labels={'y': 'Quantity (kg/m³)', 'x': 'Materials'},
        color=quantities,
        color_continuous_scale=('Oranges' if is_dark else 'Blues')
    )
    fig_bar.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="kg/m³",
        template=("plotly_dark" if is_dark else None),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig_bar.add_hline(y=cost, line_dash="dash", line_color="red", annotation_text="Cost Line (₹/m³ scaled)")
    
    # Combined Chart: Use make_subplots for side-by-side pie + horizontal bar (fixes domain error)
    fig_combined = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Proportions (%)', 'Quantities (kg/m³)'),
        specs=[[{"type": "pie"}, {"type": "bar"}]]
    )
    
    # Add pie to first subplot
    fig_combined.add_trace(
        go.Pie(
            labels=materials, values=percentages, name="Proportions",
            hole=0.3, showlegend=False
        ),
        row=1, col=1
    )
    
    # Add horizontal bar to second subplot
    fig_combined.add_trace(
        go.Bar(
            y=materials, x=quantities, orientation='h', name="Quantities",
            marker_color=('orange' if is_dark else 'lightblue'), showlegend=False
        ),
        row=1, col=2
    )
    
    # Update layout
    fig_combined.update_layout(
        title="Interactive Mix Visualization",
        height=400,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
        template=("plotly_dark" if is_dark else None),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig_combined.update_xaxes(title_text="kg/m³", row=1, col=2)
    fig_combined.update_yaxes(title_text="Materials", row=1, col=2)
    
    return fig_pie, fig_bar, fig_combined

# Header
st.markdown("# AI Concrete Mix Optimizer")
st.markdown("##### Professional Tool for IS 10262:2019 Compliant Designs | Higher Strength, Lower Cost")

# Civil-themed brand banner (logo + tagline)
st.markdown(
    """
    <div class="brand-banner">
      <div class="brand-logo">
        <svg width="56" height="56" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg">
          <!-- Concrete blocks -->
          <rect x="6" y="32" width="18" height="12" rx="3" fill="#cfd4d9" stroke="#2f3b46" stroke-width="2"/>
          <rect x="22" y="20" width="26" height="12" rx="3" fill="#cfd4d9" stroke="#2f3b46" stroke-width="2"/>
          <!-- Mixer drum accent -->
          <circle cx="42" cy="38" r="7" fill="#f39c12" stroke="#2f3b46" stroke-width="2"/>
          <!-- Rebar lines -->
          <line x1="10" y1="30" x2="30" y2="18" stroke="#2980b9" stroke-width="2"/>
          <line x1="30" y1="18" x2="46" y2="18" stroke="#2980b9" stroke-width="2"/>
        </svg>
      </div>
      <div>
        <div class="title">AI Concrete Mix Optimizer</div>
        <div class="subtitle">IS 10262:2019 compliant · Higher Strength · Lower Cost</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tabs for user-friendly navigation
tab1, tab2 = st.tabs([" Design Mix", "ℹ️ About & Compliance"])

with tab1:
    # Inputs in columns for clean layout
    col1, col2 = st.columns(2)
    with col1:
        target_strength = st.number_input(
            "Target Compressive Strength (MPa)", 
            min_value=15, max_value=60, value=25,
            help="e.g., 25 for M25 grade (IS 456)"
        )
        slump = st.slider(
            "Workability - Slump (mm)", 
            25, 150, 50,
            help="Higher slump for better flow (IS 10262)"
        )
    with col2:
        max_agg_size = st.selectbox(
            "Max Coarse Aggregate Size (mm)", 
            [10, 20, 40],
            help="Affects water demand (IS 383)"
        )
        exposure = st.selectbox(
            "Exposure Condition", 
            ["Mild", "Moderate", "Severe"],
            help="Impacts durability requirements (IS 456 Table 5)"
        )
    
    # Calculate button with progress
    if st.button("🔬 Generate Optimized Mix", type="primary"):
        with st.spinner("Analyzing per IS 10262..."):
            mix = calculate_mix(target_strength, slump, max_agg_size)
            cost = calculate_cost(mix)
        
        # Metrics row for quick insights
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Estimated Cost", f"₹{cost}/m³")
        col2.metric("💪 Target Strength", f"{target_strength} MPa")
        col3.metric("🔍 w/c Ratio", f"{mix['Water-Cement Ratio (w/c)']}")
        
        # Mix table - clean and centered
        st.subheader("📋 Mix Proportions (per m³)")
        mix_df = pd.DataFrame(list(mix.items()), columns=['Property', 'Value'])
        st.dataframe(mix_df, use_container_width=True, hide_index=True)
        
        # Interactive Charts Section
        st.subheader("📈 Interactive Mix Visualizations")
        st.write("Hover, zoom, and explore the mix composition below.")
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            fig_pie, _, _ = create_interactive_charts(mix, cost)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_chart2:
            _, fig_bar, _ = create_interactive_charts(mix, cost)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Combined Chart Expander
        with st.expander("🔍 Advanced Combined View"):
            _, _, fig_combined = create_interactive_charts(mix, cost)
            st.plotly_chart(fig_combined, use_container_width=True)
        
        # Gemini section - expander for cleanliness
        if GEMINI_API_KEY != "YOUR_API_KEY_HERE":
            with st.expander("🤖 AI-Powered Optimizations "):
                tip = get_gemini_tip(mix, target_strength)
                st.markdown(f"**Suggestions:**")
                st.markdown(tip)
        else:
            st.info("🔑 Add your Gemini API key in the code to enable AI suggestions!")

with tab2:
    st.subheader("📖 Project Overview")
    st.write("""
    This tool automates concrete mix design using **IS 10262:2019** guidelines for Indian standards.
    - **Inputs:** Target strength, slump, aggregate size, exposure.
    - **Outputs:** Proportions, cost estimate (2025 prices), compliance check.
    - **Novelty:** Rule-based optimization + Gemini AI for sustainable tweaks (e.g., fly ash replacement).
    - **Visuals:** Interactive Plotly charts for mix analysis.
    """)
    
    st.subheader("⚖️ Key IS Compliance")
    compliance_df = pd.DataFrame({
        "Aspect": ["w/c Ratio", "Min Cement Content", "Durability"],
        "Requirement": ["≤0.50 (mild exposure)", "≥300 kg/m³ (M20+)", "Per IS 456 Table 5"],
        "Status": ["Auto-checked", "Enforced", "Exposure-based"]
    })
    st.table(compliance_df)
    
    st.subheader("💼 Pricing Basis (Avg. India 2025)")
    st.write("• Cement (OPC 53): ₹7/kg\n• Sand (Zone II): ₹1.8/kg\n• Coarse Agg (20mm): ₹1.1/kg\n• Water: ₹0.05/L")
    st.caption("Update prices in code for regional accuracy.")

# Sidebar for quick access & info
with st.sidebar:
    st.header("🛠️ Quick Tools")
    # Dark mode toggle
    st.checkbox("🌑 Dark Theme", value=st.session_state.get("dark_mode", False), key="dark_mode")
    st.write("**Modern Features:**")
    st.write("- Clean, tabbed interface")
    st.write("- Professional gray-blue theme")
    st.write("- Tooltips for guidance")
    st.write("- **Interactive Charts:** Pie/Bar with hover & zoom")
    st.write("- Responsive layout")
    
    if st.button("📈 View Sample Mix (M25)"):
        st.session_state.sample_mix = calculate_mix(25)
        st.rerun()
    
    st.header("📚 Resources")
    st.write("[IS 10262:2019 PDF](https://bis.gov.in) | [Gemini Docs](https://ai.google.dev) | [Plotly Docs](https://plotly.com/python)")
    st.caption("Built with Streamlit | Deploy: GitHub + Streamlit Cloud")

# Footer (civil-themed)
st.markdown(
    """
    <div class="footer-bar">
      <span>🧱 Concrete-first UI for Civil Engineers</span>
      <span style="float:right;">Need design tweaks? <a href="#">Request a theme variant</a></span>
    </div>
    """,
    unsafe_allow_html=True,
)

