from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = FastAPI(title='Diabetes prediction')

    
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pipe = joblib.load(os.path.join(BASE_DIR, 'model' , 'pipe.pkl'))

class InputData(BaseModel):
    gender: str
    age: int
    hypertension: int
    heart_disease: int
    smoking_history: str
    bmi: float
    HbA1c_level: float
    blood_glucose_level: int
    
    
@app.post('/predict') 
def predict(data: InputData):
 try:
    input_dict = data.model_dump()
    df = pd.DataFrame([input_dict])
    df = df[pipe.feature_names_in_]
    
    
    prediction = pipe.predict(df)[0]
    probability = pipe.predict_proba(df)[0][1]
    
    return {
        "prediction": int(prediction),
        "risk_percentage": float(round(probability*100,2)),
        "result": "Diabetic" if prediction ==1 else "Non-Diabetic"
    }
 except Exception as e:
     import traceback
     traceback.print_exc()
     return{"error": str(e)}
    
    
@app.get('/')
def home():
    return{"message": "API is runnin. Use /docs to test"}    
            
    
    
    
    
