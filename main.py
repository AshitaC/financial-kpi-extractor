import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re
from data_extractor import extract

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Financial KPI Extractor",
    page_icon="💹",
    layout="centered"
)

# ---- HIDE STREAMLIT ELEMENTS & CUSTOM CSS ----
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    .title-heading {
        text-align: center;
        font-size: 32px;
        font-weight: 600;
        margin-bottom: 0.3rem;
        color: #1f1f1f;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #5a5a5a;
        margin-bottom: 2rem;
    }
    .centered-success {
        text-align: center;
        color: #007026;
        padding: 10px;
        background-color: #dff0d8;
        border-radius: 5px;
        margin-top: 10px;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .section-header {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 10px;
        color: #333;
    }
    .chart-title {
        text-align: center;
        font-size: 14px;
        font-weight: 500;
        color: #666;
        margin-bottom: 5px;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


# ---- HELPER: CLEAN DATA ----
def parse_value(val_str):
    try:
        clean_str = re.sub(r'[^\d.]', '', str(val_str))
        return float(clean_str) if clean_str else 0.0
    except:
        return 0.0


# ---- HELPER: CREATE CHART ----
def create_chart(actual, estimated):
    fig = go.Figure()

    # Estimated Bar (Context - Grey)
    fig.add_trace(go.Bar(
        x=['Est.'],
        y=[estimated],
        name='Expected',
        marker_color='#cfcfcf',
        text=[f"{estimated}"],
        textposition='auto',
        textfont=dict(color='black')
    ))

    # Actual Bar (Focus - Corporate Blue)
    fig.add_trace(go.Bar(
        x=['Act.'],
        y=[actual],
        name='Actual',
        marker_color='#004e82',
        text=[f"{actual}"],
        textposition='auto',
        textfont=dict(color='white')
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=10),
        height=200,
        showlegend=False,
        yaxis_title=None,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


# ---- TITLE SECTION ----
st.markdown('<div class="title-heading">Financial KPI Extractor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Extract Revenue & EPS (Actual vs Expected) from any financial article</div>',
            unsafe_allow_html=True)

# ---- SESSION STATE INITIALIZATION ----
if "paragraph" not in st.session_state:
    st.session_state.paragraph = ""
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

# --- COMPLEX SAMPLE TEXT (TESLA Q3) ---
sample_text = (
    "Tesla reported third-quarter earnings Wednesday that topped analysts’ estimates even as revenue came in just shy of expectations. "
    "The stock popped roughly 17% in Thursday morning trading."
    "Here’s what the company reported compared with what Wall Street was expecting, based on a survey of analysts by LSEG:"
    "Earnings per share: 72 cents, adjusted vs. 58 cents expected"
    "Revenue: $25.18 billion vs. $25.37 billion expected"
    "Revenue increased 8% in the quarter from $23.35 billion a year earlier. Net income rose to about $2.17 billion, or 62 cents a share, from $1.85 billion, or 53 cents a share, a year ago."
    "Profit margins were bolstered by $739 million in automotive regulatory credit revenue during the quarter."
)

# ---- MAIN CARD ----
with st.container(border=True):
    st.write("###  Enter financial news or earnings report text")

    # Text Area
    text_input = st.text_area(
        "Paste article text below:",
        value=st.session_state.paragraph,
        height=200,
        placeholder="Enter earnings report or financial article here...",
        label_visibility="collapsed"
    )
    # Sync text input with session state
    st.session_state.paragraph = text_input

    # BUTTONS
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Use Sample Text", use_container_width=True):
            st.session_state.paragraph = sample_text
            st.session_state.extracted_data = None  # Clear previous data on new sample load
            st.rerun()
    with col2:
        extract_clicked = st.button(" Extract KPIs", use_container_width=True, type="primary")

    # ---- EXTRACTION LOGIC ----
    if extract_clicked:
        if st.session_state.paragraph.strip():
            with st.spinner("Analyzing financial data..."):
                try:
                    # Perform extraction
                    data = extract(st.session_state.paragraph)
                    # SAVE TO SESSION STATE (This fixes the reset issue)
                    st.session_state.extracted_data = data
                except Exception as e:
                    st.error(f"⚠ Unable to extract data: {e}")
        else:
            st.warning("⚠ Please enter a financial paragraph first.")

    # ---- DISPLAY LOGIC (Run this if data exists in memory) ----
    if st.session_state.extracted_data:
        data = st.session_state.extracted_data

        # Build DataFrame
        df = pd.DataFrame({
            'Measure': ['Revenue', 'EPS'],
            'Estimated': [
                data.get('revenue_expected', '0'),
                data.get('eps_expected', '0')
            ],
            'Actual': [
                data.get('revenue_actual', '0'),
                data.get('eps_actual', '0')
            ]
        })

        # 1. Success Message
        st.markdown('<div class="centered-success">✔ Data extraction complete!</div>', unsafe_allow_html=True)

        # 2. Table
        st.markdown('<div class="section-header">Extracted Financial KPIs</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 3. Charts
        st.markdown('<div class="section-header">Performance Visualization</div>', unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)
        rev_act = parse_value(data.get('revenue_actual', 0))
        rev_est = parse_value(data.get('revenue_expected', 0))
        eps_act = parse_value(data.get('eps_actual', 0))
        eps_est = parse_value(data.get('eps_expected', 0))

        with chart_col1:
            st.markdown('<div class="chart-title">Revenue (Billions)</div>', unsafe_allow_html=True)
            fig_rev = create_chart(rev_act, rev_est)
            st.plotly_chart(fig_rev, use_container_width=True, config={'displayModeBar': False})

        with chart_col2:
            st.markdown('<div class="chart-title">EPS (Cents/Dollars)</div>', unsafe_allow_html=True)
            fig_eps = create_chart(eps_act, eps_est)
            st.plotly_chart(fig_eps, use_container_width=True, config={'displayModeBar': False})

        # 4. Download Button
        st.write("")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="financial_kpis.csv",
            mime="text/csv",
            use_container_width=True
        )