import streamlit as st
import base64

# Function to encode image as Base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

# Custom CSS with animations
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');

:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --accent-color: #4f46e5;
    --text-color: #1a1a1a;
}

* {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background: #f8f9fa;
    overflow-x: hidden;
}

.profile-section {
    position: relative;
    z-index: 2;
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding: 4rem 2rem;
}

.profile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 4rem;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
}

.profile-card {
    position: relative;
    perspective: 1000px;
}

.profile-image {
    width: 280px;
    height: 280px;
    margin: 0 auto;
    border-radius: 50%;
    overflow: hidden;
    position: relative;
    transform-style: preserve-3d;
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
}

.profile-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    filter: grayscale(20%);
    transition: all 0.3s ease;
}

.profile-card:hover img {
    filter: grayscale(0%);
    transform: scale(1.05);
}

.profile-content {
    text-align: center;
    margin-top: 2rem;
    position: relative;
}

.name-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 1rem;
    animation: fadeInUp 1s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
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
                <h2 class="name-title">Hardik Chhipa</h2>
            </div>
        </div>
        <div class="profile-card">
            <div class="profile-image">
                <img src="data:image/jpeg;base64,{image2_base64}" alt="Janenie J.">
            </div>
            <div class="profile-content">
                <h2 class="name-title">Janenie J.</h2>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)



