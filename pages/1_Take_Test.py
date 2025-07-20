import streamlit as st
import numpy as np
import io
import tensorflow as tf
import torch
import base64
import gdown
import os
from torchvision import models, transforms
from PIL import Image, ImageOps, ImageColor
from streamlit.components.v1 import html

# Google Drive File IDs (Replace with your actual file IDs)
BINARY_MODEL_FILE_ID = "1Gy38wjFVdhKSpPUxZtCjs4OQeLV8Njja"
DR_MODEL_FILE_ID = "1EI7L47cNs5lqX2l4dDBDDU5ID5SQ6Gpe"

BINARY_MODEL_PATH = "saved_models/densenet121_retina_finetuned.pth"
DR_MODEL_PATH = "saved_models/ClearSight.h5"

# Add this right after imports but before st.set_page_config
def nav_page(page_name, timeout_secs=3):
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

st.set_page_config(page_title="Take Test - ClearSight.AI", 
                   page_icon="👁️", 
                   layout="wide",
                   initial_sidebar_state="collapsed")




take_test_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js Animation</title>
  <style>
  body {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
  #particles-js {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    z-index: -1;
  }
  .content {
    position: relative;
    z-index: 1;
    text-align: center;
    padding-top: 5vh;
    color: white;
    font-family: Arial, sans-serif;
  }

  .test-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 45%;
    max-width: 50rv;
    margin: 0 auto;
    background: rgba(15, 17, 23, 0.15);
    padding: 1rem;
    border-radius: 20px;
    backdrop-filter: blur(5px);
    font-family: Arial, sans-serif;
    text-align: center;
    box-sizing: border-box;
  }
  .gradient-text {
    font-size: clamp(2.5rem, 8vw, 4.5rem);
    font-weight: 700;
    background: linear-gradient(45deg, #eff6ee, #9197ae, #273043);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 4px 10px rgba(0,0,0,0.2);
    line-height: 1;
    margin: 0;
    padding: 0.5rem 0;
  }
  @media (max-width: 768px) {
    .test-container {
      width: 85%;
      padding: 0.8rem;
    }
    .gradient-text {
      font-size: clamp(2rem, 10vw, 3rem);
    }
  }
  @media (max-width: 480px) {
    .test-container {
      width: 95%;
    }
    .gradient-text {
      font-size: clamp(1.8rem, 12vw, 2.5rem);
    }
  }
  </style>
</head>
<body>
  <div id="particles-js"></div>
    <div class="test-container"> <h2 class="gradient-text">ClearSight.AI</h2>
    <!-- Streamlit content will be injected here -->
    </div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 400,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "star",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          },
          "image": {
            "src": "img/github.svg",
            "width": 100,
            "height": 100
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": true,
            "speed": 1,
            "opacity_min": 0.5,
            "sync": false
          }
        },
        "size": {
          "value": 2,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#ffffff",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 0.65,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "bounce",
          "bounce": true,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 10,
            "duration": 2,
            "opacity": 0.5,
            "speed": 1
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 2
          },
          "remove": {
            "particles_nb": 3
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""

# Custom CSS for Streamlit components
st.markdown("""
<style>
.stApp {
    background: transparent !important;
}

.st-emotion-cache-1y4p8pa {
    padding: 0 !important;
}

.stMarkdown, .stFileUploader, .stImage {
    position: relative;
    z-index: 2 !important;
}

h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

.st-bb {
    border-color: white !important;
}

.st-cb {
    color: white !important;
}

.severity-box {
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
    background: rgba(255,255,255,0.1);
}

.progress-container {
    margin: 20px 0;
    padding: 10px;
    border-radius: 8px;
    background: rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

#session state initializations
if 'show_retry' not in st.session_state:
    st.session_state.show_retry = False
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False
if 'diagnosis_data' not in st.session_state:
    st.session_state.diagnosis_data = None


st.components.v1.html(take_test_html, height=400)

@st.cache_resource

# Function to download a model from Google Drive
def download_model(file_id, output_path):
    if not os.path.exists(output_path):  # Avoid redundant downloads
        url = f"https://drive.google.com/uc?id={file_id}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        gdown.download(url, output_path, quiet=False)
        print(f"Downloaded: {output_path}")
    else:
        print(f"Model already exists: {output_path}")

def load_models():
    # Download models if they are not present
    download_model(BINARY_MODEL_FILE_ID, BINARY_MODEL_PATH)
    download_model(DR_MODEL_FILE_ID, DR_MODEL_PATH)

    # Load binary classification model (PyTorch)
    binary_model = models.densenet121(weights=None)  # No pretrained weights
    num_ftrs = binary_model.classifier.in_features
    binary_model.classifier = torch.nn.Linear(num_ftrs, 2)
    binary_model.load_state_dict(torch.load(BINARY_MODEL_PATH, map_location=torch.device('cpu')))
    binary_model.eval()

    # Load DR stage model (TensorFlow)
    dr_model = tf.keras.models.load_model(DR_MODEL_PATH, compile=False)
    dr_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
    
    return binary_model, dr_model

# Initialize models
binary_model, dr_model = load_models()

def preprocess_binary(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def preprocess_dr(image):
    size = (512, 512)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    img_array = np.array(image) / 255.0
    return np.expand_dims(img_array, axis=0)

with st.container():
    st.title("Test Your Diabetic Retinopathy Status")
    st.markdown("---")

    st.markdown("#### Or select a sample retinal image for testing:")
    sample_choice = st.selectbox("Choose a DR stage (0 = No DR, 1 = Mild DR, 2 = Moderate DR, 3 = Severe, 4 = Proliferative)", 
                                 options=["None", "0", "1", "2", "3", "4"], 
                                 index=0)

    image = None
    uploaded_file = None

    if sample_choice != "None":
        sample_path = f"sample_images/{sample_choice}.png"
        try:
            image = Image.open(sample_path).convert('RGB')
            st.success(f"Loaded sample image for stage {sample_choice}")
        except Exception as e:
            st.error(f"Failed to load sample image: {e}")
            st.stop()
    else:
        uploaded_file = st.file_uploader(
            "Upload a retinal scan image", 
            type=["jpg", "jpeg", "png"], 
            accept_multiple_files=False, 
            key="test_uploader"
        )
        if uploaded_file:
            image = Image.open(uploaded_file).convert('RGB')

    if image is not None:
        try:
            col1, col2, col3 = st.columns([5, 5, 6.5])
            with col2:
                st.markdown("""
                <style>
                    .centered-image {
                        display: flex;
                        justify-content: center;
                        margin: 0 auto;
                        padding: 20px 0;
                    }
                </style>
                """, unsafe_allow_html=True)             

                st.markdown('<div class="centered-image">', unsafe_allow_html=True)
                st.image(image, caption="Selected Retinal Scan", width=600)
                st.markdown('</div>', unsafe_allow_html=True)

            # Step 1: Retina Validation
            with st.spinner('Verifying retinal scan...'):
                image_tensor = preprocess_binary(image)
                with torch.no_grad():
                    output = binary_model(image_tensor)
                    probabilities = torch.nn.functional.softmax(output, dim=1)
                    retina_prob = probabilities[0][1].item()

            if retina_prob < 0.5:
                st.session_state.show_retry = True
                st.error("❌ Non-retinal Image Detected. Please upload a valid retinal scan.")
                
                if st.button("🔄 Try Again", key="retry_button"):
                    st.session_state.pop("show_retry", None)
                    st.session_state.pop("test_uploader", None)
                    st.rerun()
            else:
                st.session_state.show_retry = False
                st.success(f"✅ Valid Retinal Scan Detected (Confidence: {retina_prob*100:.1f}%)")

                # Step 2: DR Detection
                with st.spinner('Analyzing diabetic retinopathy stage...'):
                    dr_input = preprocess_dr(image)
                    dr_pred = dr_model.predict(dr_input)
                    dr_class = np.argmax(dr_pred)
                    confidence = np.max(dr_pred)

                # Save to session
                st.session_state.diagnosis_data = {
                    'stage': dr_class,
                    'confidence': confidence,
                    'retina_prob': retina_prob,
                    'image': image
                }

                # Display Results
                dr_stages = {
                    0: ["No Diabetic Retinopathy (Stage 0)", "#4CAF50", "✅"],
                    1: ["Mild Diabetic Retinopathy (Stage 1)", "#FFC107", "⚠️"],
                    2: ["Moderate Diabetic Retinopathy (Stage 2)", "#FF9800", "⚠️⚠️"],
                    3: ["Severe Diabetic Retinopathy (Stage 3)", "#F44336", "❌"],
                    4: ["Proliferative Diabetic Retinopathy (Stage 4)", "#D32F2F", "🆘"]
                }

                stage, color, emoji = dr_stages[dr_class]

                st.markdown(f"""
                <div class="severity-box" style="border-left: 5px solid {color}; padding-left: 15px; margin-top: 20px;">
                    <h3>{emoji} Diagnosis: {stage}</h3>
                    <p><strong>Confidence:</strong> {confidence*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)

                # Button Style
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

                st.markdown("---")

                if st.button("Results Analysis"):
                    nav_page("results_analysis") 

                st.markdown("---")

        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
