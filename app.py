import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = []

    int_features.append(float(request.form.get("Satisfaction")))
    int_features.append(float(request.form.get("timespent")))
    int_features.append(float(request.form.get("Work_Accident")))

    if request.form.get("Promotion") == "YES":
        int_features.append(1)
    else:
        int_features.append(0)

    if request.form.get("Department") == "RandD":
        int_features.append(1)
        int_features.append(0)
        int_features.append(0)
    elif request.form.get("Department") == "HR":
        int_features.append(0)
        int_features.append(1)
        int_features.append(0)
    elif request.form.get("Department") == "Management":
        int_features.append(0)
        int_features.append(0)
        int_features.append(1)
    else:
        int_features.append(0)
        int_features.append(0)
        int_features.append(0)
        
    if request.form.get("Salary") == "low":
        int_features.append(0)
        int_features.append(1)
        int_features.append(0)
    elif request.form.get("Salary") == "medium":
        int_features.append(0)
        int_features.append(0)
        int_features.append(1)
    elif request.form.get("Salary") == "high":
        int_features.append(1)
        int_features.append(0)
        int_features.append(0)
    
    for x in int_features:
        print(x)
    # int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = prediction[0]
    if output == 0:
        return render_template('index.html', prediction_text='Employee will not leave the company probably.')    
    return render_template('index.html', prediction_text='Employee will leave the company probably.')

    


if __name__ == "__main__":
    app.run(debug=True)