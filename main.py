import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import warnings
from warnings import filterwarnings
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.experimental import enable_iterative_imputer
from fancyimpute import IterativeImputer
from sklearn.preprocessing import RobustScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import numpy as np
import uvicorn


app = FastAPI()

#--------------------------------------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with the frontend’s actual IP and port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )
#-------------------------------------------------------------------------------------------------------


from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import pandas as pd
import joblib
import uvicorn

app = FastAPI()

@app.get("/ping")
async def ping():
    return "hello I am alive"

@app.post("/CKD_predict")
async def CKD_predict(file: UploadFile = File(...)):
    try:
        # Load the model
        model = joblib.load(r"C:\Users\gayan\Desktop\Research\dev\files\random_forest_model.pkl")
        # Load the saved RobustScaler
        scaler = joblib.load(r"C:\Users\gayan\Desktop\Research\dev\files\robust_scaler.pkl")

        # Read the uploaded file
        file_content = await file.read()
        new_data = pd.read_csv(BytesIO(file_content))

        # Process the first row of data
        new_data_one_raw = new_data.iloc[0].values.reshape(1, -1)

        # Scale the data
        scaled_data = scaler.transform(new_data_one_raw)

        # Make a prediction
        prediction = model.predict(scaled_data)
        str=''
        # Return the result
        str = ''
        if int(prediction[0]) == 1:
            str = 'You have CKD'
        elif int(prediction[0]) == 0:
            str = 'You have Not CKD'
        print(new_data)
        print(str)
        return {"prediction": str}  # Assuming the model predicts a numeric label

    except Exception as e:
        # Handle errors and return a meaningful message
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
