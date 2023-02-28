import pickle
import numpy as np
import pandas as pd
from flask import Flask
from flask import request
from flask import jsonify
import tensorflow as tf
from sklearn.model_selection import train_test_split

app = Flask(__name__)


def predict(object):
    
    object1 = object.drop("pm10", axis='columns')

    path = open("models/model.sav", 'rb')

    model = pickle.load(path)
    #model = tf.keras.models.load_model("C:\Users\lara.rantusa\FERI\MAG\IIS\Nal1\models\model.sav")

    x_train, x_test, y_train, y_test = train_test_split(object1, object["pm10"], test_size = 0.25, random_state = 789)

    prediction = model.predict(x_test)


    print("Prediction ", prediction)
    prediction = np.nan_to_num(prediction)
    prediction = np.array(prediction[:, 0]) 
    prediction = np.nan_to_num(prediction)
    print("Prediction1 ", prediction)
    #prediction = scaler.inverse_transform([prediction])
    return prediction[0, 0].astype(float)


@app.route('/predict', methods=['POST'])
def req_predict():
    object_json = request.json
    object = pd.DataFrame.from_dict(object_json)
    prediction = predict(object)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5000)