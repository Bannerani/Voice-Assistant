import os
import pickle
import numpy as np
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Performance Predictor",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for shadow effects and card styling
st.markdown("""
    <style>
    /* Global styles */
    .main {
        background-color: #f8fafc;
    }
    
    /* Card Container with Shadow */
    .custom-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08), 0 4px 10px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        border: 1px solid #edf2f7;
    }

    /* Header styling */
    .title-text {
        color: #2d3748;
        font-weight: 700;
        text-align: center;
        margin-bottom: 8px;
    }
    
    .subtitle-text {
        color: #718096;
        text-align: center;
        margin-bottom: 24px;
    }

    /* Prediction Result Box */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(118, 75, 162, 0.3);
        margin-top: 20px;
    }

    /* Customizing Streamlit buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(118, 75, 162, 0.25);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        opacity: 0.95;
        box-shadow: 0 6px 16px rgba(118, 75, 162, 0.35);
    }
    </style>
""", unsafe_allow_html=True)

# Load the SVR Model
MODEL_PATH = "svm.pkl"

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return None

model = load_model()

# Categorical options map
CATEGORICAL_OPTIONS = {
    "gender": ["Male", "Female", "Other"],
    "course": ["Computer Science", "Engineering", "Business", "Arts", "Medicine", "Law"],
    "internet_access": ["Yes", "No"],
    "sleep_quality": ["Poor", "Average", "Good", "Excellent"],
    "study_method": ["Self Study", "Group Study", "Online Lectures", "Tutor"],
    "exam_difficulty": ["Easy", "Medium", "Hard"]
}

# Encoding maps for ordinal/categorical fields
ENCODING_MAPS = {
    "gender": {"Male": 0, "Female": 1, "Other": 2},
    "course": {"Computer Science": 0, "Engineering": 1, "Business": 2, "Arts": 3, "Medicine": 4, "Law": 5},
    "internet_access": {"No": 0, "Yes": 1},
    "sleep_quality": {"Poor": 0, "Average": 1, "Good": 2, "Excellent": 3},
    "study_method": {"Self Study": 0, "Group Study": 1, "Online Lectures": 2, "Tutor": 3},
    "exam_difficulty": {"Easy": 0, "Medium": 1, "Hard": 2}
}

# Header Section
st.markdown("<h1 class='title-text'>Performance Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Enter student details below to generate predictions using the SVR model.</p>", unsafe_allow_html=True)

# Main Form Container
with st.container():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, value=20)
            gender = st.selectbox("Gender", CATEGORICAL_OPTIONS["gender"])
            course = st.selectbox("Course", CATEGORICAL_OPTIONS["course"])
            study_hours = st.number_input("Study Hours (per week)", min_value=0.0, max_value=168.0, value=5.5, step=0.5)
            class_attendance = st.number_input("Class Attendance (%)", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
            internet_access = st.selectbox("Internet Access", CATEGORICAL_OPTIONS["internet_access"])

        with col2:
            sleep_hours = st.number_input("Sleep Hours (per day)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
            sleep_quality = st.selectbox("Sleep Quality", CATEGORICAL_OPTIONS["sleep_quality"])
            study_method = st.selectbox("Study Method", CATEGORICAL_OPTIONS["study_method"])
            facility_rating = st.slider("Facility Rating (1-5)", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
            exam_difficulty = st.selectbox("Exam Difficulty", CATEGORICAL_OPTIONS["exam_difficulty"])

        submit_button = st.form_submit_button("Generate Prediction")
        
    st.markdown("</div>", unsafe_allow_html=True)

# Prediction Logic & Output Display
if submit_button:
    if model is None:
        st.error("Model file (`svm.pkl`) not found. Please verify the file path.")
    else:
        # Construct feature vector matching model inputs
        features = [
            float(age),
            ENCODING_MAPS["gender"][gender],
            ENCODING_MAPS["course"][course],
            float(study_hours),
            float(class_attendance),
            ENCODING_MAPS["internet_access"][internet_access],
            float(sleep_hours),
            ENCODING_MAPS["sleep_quality"][sleep_quality],
            ENCODING_MAPS["study_method"][study_method],
            float(facility_rating),
            ENCODING_MAPS["exam_difficulty"][exam_difficulty]
        ]

        prediction = model.predict(np.array([features]))[0]
        formatted_prediction = round(float(prediction), 2)

        # Display Result with CSS Shadow Effects
        st.markdown(f"""
            <div class='result-card'>
                <h3 style='margin:0; font-size: 1.2rem; opacity: 0.9;'>Predicted Score / Value</h3>
                <h1 style='margin:10px 0 0 0; font-size: 2.8rem;'>{formatted_prediction}</h1>
            </div>
        """, unsafe_allow_html=True)
