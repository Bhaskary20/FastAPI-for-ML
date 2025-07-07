from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal



app=FastAPI()


class Patient(BaseModel):

    id: Annotated[str, Field(..., description="Enter ID")]
    name: Annotated[str, Field(..., description="Enter name")]
    city: Annotated[str, Field(..., description='City name?')]
    age: Annotated[int, Field(..., description='Enter age')]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description='Gender?')]
    height: Annotated[float, Field(..., description='Enter height')]
    weight: Annotated[float, Field(..., description='Enter weight')]


    @computed_field
    @property

    def BMI(self) -> float:
        
        BMI=round(self.weight/(self.height**2), 2)
        return BMI
    


    @computed_field
    @property

    def verdict(self) -> str:

        if self.BMI<18.5:
            return 'Underweight'
        
        elif self.BMI<30:
            return 'Normal'
        
        else: 
            return 'Obese'



    
def load_data():
    with open ('patients.json', 'r') as f:
        data=json.load(f)

    return data


def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data,f)



@app.post('/create')

def create_patient(patient: Patient):

    data=load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Alr exists')
    
    data['patient.id']=patient.model_dump(exclude=['id'])


    save_data(data)

    return JSONResponse(status_code=201, content={'message' : 'patient created successfully'})