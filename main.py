from fastapi import FastAPI, Path, HTTPException, Query
import json

def load_data():
    with open('patients.json', 'r') as f:
        data= json.load(f)

        return data

app = FastAPI()

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
