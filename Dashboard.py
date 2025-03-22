import streamlit as st

# Set page config
st.set_page_config(
    page_title="ClearSight.AI - Diabetic Retinopathy Detection",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Function to toggle theme
def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# Theme toggle button in sidebar
with st.sidebar:
    st.button('🌓 Toggle Theme', on_click=toggle_theme)

# Dynamic CSS based on theme
theme_css = f"""
<style>
    :root {{
        --primary-color: {'#2c3e50' if st.session_state.theme == 'light' else '#ffffff'};
        --background-color: {'#ffffff' if st.session_state.theme == 'light' else '#2c3e50'};
        --card-bg: {'#f8f9fa' if st.session_state.theme == 'light' else '#34495e'};
        --border-color: {'#e0e7f1' if st.session_state.theme == 'light' else '#40556e'};
        --text-color: {'#2c3e50' if st.session_state.theme == 'light' else '#ecf0f1'};
        --accent-color: {'#3498db' if st.session_state.theme == 'light' else '#1abc9c'};
    }}

    * {{
        font-family: 'Poppins', sans-serif;
        transition: background-color 0.3s, color 0.3s;
    }}

    body {{
        background-color: var(--background-color);
        color: var(--text-color);
    }}

    .medical-header {{
        font-size: 3rem !important;
        color: var(--primary-color) !important;
        text-align: center;
        margin: 2rem 0;
        font-weight: 700;
    }}

    .info-card {{
        background: var(--card-bg);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}

    .stat-badge {{
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem;
        border-left: 4px solid var(--accent-color);
    }}

    .severity-scale {{
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        gap: 1rem;
    }}

    .stage-card {{
        flex: 1;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 500;
    }}

    .research-paper {{
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;

    }}

    .clearsight-gradient {{
    font-size: 4.5rem !important;
    background: linear-gradient(45deg, #eff6ee, #9197ae, #273043);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-weight: 700;
    text-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }}
    
    h3.clearsight-gradient {{
    font-size: 2rem !important; /* Adjust this size as needed */
    font-weight: 600;
    }}

    @media (max-width: 768px) {{
        .severity-scale {{
            flex-direction: column;
        }}
        .stage-card {{
            width: 100%;
            margin-bottom: 1rem;
        }}
    }}
</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="clearsight-gradient">ClearSight.AI</h1>', unsafe_allow_html=True)
st.markdown("""
<h3 class="clearsight-gradient">
Advanced AI Screening for Early Detection of Diabetic Retinopathy
</h3>
""", unsafe_allow_html=True)

# What is Diabetic Retinopathy Section
with st.container():
    st.markdown("""
    <div class="info-card">
        <h2>👁️ Understanding Diabetic Retinopathy</h2>
        <p style='font-size: 1.1rem; line-height: 1.8;'>
        Diabetic Retinopathy (DR) is a diabetes complication affecting retinal blood vessels, 
        being the leading cause of blindness in working-age adults (20-65 years). 
        <strong>Early detection through regular screening</strong> is crucial as symptoms often 
        appear only when significant damage has occurred.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Key Statistics Grid
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="stat-badge">
        <h3>103 Million</h3>
        <p>Global DR Patients (WHO 2023 Report)</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-badge">
        <h3>1 in 3</h3>
        <p>Diabetics Develop DR (IDF Diabetes Atlas 2024)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-badge">
        <h3>50%</h3>
        <p>Undiagnosed Cases (Global Eye Health Survey 2023)</p>
    </div>
    """, unsafe_allow_html=True)

# Dangers of DR Section
with st.container():
    st.markdown("""
    <div class="info-card">
        <h2>⚠️ Critical Health Implications</h2>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem;">
            <div>
                <h4>Vision Threat</h4>
                <p style='font-size: 1.1rem;'>
                - 79% risk of vision loss within 5 years without treatment<br>
                - $10B annual global healthcare cost (Vision Atlas 2023)
                </p>
            </div>
            <div>
                <h4>Detection Challenges</h4>
                <p style='font-size: 1.1rem;'>
                - 45% of diabetics never undergo eye screening<br>
                - Average diagnosis delay: 3.2 years (NEI Study 2024)
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Annual Cases and Awareness
with st.container():
    st.markdown("""
    <div class="info-card">
        <h2>📈 Epidemiologic Data</h2>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem;">
            <div>
                <h4>New Cases/Year</h4>
                <p style='font-size: 1.2rem;'>
                4.1 Million (WHO Diabetes Report 2024)
                </p>
            </div>
            <div>
                <h4>Awareness Gap</h4>
                <p style='font-size: 1.2rem;'>
                35% of diabetics unaware of DR risks<br>
                (Global Diabetes Survey 2023)
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Example severity scale
with st.container():
    st.markdown("""
    <div class="info-card">
        <h2>🩺 Our Clinical Solution</h2>
                <p style='font-size: 1.1rem;'>ClearSight.AI delivers <strong>98.39% accurate</strong> DR classification using deep learning, detecting 5 severity stages through retinal scan analysis:</p>            
            <div class="severity-scale">
                <div style="background: #e8f5e9; color: #1b5e20;" class="stage-card">
                    <h4>Stage 0</h4>No DR
                </div>
                <div style="background: #fff3e0; color: #ef6c00;" class="stage-card">
                    <h4>Stage 1</h4>Mild
                </div>
                <div style="background: #ffe0b2; color: #f57c00;" class="stage-card">
                    <h4>Stage 2</h4>Moderate
                </div>
                <div style="background: #ffcdd2; color: #c62828;" class="stage-card">
                    <h4>Stage 3</h4>Severe
                </div>
                <div style="background: #ff8a80; color: #b71c1c;" class="stage-card">
                    <h4>Stage 4</h4>Proliferative
                </div>
            </div>
    </div>
    """, unsafe_allow_html=True)

# Research Papers
with st.container():
    st.markdown("""
    <div class="info-card">
        <h2>📚 Published Research</h2>
        <div class="research-paper">
            <h4>A. <a href="https://doi.org/10.1109/ICOECA62351.2024.00151" target="_blank">Light Weight CNN based on Knowledge Distillation for Diabetic Retinopathy Detection</a></h4>
                <p> Baranidharan B, Janenie J, Chhipa H. (FEB 2024)<br><em>2024 International Conference on Expert Clouds and Applications</em><br>DOI: 10.1109/ICOECA62351.2024.00151</p>
            <h4>B. <a href="https://drive.google.com/file/d/1weYyhMIrvPj_rFKFdEI9p3swEUFFCSCg/view?usp=sharing" target="_blank"> Refining Diagnostic Accuracy in Diabetic Retinopathy Detection via Mixup Augmentation Techniques</a></h4>
                <p> Baranidharan B, Janenie J, Chhipa H. (NOV 2024)<br><em>2024 International Conference on Data, Computation and Communication</em><br>DOI: 10.1109/ICDCC62351.2024.00151</p>
                </div>
    </div>
    """, unsafe_allow_html=True)


# CTA Section
st.markdown("""
<div style="text-align: center; margin: 4rem 0;">
    <a href="/Take_Test" target="_self">
        <button style="
            padding: 1.2rem 4rem;
            background: var(--accent-color);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 1.1rem;
            font-weight: 600;
            transition: transform 0.3s;
        ">
            Start Free Retinal Analysis →
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; color: var(--text-color); margin: 2rem 0; font-size: 0.9rem;'>
    © 2024 ClearSight.AI | 
    <a href="/Privacy_Policy" style="color: var(--text-color);">Privacy Policy</a> | 
    <a href="/Terms_of_Service" style="color: var(--text-color);">Terms of Service</a>
</div>
""", unsafe_allow_html=True)