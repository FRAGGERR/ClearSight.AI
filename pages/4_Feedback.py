import streamlit as st
from streamlit_lottie import st_lottie
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase only once
if not firebase_admin._apps:
    # Load credentials directly from Streamlit secrets
    firebase_config = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
    
db = firestore.client()

def save_feedback(data):
    """Save feedback to Firestore"""
    try:
        doc_ref = db.collection('feedback').document()
        doc_ref.set({
            'timestamp': datetime.datetime.now().isoformat(),
            'name': data['name'],
            'email': data['email'],
            'role': data['role'],
            'rating': data['rating'],
            'comments': data['comments'],
            'app_version': '1.0.0'
        })
        return True
    except Exception as e:
        st.error(f"Error saving feedback: {str(e)}")
        return False

def feedback_form():
    with st.form("feedback_form"):
        # Custom CSS for the feedback form
        st.markdown("""
        <style>
            .feedback-header {
                background: linear-gradient(45deg, #2c3e50, #3498db);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                font-family: 'Poppins', sans-serif;
                font-size: 2em !important;
                text-align: center;
                margin-bottom: 30px !important;
            }
            
            .stTextInput>div>div>input, .stTextArea>div>div>textarea {
                border: 1px solid #4ECDC4 !important;
                border-radius: 8px !important;
                padding: 10px !important;
            }
            
            .stSelectSlider>div>div>div>div {
                background: #f0f2f6 !important;
                border-radius: 20px !important;
                padding: 10px !important;
            }
            
            .stButton>button {
                background: linear-gradient(45deg, #4ECDC4, #45B7AF) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px 24px !important;
                font-size: 1.1em !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4) !important;
            }
            
            .feedback-container {
                border: 2px solid #4ECDC4;
                border-radius: 15px;
                padding: 30px;
                margin: 20px 0;
                background: rgba(255, 255, 255, 0.9);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        </style>
        """, unsafe_allow_html=True)

        # Form container
        with st.container():
            st.markdown('<h1 class="feedback-header">Share Your Experience</h1>', unsafe_allow_html=True)
            
            # Form elements
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Your Name (optional)", help="We'd love to know who you are!")
            with cols[1]:
                email = st.text_input("Email (optional)", help="Only if you want us to respond back")
            
            # New demographics field
            role = st.selectbox(
                "Your Role (optional)",
                options=["", "Patient", "Doctor", "Researcher", "Student", "Other"],
                index=0,
                help="Help us understand our user base better"
            )

            rating = st.select_slider(
                "How would you rate your experience?",
                options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
                help="Slide to select your rating"
            )
            
            comments = st.text_area(
                "Your valuable feedback",
                height=150,
                placeholder="What did you like? What can we improve?",
                help="We read every piece of feedback carefully"
            )
            
            # Centered submit button
            _, col, _ = st.columns([1, 2, 1])
            with col:
                submitted = st.form_submit_button(
                    "🚀 Submit Feedback",
                    use_container_width=True,
                    help="Click to share your thoughts with us"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Submission handling (existing logic remains same)
        if submitted:
            if not comments.strip():
                st.warning("Please provide feedback text")
                return

            feedback_data = {
                "name": name.strip(),
                "email": email.strip(),
                "role": role.strip() if role else "Not specified",
                "rating": rating,
                "comments": comments.strip()
            }

            if save_feedback(feedback_data):
                st.success("Thank you for your feedback! 💌")
                with open("eye_animation.json") as f:
                    lottie_celebration = json.load(f)

                st_lottie(lottie_celebration, height=200)


def main():
    st.set_page_config(page_title="Feedback", page_icon="💬")

    st.markdown("""
    <style>
    .header-container {
        text-align: center;
        margin-bottom: 40px;
    }
    .animated-header {
        font-size: 2.5em !important;
        position: relative;
        display: inline-block;
        color: #2c3e50;
        margin: 20px 0;
    }
    .animated-header::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #4ECDC4, #45B7AF);
        left: 0;
        bottom: -10px;
        animation: underline 2s infinite;
    }
    @keyframes sweep {
        0% { width: 0%; left: 0; }
        100% { width: 97%; left: 0; }
    }
    .animated-header::after {
        animation: sweep 3s ease-in-out infinite;
    }
    </style>

    <div class="header-container">
        <h1 class="animated-header">User Feedback</h1>
    </div>
    """, unsafe_allow_html=True)

    feedback_form()

if __name__ == "__main__":
    main()