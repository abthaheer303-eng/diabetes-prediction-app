import streamlit as st
import pandas as pd
import joblib
import requests


API_URL = "http://diabetes-prediction-app-a874.onrender.com/predict"

st.set_page_config(page_title='Diabetes prediction',layout='wide',page_icon="icons8-hospital-50.png", initial_sidebar_state='collapsed')

st.markdown("""
    <style>
     .stApp{
       background: #e6f3ff;
       }
     .main-header {
       background: linear-gradient(90deg, #0d47a1 0% #1976d2 100%);
       padding:20px 30px;
       border-radius: 8px;
       color: black;
       margin-bottom: 30px;
       box-shadow: 0 2px 8px rgba(0,0,0,0,1);
     }
     .card{
       background: white;
       padding: 25px;
       border-radius: 10px
       box-shadow:0 2px 10px rgba(0,0,0,0.05);
       border-left: 4px solid #1976d2;
     }
     .metric-card{
       background: blue;
       padding: 20px;
       text-align: center;
       box-shadow: 0 1px 5px rgba(0,0,0,0.08);
       
     }
     div.stButton > button {
       background-color: #1976d2;
       color: white;
       border:none;
       border-radius: 6px;
       font-weight: 600;
       padding: 12px;
     }
     div.stButton > button:hover{
       background-color: #1565c0;
     }
     </style>
""", unsafe_allow_html=True     )
col_logo, col_title = st.columns([1,6])

with col_logo:
  st.image('hospital.jpg', width=80)
  
  with col_title:
    st.markdown("""
    <div class="main-header">
      <h1 style="margin:0;">City Care Hospital</h1>
      <p style='margin:0; opacity:0.9;'>Diabetes Risk Assessment System  | AI powered Diagnostics</p>  
    </div>
  """, unsafe_allow_html=True)
st.markdown("<div class='card'>", unsafe_allow_html= True)
st.subheader("Patient Information Form")
with st.form('prediction_form'):
  col1, col2, col3 = st.columns(3)
  with col1:
    st.markdown("**Demographics**")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age",1,120,45)
  with col2:
    st.markdown("**Medical History**")
    hypertension = st.selectbox("Hypertension", ["No", "Yes"])
    hypertension= 1 if hypertension == "Yes" else 0
    heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
    heart_disease = 1 if heart_disease == "Yes" else 0
    smoking_history = st.selectbox("Smoking History", ["never", "former", "current", "not current", "ever"])
  with col3:
    st.markdown("**Lab Results**")
    bmi = st.number_input("BMI (kg/m²)", 10.0, 60.0, 25.0, step=0.1)
    HbA1c_level = st.number_input("HbA1c Level (%)", 3.0, 15.0, 5.7, step=0.1)
    blood_glucose_level = st.number_input("Blood Glucose (mg/dL)", 50, 400, 100)
  st.divider()
  submitted = st.form_submit_button("RUN PREDICTION ANALYSIS", use_container_width= True)
st.markdown("</div>", unsafe_allow_html=True) 
 

      
if submitted:
    data = {
        "gender": (gender), "age": int(age), "hypertension": int(hypertension),
        "heart_disease": int(heart_disease), "smoking_history": smoking_history,
        "bmi": float(bmi), "HbA1c_level": float(HbA1c_level), "blood_glucose_level": int(blood_glucose_level)
    }
    with st.spinner('processing ...'):
     try:
            res = requests.post(API_URL,  json=data ,timeout=10)
            result = res.json()
                       
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Assessment Report")
            
            col1, col2, col3 = st.columns(3)
            with col1:
              st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
              st.metric("Risk Percentage", f"{result['risk_percentage']}%")
              st.markdown("</div>", unsafe_allow_html=True)
            with col2:
              st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
              st.metric("Prediction", result['result'])
              st.markdown("</div>", unsafe_allow_html=True)
              
            with col3:
              st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
              status = "High Risk" if result['prediction']== 1 else "LOW RISK"
              st.metric("Risk Category", status)
              st.markdown("</div>", unsafe_allow_html=True)
              
              
              proba =(result['risk_percentage']/100)
              if result['prediction'] == 0:
                    st.markdown(f"""
                  <div style="background-color:#e3f2fd; padding:25px; border-radius:10px;
                   border-left: 6 px solid #1976d2; text-align:center; margin-bottom:15px">
                      <h2 style="color:#0d47a1; margin:0;"> Low Risk</h2>
                      <p style="color:#1565c0; font-size:20px; margin:10px 0;"><b>{result['risk_percentage']}%</b></p>
                      <p style="color:#424242;">keep maintaining healthy lifestyle!</p>
                  </div>
                   """,unsafe_allow_html=True)
                     
                    st.progress(proba)
                    
                    st.info("**Recommendation:** Low risk detected. Advise regular checkup.")
              else:
                    st.markdown(f"""
                    <div style="background-color:#ffebee; padding:25px; border-radius:10px;
                    border-left: 6px solid #d32f2f; text-align:center; margin-bottom:15px">
                        <h2 style="color:#b71c1c; margin:0;"> High Risk</h2>
                        <p style="color:#c62828; font-size:20px; margin:10px 0;"><b>{result['risk_percentage']}%</b></p>
                        <p style='color:#424242;">please consult a doctor immediately.</p>
                    </div>
                    """,unsafe_allow_html=True)
                    st.progress(proba)
                    st.warning("**Recommmendation:** Patient shows high risk factors. Refer to Endocrinology Department.")
     except:
       st.error("Server connection failed. Please ensure the API is running.")
st.markdown("---")
st.caption(" 2026 City Care Hospital | Confidential Patient Data | Version 1.0")            
         
     
                     
                     
                
            
