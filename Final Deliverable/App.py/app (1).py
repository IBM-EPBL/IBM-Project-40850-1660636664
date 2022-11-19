from flask import Flask, render_template, request, flash, redirect
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "JJoSicw67yzKlSR_agOi5liOkDvcZwsd3m4bV0ck9Sjx"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()['access_token']
print('mltoken',mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')
@app.route("/kidney", methods=['GET', 'POST'])
def kidneyPage():
    return render_template('kidney.html')

@app.route("/predictPage", methods = ['POST', 'GET'])
def predictPage():
    age=request.form['age']
    bp=request.form['bp']
    al=request.form['al']
    su=request.form['su']
    rbc=request.form['rbc']
    pc=request.form['pc']
    pcc=request.form['pcc']
    ba=request.form['ba']
    bgr=request.form['bgr']
    bu=request.form['bu']
    sc=request.form['sc']
    pot=request.form['pot']
    wc=request.form['wc']
    htn=request.form['htn']
    dm=request.form['dm']
    cad=request.form['cad']
    pe=request.form['pe']
    ane=request.form['ane']

    t=[[int(float(age)),int(float(bp)),int(float(al)),int(float(su)),int(float(rbc)),int(float(pc)),int(float(pcc)),int(float(ba)),int(float(bgr)),int(float(bu)),int(float(sc)),int(float(pot)),int(float(wc)),int(float(htn)),int(float(dm)),int(float(cad)),int(float(pe)),int(float(ane))]]
    print(t)
    payload_scoring = {"input_data": [{"field": [["age","bp","al","su","rbc","pc","pcc","ba","bgr","bu","sc","pot","wc","htn","dm","cad","pe","ane"]], "values": t}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6b7627de-946c-42c9-a3d2-563154efd72b/predictions?version=2022-11-17', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions=response_scoring.json()
    print(predictions)
    pred=predictions['predictions'][0]['values'][0][0]
    if (pred==0):
        output="Great! You are Healthy"
        print("Great! You are Healthy")
    else:
        output="Chronic Kidney Disease-Detected!!"
        print("Chronic Kidney Disease-Detected!!")
    return render_template('predict.html', pred = output)

if __name__=='__main__':
    app.run(debug=True)

