import aiofiles
from fastapi import FastAPI, HTTPException
import json
from typing import List
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BloodPressure(BaseModel):
    systolic: dict
    diastolic: dict

class DiagnosisHistory(BaseModel):
    month: str
    year: int
    blood_pressure: BloodPressure
    heart_rate: dict
    respiratory_rate: dict
    temperature: dict

class Diagnostic(BaseModel):
    name: str
    description: str
    status: str

class PatientData(BaseModel):
    name: str
    gender: str
    age: int
    profile_picture: str
    date_of_birth: str
    phone_number: str
    emergency_contact: str
    insurance_type: str
    diagnosis_history: List[DiagnosisHistory]
    diagnostic_list: List[Diagnostic]
    lab_results: List[str]



async def load_patient_data():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'patients_data.json')
        async with aiofiles.open(file_path, 'r') as file:
            data = await file.read()
            return json.loads(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading patient data: {str(e)}")


@app.get("/patients", response_model=List[PatientData])
async def get_patients():
    return await load_patient_data()


@app.get("/patient/{patient_id}", response_model=PatientData)
async def get_patient(patient_id: int):
    patients = await load_patient_data()

    if patient_id < 1 or patient_id > len(patients):
        raise HTTPException(status_code=404, detail="Patient not found")

    return patients[patient_id - 1]
