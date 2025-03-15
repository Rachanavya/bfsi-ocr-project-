import streamlit as st
import re
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
import pytesseract
from PIL import Image
import os
import base64

def set_background():
    if st.session_state.page in ["welcome", "login", "signup", "options"]:
        image_path = r"C:\\Users\\navya\\OneDrive\\Desktop\\infosys\\blue.png"
    else:
        image_path = r"C:\\Users\\navya\\OneDrive\\Desktop\\infosys\\after.png"
    
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Configure Tesseract OCR
tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

st.set_page_config(page_title="Welcome | Your Trusted Financial Advisor", layout="centered")

# Initialize MongoDB client
db_client = MongoClient("mongodb://localhost:27017/")
db_supervised = db_client["supervised_db"]

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "users" not in st.session_state:
    st.session_state.users = {"admin": "Admin@123"}  # Sample user

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def process_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        extracted_text = extract_text_from_image(image)
        data = {'Extracted Text': extracted_text.split('\n')}
        df = pd.DataFrame(data)
        return df
    return None

set_background()

# Welcome Page
if st.session_state.page == "welcome":
    st.title("Welcome to Your Financial Future")
    st.markdown("""
    <p style='font-family: Arial, sans-serif; font-size: 40px; text-align: center; font-weight: bold;'>"Ally"</p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style='font-size: 18px; text-align: center;'>At ALLY, we help you plan, grow, and secure your financial future with expert advice tailored to your needs.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Get Started Today", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# Login Page
elif st.session_state.page == "login":
    st.title("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.page = "options"
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    if st.button("Sign Up"):
        st.session_state.page = "signup"
        st.rerun()

# Signup Page
elif st.session_state.page == "signup":
    st.title("Create an Account")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    otp = st.text_input("Enter OTP")
    new_password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Re-enter Password", type="password")
    
    def validate_password(password):
        return bool(re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$', password))
    
    if st.button("Sign Up"):
        if new_password != confirm_password:
            st.error("Passwords do not match!")
        elif not validate_password(new_password):
            st.error("Password must have at least 8 characters, one number, one capital letter, and one special character.")
        else:
            st.session_state.users[email] = new_password
            st.success("Account created successfully! Please login.")
            st.session_state.page = "login"
            st.rerun()

# Options Page
elif st.session_state.page == "options":
    st.title("Choose Your Service")
    st.write("Select one of the options below:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Document Analysis", use_container_width=True):
            st.session_state.page = "document_analysis"
            st.rerun()
    with col2:
        if st.button("🏦 Loan Eligibility Checker", use_container_width=True):
            st.session_state.page = "loan_eligibility"
            st.rerun()

# Document Analysis Page
elif st.session_state.page == "document_analysis":
    
    # Sidebar for Document Analysis
    st.sidebar.title("Upload Files")
    st.sidebar.subheader("Select Data Type:")
    
    data_type = st.sidebar.radio("Select Data Type:", ["Supervised", "Unsupervised", "Semi-Supervised","Compare Two Stocks"])
    
    if data_type == "Supervised":
        doc_type = st.sidebar.radio("Select Document Type:", ["Invoice", "Payslip", "Bank Statement", "Bank Transactions"])
    elif data_type == "Semi-Supervised":
        doc_type = st.sidebar.radio("Select Option:", ["Stock Market"])
    elif data_type == "Unsupervised":
        doc_type = st.sidebar.radio("Select Option:", ["Cluster Data"])
    
    
    
    st.sidebar.subheader("Upload Files")
    uploaded_files = st.sidebar.file_uploader("Drag and drop files here", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
    st.sidebar.subheader("Process Files")
    if st.sidebar.button("Process Files"):
       with st.spinner("Processing... Please wait."):
            time.sleep(3)  # Simulating backend processing
        
    
    st.title("📊 DOCUMENT ANALYSIS")
    
# Loan Eligibility Checker Page
elif st.session_state.page == "loan_eligibility":
    st.title("🏦 Student Loan Eligibility Checker")

    # Student details
    tenth_result = st.number_input("10th Grade Percentage", min_value=0.0, max_value=100.0, step=0.1)
    inter_marks = st.number_input("Intermediate Percentage", min_value=0.0, max_value=100.0, step=0.1)
    standardized_exam = st.number_input("Standardized Exam Score (e.g., JEE, NEET)", min_value=0, max_value=360, step=1)
    parents_income = st.number_input("Parents' Annual Income (INR)", min_value=0, step=10000)
    preferred_course = st.selectbox("Select Preferred Course", ["Engineering", "Medical", "Management", "Law", "Other"])

    # Check eligibility
    if st.button("Check Eligibility"):
        if tenth_result >= 60 and inter_marks >= 60 and standardized_exam >= 50 and parents_income <= 1000000:
            st.success("✅ You are eligible for a student loan!")
            
            # Suggested banks & loan details
            st.subheader("🏦 Recommended Banks & Loan Details")
            loan_options = {
                "SBI Education Loan": {"Max Loan": "₹20 Lakhs", "Interest Rate": "8.5%"},
                "HDFC Credila": {"Max Loan": "₹25 Lakhs", "Interest Rate": "9.2%"},
                "ICICI Education Loan": {"Max Loan": "₹30 Lakhs", "Interest Rate": "10.5%"},
                "Axis Bank": {"Max Loan": "₹15 Lakhs", "Interest Rate": "9.0%"}
            }
            
            df = pd.DataFrame(loan_options).T
            st.table(df)
        else:
            st.error("❌ Sorry, you do not meet the eligibility criteria for a student loan.")
