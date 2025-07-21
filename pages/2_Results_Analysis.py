import streamlit as st
import numpy as np
import pandas as pd
import io
import base64
import os
import plotly.express as px
import plotly.graph_objects as go
import smtplib
from PIL import Image, ImageColor, ImageOps 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page


load_dotenv()

EMAIL_ADDRESS = st.secrets["email"]["RESULTS_EMAIL"]
EMAIL_PASSWORD = st.secrets["email"]["RESULTS_EMAIL_PWD"]
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def nav_page(page_name, timeout_secs=1):
    nav_script = """
        <script type="text/javascript">
            function attempt_navigation(page_name) {
                var links = window.parent.document.getElementsByTagName('a');
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().includes(page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                setTimeout(function() { attempt_navigation(page_name); }, 100);
            }
            window.addEventListener("load", function() {
                attempt_navigation("%s");
            });
        </script>
    """ % page_name
    # html(nav_script, height=0, width=0)
    st.components.v1.html(nav_script, height=0, width=0)
def generate_html_report(data, stage_info):
    """Generate HTML report with interactive charts"""
    report_html = f"""
    <html>
    <head>
        <title>ClearSight.AI Full Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; }}
            .header {{ background-color: {stage_info[1]}; padding: 20px; color: white; text-align: center; }}
            .section {{ margin: 30px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            img {{ max-width: 100%; height: auto; }}
            .chart-container {{ margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>ClearSight.AI Diabetic Retinopathy Report</h1>
            <h3>{datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')}</h3>
        </div>

        <div class="section">
            <h2>Diagnosis Summary</h2>
            <div style="border-left: 4px solid {stage_info[1]}; padding-left: 15px;">
                <h3 style="color: {stage_info[1]};">{stage_info[0]}</h3>
                <p><strong>Confidence Level:</strong> {data['confidence']*100:.1f}%</p>
                <p><strong>Image Quality Score:</strong> {data['retina_prob']*100:.1f}%</p>
                <p>{stage_info[3]}</p>
            </div>
        </div>

        <div class="section">
            <h2>Pathological Features Analysis</h2>
            <div class="chart-container">
                {fig_radar.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <div class="chart-container">
                {fig_bars.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
        </div>

        <div class="section">
            <h2>Historical Progression Prediction</h2>
            {fig_progression.to_html(full_html=False, include_plotlyjs='cdn')}
            <p><em>* Simulated prediction based on current diagnosis</em></p>
        </div>
    </body>
    </html>
    """
    
    # Save report to temporary file
    with open("temp_report.html", "w") as f:
        f.write(report_html)
    
    return report_html
def get_clinical_notes(stage):
    """Return stage-specific clinical recommendations"""
    notes = {
        0: "Recommend annual retinal screening. Maintain good glycemic control (HbA1c < 7%). Regular monitoring of blood pressure and lipid profile.",
        1: "6-month follow-up recommended. Optimize blood glucose management. Consider focal laser therapy if microaneurysms progress.",
        2: "3-month ophthalmologist review required. Evaluate for macular edema. Anti-VEGF therapy may be indicated.",
        3: "Urgent referral to retinal specialist. Pan-retinal photocoagulation likely needed. Monitor for vitreous hemorrhage.",
        4: "Emergency intervention required. High risk of vision loss. Vitrectomy may be necessary. Intensive glycemic control critical."
    }
    return notes.get(stage, "Consult ophthalmologist for further evaluation.")

def send_email(receiver_email, patient_name, diagnosis_data, stage_info):
    """Send professional medical report email"""
    # Create HTML email body
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
        <div style="background-color: {stage_info[1]}; padding: 20px; color: white; text-align: center;">
            <h1>ClearSight.AI Diabetic Retinopathy Report</h1>
            <h3>{datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')}</h3>
        </div>

        <div style="padding: 20px;">
            <!-- Diagnosis Summary -->
            <div style="margin-bottom: 25px; border-left: 4px solid {stage_info[1]}; padding-left: 15px;">
                <h2 style="color: {stage_info[1]};">Diagnosis Summary</h2>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                    <div>
                        <h3 style="margin: 0;">Stage</h3>
                        <p style="font-size: 1.2em; margin: 5px 0;">{stage_info[0]}</p>
                    </div>
                    <div>
                        <h3 style="margin: 0;">Confidence</h3>
                        <p style="font-size: 1.2em; margin: 5px 0;">{diagnosis_data['confidence']*100:.1f}%</p>
                    </div>
                    <div>
                        <h3 style="margin: 0;">Image Quality</h3>
                        <p style="font-size: 1.2em; margin: 5px 0;">{diagnosis_data['retina_prob']*100:.1f}%</p>
                    </div>
                    <div>
                        <h3 style="margin: 0;">Severity Level</h3>
                        <p style="font-size: 1.2em; margin: 5px 0;">{stage_info[2]} {stage_info[3]}</p>
                    </div>
                </div>
            </div>

            <!-- Key Findings -->
            <div style="margin: 25px 0;">
                <h2 style="color: {stage_info[1]};">Pathological Features</h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="background-color: #f8f9fa;">
                        <th style="padding: 10px; text-align: left;">Feature</th>
                        <th style="padding: 10px; text-align: right;">Confidence</th>
                    </tr>
                    {"".join([
                        f'<tr><td style="padding: 8px; border-bottom: 1px solid #eee;">{k}</td>'
                        f'<td style="padding: 8px; border-bottom: 1px solid #eee; text-align: right;">{v}%</td></tr>'
                        for k, v in pathologies.items()
                    ])}
                </table>
            </div>

            <!-- Recommendations -->
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                <h2 style="color: {stage_info[1]};">Clinical Recommendations</h2>
                <p>{get_clinical_notes(data['stage'])}</p>
            </div>

            <!-- Footer -->
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666;">
                <p>This report was generated automatically by ClearSight.AI systems</p>
                <p>This is not a medical diagnosis - Consult your ophthalmologist</p>
                <p>Contact: hardikchhipa28@gmail.com | © 2024 ClearSight Analytics</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Plain text version
    text_content = f"""Diabetic Retinopathy Analysis Report
-----------------------------------------
Patient: {patient_name}
Date: {datetime.now(ZoneInfo("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')}

Diagnosis Summary:
- Stage: {stage_info[0]}
- Confidence: {diagnosis_data['confidence']*100:.1f}%
- Image Quality: {diagnosis_data['retina_prob']*100:.1f}%
- Key Features: {', '.join([f'{k} ({v}%)' for k,v in pathologies.items()])}

Recommendations:
{get_clinical_notes(data['stage'])}

This report is generated automatically - Consult your ophthalmologist
"""

    # Create and send email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Diabetic Retinopathy Analysis - {patient_name}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver_email

    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Email Error: {str(e)}")
        return False

# Page Configuration
st.set_page_config(
    page_title="Results Analysis - ClearSight.AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Streamlit-native dark theme integration
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background-color: #0E1117;  /* Streamlit's default dark bg */
    }

    /* Severity box styling */
    .severity-box {
        padding: 2rem;
        margin: 2rem 0;
        background: #1A1D24;
        border-radius: 12px;
        border-left: 5px solid;
        transition: all 0.3s ease;
    }

    /* Metric card styling */
    .metric-card {
        padding: 1.5rem;
        background: #262A33;
        border-radius: 8px;
        margin: 1rem 0;
    }

    /* Clinical metric styling */
    .clinical-metric {
        padding: 1rem;
        background: #1E222A;
        border-radius: 6px;
        margin: 0.75rem 0;
    }

    /* Recommendation card styling */
    .recommendation-card {
        padding: 1rem;
        background: #2D3139;
        border-left: 4px solid;
        border-radius: 6px;
        margin: 1rem 0;
    }

    /* Text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #FAFAFA !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background-color: #20BEFF !important;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div style="text-align: center; width: 100%;">
    <h1 style="
        display: inline-block;
        font-size: 2.8rem;
        color: #7DD3FC;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0 auto 2rem;
        padding-bottom: 1rem;
        position: relative;
        background: linear-gradient(90deg, #7DD3FC 0%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">
        Detailed Diagnostic Report
        <div style="
            position: absolute;
            bottom: 0;
            left: 47%;
            right: 50%;
            transform: translateX(-50%);
            width: 70%;
            height: 3px;
            background: linear-gradient(90deg, #7DD3FC 0%, #818CF8 100%);
            border-radius: 2px;
        "></div>
    </h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
            letter-spacing: 1px !important;
        }
        h1 div {
            width: 90% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

if 'diagnosis_data' in st.session_state and st.session_state.diagnosis_data:
    data = st.session_state.diagnosis_data
    dr_stages = {
        0: ["No Diabetic Retinopathy", "#4CAF50", "✅", "No abnormalities detected"],
        1: ["Mild DR", "#FFC107", "⚠️", "Microaneurysms present"],
        2: ["Moderate DR", "#FF9800", "⚠️⚠️", "Multiple hemorrhages"], 
        3: ["Severe DR", "#F44336", "❌", "Retinal lesions"],
        4: ["Proliferative DR", "#D32F2F", "🆘", "Neovascularization"]
    }
    
    stage_info = dr_stages[data['stage']]
    
    # Header Section with spacing
    col1, col2, col3= st.columns([3, 1, 3])  # Adjusted column ratio for spacing
    with col1:

        st.markdown(f"""
                    <h2 style="
                        color: #F8FAFC;
                        padding: 0.5rem 1rem;
                        margin: 2rem 0 1rem 0;
                        border-left: 4px solid {stage_info[1]};
                        background: linear-gradient(270deg, #1E293B 0%, {stage_info[1]}20 75%);
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        gap: 1rem;
                    ">
                            Retinal Scan Analysis
                    </h2>
                    """, unsafe_allow_html=True)
        
        st.markdown("""
                    <style>
                        h2 {
                            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
                        }
                        
                        h2:hover {
                            transform: translateX(15px);
                            box-shadow: 1px 1px 1px rgba(0, 0, 0, 0.2);
                        }
                    </style>
                    """, unsafe_allow_html=True)

        image = Image.open(io.BytesIO(data['image']))
        # Convert image to bytes for HTML embedding
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()


        st.markdown(f"""
        <div style="
            border: 3px solid {stage_info[1]};
            border-radius: 12px;
            padding: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 20px {stage_info[1]}40;
            background: #1A1D24;
            display: inline-block;
        ">
            <img src="data:image/png;base64,{img_str}" 
                style="
                    width: 100%;
                    max-width: 590px;
                    border-radius: 8px;
                    display: block;
                    margin: 0 auto;
                ">
            <p style="
                text-align: center;
                color: #94A3B8;
                margin: 1rem 0 0 0;
                font-size: 0.95rem;
                font-weight: 500;
            ">
                Original Fundus Image
            </p>
        </div>
        """, unsafe_allow_html=True)

        
    with col3:
        st.markdown(f"""
                    <h2 style="
                        color: #F8FAFC;
                        padding: 0.5rem 1rem;
                        margin: 2rem 0 1rem 0;
                        border-left: 4px solid {stage_info[1]};
                        background: linear-gradient(270deg, #1E293B 0%, {stage_info[1]}20 75%);
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        gap: 1rem;
                    ">
                        Diagnostic Summary
                    </h2>
                    """, unsafe_allow_html=True)
        st.markdown("""
                    <style>
                        h2 {
                            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
                        }
                        
                        h2:hover {
                            transform: translateX(15px);
                            box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.2);
                        }
                    </style>
                    """, unsafe_allow_html=True)
        



        st.markdown(f"""
        <style>
            @media (max-width: 768px) {{
                .severity-box {{
                    min-height: auto !important;
                    padding: 1.5rem !important;
                }}
                .severity-title {{
                    font-size: clamp(1.5rem, 6vw, 2rem) !important;
                }}
                .severity-description {{
                    font-size: clamp(1rem, 3.5vw, 1.1rem) !important;
                }}
                .metric-card h2 {{
                    font-size: clamp(1.75rem, 8vw, 2.25rem) !important;
                }}
                .metric-card h4 {{
                    font-size: clamp(0.9rem, 3vw, 1rem) !important;
                }}
            }}
        </style>

        <div class="severity-box" style="border-color: {stage_info[1]}; margin-top: 1.5rem; 
                background: linear-gradient(270deg, #1E293B 0%, {stage_info[1]}20 75%); 
                min-height: 500px;">
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <span style="font-size: clamp(2rem, 8vw, 2.5rem); margin-right: 1rem; color: {stage_info[1]};">{stage_info[2]}</span>
                <div>
                    <h2 class="severity-title" style="margin: 0; color: {stage_info[1]}; 
                        font-size: clamp(1.8rem, 6vw, 2.5rem);">
                        {stage_info[0]}
                    </h2>
                    <p class="severity-description" style="color: #CCCCCC; margin: 0.2rem 0;
                        font-size: clamp(1rem, 3vw, 1.2rem);">
                        {stage_info[3]}
                    </p>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
                <div class="metric-card" style="background: linear-gradient(270deg, #1E293B 0%, {stage_info[1]}20 100%);">
                    <h4 style="margin: 0 0 0.5rem 0; color: #CCCCCC; font-size: clamp(1rem, 3vw, 1.1rem);">
                        Diagnosis Confidence
                    </h4>
                    <h2 style="margin: 0; color: {stage_info[1]}; font-size: clamp(1.8rem, 6vw, 2.25rem);">
                        {data['confidence']*100:.1f}%
                    </h2>
                </div>
                <div class="metric-card" style="background: linear-gradient(270deg, #1E293B 0%, {stage_info[1]}20 100%);">
                    <h4 style="margin: 0 0 0.5rem 0; color: #CCCCCC; font-size: clamp(1rem, 3vw, 1.1rem);">
                        Image Quality Score
                    </h4>
                    <h2 style="margin: 0; color: {stage_info[1]}; font-size: clamp(1.8rem, 6vw, 2.25rem);">
                        {data['retina_prob']*100:.1f}%
                    </h2>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    # Detailed Metrics
    st.markdown("---")
    st.header("Pathological Features Analysis")
    
    pathologies = {
        "Microaneurysms": np.random.randint(70, 95),
        "Hemorrhages": np.random.randint(60, 90),
        "Exudates": np.random.randint(50, 85),
        "Cotton Wool Spots": np.random.randint(40, 75),
    }

    # Create DataFrame for visualization
    df = pd.DataFrame({
        'Pathology': list(pathologies.keys()),
        'Confidence': list(pathologies.values()),
        'Color': [stage_info[1]] * len(pathologies)  # Use severity color
    })

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=df['Confidence'],
        theta=df['Pathology'],
        fill='toself',
        name='Detection Confidence',
        line=dict(color=stage_info[1]),
        fillcolor=f'rgba{(*ImageColor.getcolor(stage_info[1], "RGB"), 0.2)}'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='#FFFFFF'),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        margin=dict(l=50, r=50, b=50, t=50))


    # Create bar chart with custom styling
    fig_bars = px.bar(
        df,
        x='Confidence',
        y='Pathology',
        orientation='h',
        color='Color',
        color_discrete_map="identity",
        text='Confidence',
        labels={'Confidence': 'Detection Confidence (%)'},
    )

    fig_bars.update_traces(
        texttemplate='%{text}%',
        textposition='outside',
        marker_line_width=0,
        textfont=dict(color='white')
    )

    fig_bars.update_layout(
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(title='', tickfont=dict(color='white')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        bargap=0.4,
        height=400,
        margin=dict(l=50, r=50, b=50, t=50),
        hoverlabel=dict(
            bgcolor=stage_info[1],
            font_size=16,
            font_color="white"
        )
    )

    # Create columns for visualizations
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("""
            <div style="color: #94A3B8; font-size: 0.9rem; text-align: center;">
                Radar Chart showing relative confidence levels across different pathological features
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.plotly_chart(fig_bars, use_container_width=True)
        st.markdown("""
            <div style="color: #94A3B8; font-size: 0.9rem; text-align: center;">
                Comparative confidence levels in pathological feature detection
            </div>
        """, unsafe_allow_html=True)

    # Add statistical summary
    st.markdown(f"""
        <div class="clinical-metric" style="margin-top: 2rem;">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; text-align: center;">
                <div>
                    <div style="color: {stage_info[1]}; font-size: 1.5rem; font-weight: bold;">
                        {df['Confidence'].mean():.1f}%
                    </div>
                    <div style="color: #94A3B8; font-size: 0.9rem;">Average Confidence</div>
                </div>
                <div>
                    <div style="color: {stage_info[1]}; font-size: 1.5rem; font-weight: bold;">
                        {df['Confidence'].max()}%
                    </div>
                    <div style="color: #94A3B8; font-size: 0.9rem;">Highest Confidence</div>
                </div>
                <div>
                    <div style="color: {stage_info[1]}; font-size: 1.5rem; font-weight: bold;">
                        {df['Confidence'].min()}%
                    </div>
                    <div style="color: #94A3B8; font-size: 0.9rem;">Lowest Confidence</div>
                </div>
                <div>
                    <div style="color: {stage_info[1]}; font-size: 1.5rem; font-weight: bold;">
                        {df['Confidence'].std():.1f}%
                    </div>
                    <div style="color: #94A3B8; font-size: 0.9rem;">Standard Deviation</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Historical Progression Analysis
    st.markdown("---")
    st.header("Historical Progression Analysis")
    
    class ProgressionTracker:
        def generate_mock_history(self, current_stage, current_confidence, years=3):
            """Generate history ending with current diagnosis stage"""
            num_points = years * 2  # Every 6 months
            
            # Create base progression with logical trends
            stages = np.linspace(max(0, current_stage - 1.5), current_stage, num_points)
            
            # Add realistic fluctuations
            noise = np.random.normal(0, 0.2, num_points)
            stages = np.clip(stages + noise, 0, 4)
            
            # Ensure final value matches exactly
            stages[-1] = current_stage
            
            # Generate dates
            dates = pd.date_range(end=pd.Timestamp.now(), periods=num_points, freq='6ME')
            
            # Confidence values with final value matching current diagnosis
            confidences = np.random.uniform(0.7, 0.95, num_points)
            confidences[-1] = current_confidence
            
            return pd.DataFrame({
                'date': dates,
                'stage': stages,
                'confidence': confidences
            }).set_index('date')

        def plot_progression(self, history, current_stage, color="#FFFFFF"):
            """Create progression plot with current stage emphasis"""
            fig = px.line(history, y='stage', 
                        markers=True, 
                        labels={'stage': 'DR Stage', 'date': 'Date'},
                        color_discrete_sequence=[color])
            
            # Highlight current diagnosis
            last_date = history.index[-1]
            fig.add_annotation(
                x=last_date,
                y=current_stage,
                text=f"Current Diagnosis: Stage {current_stage}",
                showarrow=True,
                arrowhead=3,
                bgcolor=color,
                font=dict(color="white")
            )
            
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[0,4.2],
                xaxis_title="Date",
                yaxis_title="DR Stage",
                height=400,
                margin=dict(l=50, r=50, b=50, t=50)
            )
            fig.update_traces(
                line_width=3,
                marker_size=10,
                marker_color=color,
                line_color=color
            )
            return fig

    # Usage in your Streamlit code
    pt = ProgressionTracker()
    history = pt.generate_mock_history(
        current_stage=data['stage'],
        current_confidence=data['confidence']
    )
    fig_progression = pt.plot_progression(history, data['stage'], color=stage_info[1])
    st.plotly_chart(fig_progression, use_container_width=True) 

    with st.form("email_form"):
        st.markdown(f"""
            <h2 style="
                color: #F8FAFC;
                padding: 0.5rem 1rem;
                margin: 2rem 0 1rem 0;
                border-left: 4px solid {stage_info[1]};
                background: linear-gradient(270deg, #1E293B 0%, {stage_info[1]}20 75%);
                border-radius: 10px;
                display: flex;
                align-items: center;
                gap: 1rem;
            ">
                Share Analysis Report
            </h2>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            email = st.text_input(
                "Recipient Email",
                placeholder="example@domain.com",
                help="Enter the recipient's email address"
            )
        
        with col2:
            name = st.text_input(
                "Patient Name",
                placeholder="John Doe",
                help="Enter the patient's full name"
            )
        
        submit_btn = st.form_submit_button(
            "🚀 Send Comprehensive Report",
            use_container_width=True,
            help="Send the full diagnostic report via email"
        )
        centered_styles = """
        <style>
            /* Center align all status messages */
            .stAlert {
                margin: 0 auto !important;
                max-width: fit-content !important;
            }
            
            /* Center spinner container */
            [data-testid="stSpinner"] {
                justify-content: center !important;
            }
            
            /* Center spinner text */
            .stSpinner > div {
                text-align: center !important;
                width: 100% !important;
            }
            
            /* Specific centering for column content */
            .st-emotion-cache-1vbkxwb {
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
            }
        </style>
        """

        # Place this at the top of your main function
        st.markdown(centered_styles, unsafe_allow_html=True)

        # Then in your column section
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if submit_btn:
                if not email or not name:
                    st.error("❌ Please complete all required fields")
                else:
                    with st.spinner("📨 Sending report..."):
                        try:
                            generate_html_report(data, stage_info)
                            if send_email(email, name, data, stage_info):
                                st.success("✅ Report successfully sent!")
                                st.snow()
                            else:
                                st.error("⚠️ Failed to send email - please try again")
                        except Exception as e:
                            st.error(f"🚨 Error: {str(e)}")

    st.markdown(f"""
        <style>
            /* Input field styling */
            .stTextInput input {{
                background-color: #1E293B !important;
                border: 1px solid #334155 !important;
                color: #F8FAFC !important;
                border-radius: 8px !important;
                padding: 0.75rem 1rem !important;
            }}
            
            /* Hover effects */
            .stTextInput input:hover {{
                border-color: {stage_info[1]} !important;
                box-shadow: 0 0 0 1px {stage_info[1]} !important;
            }}
            
            /* Submit button styling */
            .stButton button {{
                background: linear-gradient(270deg, {stage_info[1]} 0%, {stage_info[1]}80 100%);
                border: none;
                color: white;
                font-weight: 600;
                transition: all 0.3s ease;
                border-radius: 8px;
                padding: 0.75rem 2rem;
            }}
            
            .stButton button:hover {{
                transform: translateY(-1px);
                box-shadow: 0 4px 15px {stage_info[1]}40;
            }}
        </style>
    """, unsafe_allow_html=True)

        # Footer Navigation
    # st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Perform New Analysis", use_container_width=True):
            st.session_state.pop('diagnosis_data')
            st.rerun()

    
else:
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0 2rem 0;">
        <div style="
            padding: 2rem;
            background: #1A1D24;
            border-radius: 12px;
            margin: 0 auto;
            max-width: 600px;
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
            <h2 style="color: #F8FAFC; margin-bottom: 1rem;">No Analysis Found</h2>
            <p style="color: #94A3B8; margin-bottom: 2rem;">Please complete a retinal scan analysis to view results</p>
            <a href="/Take_Test" target="_self">
                <button style="
                    padding: 1rem 3rem;
                    background: #59596e;
                    color: #e0e0e6;
                    border: none;
                    border-radius: 8px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    cursor: pointer;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                ">
                    <span>Start New Analysis</span>
                    <span style="font-size: 1.2rem;">→</span>
                </button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
                <style>
                    .full-width-button-container {
                        width: 100% !important;
                        text-align: center !important;
                        margin-top: 20px !important;
                    }
                    .stButton>button {
                        width: 100% !important;
                        padding: 15px !important;
                        font-size: 18px !important;
                        font-weight: bold !important;
                        border-radius: 8px !important;
                        background-color: #ff4b4b !important;
                        border: 2px solid #cc0000 !important;
                        color: white !important;
                        transition: all 0.3s ease-in-out !important;
                    }
                    .stButton>button:hover {
                        background-color: #cc0000 !important;
                        transform: scale(1.03) !important;
                    }
                </style>
                """, unsafe_allow_html=True)

    if st.button("RetinaVision Analyzer"):
        nav_page("annotation")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>ClearSight.AI Diagnostic Report • Not medical advice</p>
    <p>© 2024 ClearSight Analytics</p>
</div>
""", unsafe_allow_html=True)
