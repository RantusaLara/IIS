import pickle
import pandas as pd
from flask import Flask
from flask import request
import json
from flask import jsonify
import sys
import os
from flask_cors import CORS, cross_origin


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.get_forecast import get_forecast


app = Flask(__name__)
cors = CORS(app)

def reorder(df):
    new_data = pd.DataFrame()
    new_data['temperature_2m'] = df['temperature_2m']
    new_data['relativehumidity_2m'] = df['relativehumidity_2m']
    new_data['windspeed_10m'] = df['windspeed_10m']
    return new_data


@app.route('/air/predict/', methods=['POST'])
@cross_origin()
def predict():
    object_json = request.json

    object_json = get_forecast()
    print(object_json)
    df = pd.json_normalize(object_json)
    df = reorder(df)

    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    model_path = os.path.join(root_dir, 'models', 'linear')

    f = open(model_path, 'rb')
    model = pickle.load(f)

    prediction = model.predict(df)
    return jsonify({'prediction': prediction[0]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
