import numpy as np
from flask import Flask, render_template, request, jsonify
import joblib
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
le = LabelEncoder()


sc = StandardScaler()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('home.html')

@app.route("/result", methods=["POST","GET"])
def result():
    list_col = ['item_weight', 'item_fat_content', 'item_visibility', 'item_type',
              'item_mrp', 'outlet_establishment_year', 'outlet_size',
              'outlet_location_type', 'outlet_type']

    item_weight = float(request.form['item_weight'])
    item_fat_content = str(request.form['item_fat_content'])
    item_visibility = (request.form['item_visibility'])
    item_type = str(request.form['item_type'])
    item_mrp = float(request.form['item_mrp'])
    outlet_establishment_year = int(request.form['outlet_establishment_year'])
    outlet_size = str(request.form['outlet_size'])
    outlet_location_type = str(request.form['outlet_location_type'])
    outlet_type = str(request.form['outlet_type'])


   # print(item_fat_content)

    # Label Encoding

    le = joblib.load('le.sav')

    item_fat_content = le.fit_transform([item_fat_content])
    item_type = le.fit_transform([item_type])
    outlet_size = le.fit_transform([outlet_size])
    outlet_location_type = le.fit_transform([outlet_location_type])
    outlet_type = le.fit_transform([outlet_type])

    inputs = np.array([item_weight, item_fat_content, item_visibility, item_type, item_mrp, outlet_establishment_year,
                      outlet_size, outlet_location_type, outlet_type]).reshape(1, -1)
    print(inputs)


# Lets put all in the list



    # Lets apply Standard Scaler

    sc = joblib.load('sc.sav')
    inputs_std = sc.transform(inputs)

    # Lets apply prediction

    model=joblib.load(r'C:\Users\SOMAY\OneDrive\Desktop\Sales Prediction\Models\random_forest_grid.sav')

    prediction = model.predict(inputs_std)
    prediction = prediction.tolist()


    return jsonify({'prediction': prediction})



if __name__ == '__main__':
    app.debug = True
    app.run()
