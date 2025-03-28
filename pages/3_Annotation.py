import streamlit as st
import cv2
import numpy as np
import tempfile
import os

def create_annotation_masks(image_path):
    # Load the fundus image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found at path: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)

    # Initialize empty masks for each lesion type
    microaneurysms_mask = np.zeros_like(img[:, :, 0])  #1
    hemorrhages_mask = np.zeros_like(img[:, :, 0])     #2
    exudates_mask = np.zeros_like(img[:, :, 0])        #3
    cotton_wool_mask = np.zeros_like(img[:, :, 0])     #4
    neovascularization_mask = np.zeros_like(img[:, :, 0])  #5

    # --- Microaneurysms (Red Dots) ---
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.bitwise_or(
        cv2.inRange(hsv, lower_red1, upper_red1),
        cv2.inRange(hsv, lower_red2, upper_red2)
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    microaneurysms_mask = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)

    # --- Hemorrhages (Larger Red Patches) ---with st.expander
    
    _, hemorrhages_mask = cv2.threshold(mask_red, 127, 255, cv2.THRESH_BINARY)
    hemorrhages_mask = cv2.morphologyEx(hemorrhages_mask, cv2.MORPH_CLOSE, kernel)

    # --- Hard/Soft Exudates (Yellow-White) ---
    L, A, B = cv2.split(lab)
    _, exudates_mask = cv2.threshold(B, 145, 255, cv2.THRESH_BINARY)

    # --- Cotton Wool Spots (Fluffy White) ---
    green_channel = img[:, :, 1]
    _, cotton_wool_mask = cv2.threshold(green_channel, 180, 255, cv2.THRESH_BINARY)
    cotton_wool_mask = cv2.morphologyEx(cotton_wool_mask, cv2.MORPH_OPEN, kernel)

    # --- Neovascularization (Abnormal Vessels) ---
    kernel_vessel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    neovascularization_mask = cv2.morphologyEx(mask_red, cv2.MORPH_GRADIENT, kernel_vessel)
    neovascularization_mask = cv2.threshold(neovascularization_mask, 40, 255, cv2.THRESH_BINARY)[1]

    return {
        "neovascularization": neovascularization_mask,
        "microaneurysms": microaneurysms_mask,
        "hemorrhages": hemorrhages_mask,
        "exudates": exudates_mask,
        "cotton_wool": cotton_wool_mask
    }

def main():
    # Custom CSS for gradients and styling
    st.set_page_config(page_title="DR Annotation", layout="wide", page_icon="👁️")
    
    gradient_text = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
    
    .gradient-text {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-family: 'Poppins', sans-serif;
        font-size: 2.5em !important;
        text-align: center;
        margin-bottom: 20px !important;
    }
    
    .header-box {
        background: linear-gradient(45deg, #2c3e50, #3498db);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 25px;
        background: #000000;
        border-radius: 8px 8px 0 0;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e2e6ee;
        color: #2c3e50 !important;  /* Changed from white to dark */
        font-weight: 700 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #4ECDC4, #45B7AF) !important;
        color: white !important;
    }
    
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .image-container:hover {
        transform: translateY(-5px);
    }
    
    .upload-section {
        border: 2px dashed #4ECDC4;
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        text-align: center;
    }
    .about-section {
        background: rgba(236, 240, 241, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border-left: 4px solid #4ECDC4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .about-section h3 {
        color: #2c3e50 !important;
        margin-bottom: 15px !important;
    }
    </style>
    """
    st.markdown(gradient_text, unsafe_allow_html=True)

    # Main content
    st.markdown('<h1 class="gradient-text">RetinaVision Analyzer</h1>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ About this Project", expanded=False):
        st.markdown("""
        <div class="about-section">
            <p><strong>Diabetic Retinopathy Detection System</strong></p>
            <p>Upload a fundus image to analyze and visualize various pathological features:</p>
            <ul>
                <li>Microaneurysms</li>
                <li>Hemorrhages</li>
                <li>Exudates</li>
                <li>Cotton Wool Spots</li>
                <li>Neovascularization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="header-box">', unsafe_allow_html=True)
    st.header("📤 Image Upload & Analysis")
    uploaded_file = st.file_uploader(
        "Drag and drop or browse fundus images", 
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG",
        key="file_uploader"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            with st.spinner('🔍 Analyzing retinal features...'):
                masks = create_annotation_masks(tmp_path)
                original_img = cv2.cvtColor(cv2.imread(tmp_path), cv2.COLOR_BGR2RGB)
                
                # Layout with enhanced styling
                col1, col2 = st.columns([1, 2], gap="large")
                
                with col1:
                    st.markdown("### Original Image 📷")
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.image(original_img, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown("### Pathology Visualization 🔬")
                    tabs = st.tabs([
                        "🧬 Microaneurysms", 
                        "🕸️ Neovascularization",
                        "🩸 Hemorrhages", 
                        "💡 Exudates", 
                        "☁️ Cotton Wool" 

                    ])
                    
                    tab_content = [
                        masks["microaneurysms"],
                        masks["neovascularization"],
                        masks["hemorrhages"],
                        masks["exudates"],
                        masks["cotton_wool"]
                    ]
                    
                    for tab, content, color in zip(tabs, tab_content, ["#FF6B6B", "#FF6B6B", "#F9C74F", "#90BE6D", "#577590"]):
                        with tab:
                            st.markdown(f'<div class="image-container" style="border: 2px solid {color}">', unsafe_allow_html=True)
                            st.image(content, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
            
            st.success("✅ Analysis complete! Switch between tabs to explore different pathologies.")
            
        except Exception as e:
            st.error(f"⚠️ Error processing image: {str(e)}")
            st.warning("Please ensure you've uploaded a valid fundus image in proper lighting conditions.")
        finally:
            try:
                os.unlink(tmp_path)
            except Exception as cleanup_error:
                st.warning(f"Warning: Temporary file cleanup failed - {str(cleanup_error)}")

if __name__ == "__main__":
    main()