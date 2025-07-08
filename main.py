from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional
import json

def load_data():
    with open('patients.json', 'r') as f:
        data= json.load(f)

        return data

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Enter ID")]
    name: Annotated[str, Field(..., description="Enter name")]
    city: Annotated[str, Field(..., description='City name?')]
    age: Annotated[int, Field(..., description='Enter age')]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description='Gender?')]
    height: Annotated[float, Field(..., description='Enter height in meters')]
    weight: Annotated[float, Field(..., description='Enter weight in kg')]

    @property
    def BMI(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @property
    def verdict(self) -> str:
        bmi = self.BMI
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        


class PatientUpdate(BaseModel):
    name: Optional[str]
    city: Optional[str]
    age: Optional[int]
    gender: Optional[Literal['Male', 'Female', 'Others']]
    height: Optional[float]
    weight: Optional[float]

def load_data():
    try:
        with open('patients.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)   





@app.get("/")
def hello():
    return {"message": "patients management system API"}

@app.get('/about')
def about():
    return{'message': "patient's info"}

@app.get('/view')
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in db', example='P001')):
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')

def sort_patient(sort_by: str= Query(..., description='sort by height,weight and bmi'), order: str= Query('asc', description='asc or dsc order')):

    valid_fields=['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='Invalid')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='select asc or desc only')
    
    data= load_data()

    sort_order= True if order=='desc' else False

    sorted_data= sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_info = data[patient_id]
    updates = patient_update.model_dump(exclude_unset=True)
    existing_info.update(updates)

    # Re-validate using Patient model
    updated_patient = Patient(id=patient_id, **existing_info)
    data[patient_id] = updated_patient.model_dump(exclude=['id'])

    save_data(data)
    return JSONResponse(status_code=200, content={
        'message': 'Patient updated',
        'BMI': updated_patient.BMI,
        'verdict': updated_patient.verdict
    })


@app.delete('/delete/{patient_id}')

def delete_patient(patient_id: str):

    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Deleted'})
