import streamlit as st
import base64

# ====== CONFIGURATION ====== #
# Adjust these values to control the layout:
IMAGE_SIZE = 300  # Set image diameter (180-300 recommended)
SECTION_HEIGHT = "55vh"  # Reduce to move content higher ("80vh", "82vh", etc)
NAME_FONT_SIZE = "2rem"  # Base font size for names
GRID_GAP = "5rem"  # Gap between profile cards ("2rem", "3rem", "4rem", etc)
# =========================== #

# Function to encode image as Base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

# Custom CSS with animations
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');

:root {{
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --accent-color: #4f46e5;
    --text-color: #1a1a1a;
    --image-size: {IMAGE_SIZE}px;
    --name-font-size: {NAME_FONT_SIZE};
}}

* {{
    font-family: 'Space Grotesk', sans-serif;
}}

.stApp {{
    background: #0F1117;
    overflow-x: hidden;
}}

.profile-section {{
    position: relative;
    z-index: 2;
    height: {SECTION_HEIGHT};  /* Height controlled by config */
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 2rem 0.1rem;
    margin-top: -20px;  /* Pull content up further */
}}

.profile-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 7rem;
    width: 100%;
    max-width: 1000px;  /* Tighter container */
    margin: 0 auto;
}}

.profile-card {{
    position: relative;
    perspective: 1000px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.1rem;
}}

.profile-image {{
    width: var(--image-size);
    height: var(--image-size);
    margin: 0 auto;
    border-radius: 50%;
    overflow: hidden;
    position: relative;
    transform-style: preserve-3d;
    animation: float 6s ease-in-out infinite;
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-20px); }}
}}

.profile-image img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    filter: grayscale(20%);
    transition: all 0.3s ease;
}}

.profile-card:hover img {{
    filter: grayscale(0%);
    transform: scale(1.05);
}}

.profile-content {{
    text-align: center;
    margin-top: 1.5rem;  /* Reduced margin */
    position: relative;
    width: 100%;
}}

.name-title {{
    font-size: var(--name-font-size);
    font-weight: 700;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin: 0;
    animation: fadeInUp 1s ease;
    line-height: 1.2;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 60px;  /* Fixed height for names */
}}

.name-title .name-line {{
    margin-top: 15px;
}}

.name-line a {{
    text-decoration: none;
    color: white;
    font-size: 28px;
    font-weight: bold;
    transition: color 0.3s;
}}
.name-line a:hover {{
    color: blue;
    cursor: pointer;
}}

@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .profile-grid {{
        gap: 3rem;  /* Direct value instead of broken calc() */
    }}

    .name-title {{
        font-size: 1.8rem;  /* Adjust this manually */
    }}

    .profile-image {{
        width: 240px;
        height: 240px;
    }}
}}

</style>
""", unsafe_allow_html=True)

# Encode uploaded images
image1_base64 = get_base64_image("static/hardik.jpg")
image2_base64 = get_base64_image("static/janenie1.png")

# Page Content
st.markdown(f"""
<div class="profile-section">
    <div class="profile-grid">
        <div class="profile-card">
            <div class="profile-image">
                <img src="data:image/jpeg;base64,{image1_base64}" alt="Hardik Chhipa">
            </div>
            <div class="profile-content">
                <div class="name-title">
                    <span class="name-line">
                        <a href="https://www.linkedin.com/in/hardik-chhipa-303040242/" target="_blank">Hardik Chhipa</a>
                    </span>
                </div>
            </div>
        </div>
        <div class="profile-card">
            <div class="profile-image">
                <img src="data:image/jpeg;base64,{image2_base64}" alt="Janenie Janakiraman">
            </div>
            <div class="profile-content">
                <div class="name-title">
                    <span class="name-line">
                        <a href="https://www.linkedin.com/in/janenie-janakiraman-299b10292/" target="_blank">Janenie Janakiraman</a>
                    </span>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
