import os
import json
import os

import pandas as pd

import price_model
from flask import Flask, request
from price_model import app_config, logger
from price_model.predicter.model_predictor import ModelPredictor
from price_model.utils.help_func import error_response, get_input_text

ABS_DIR_PATH = os.path.dirname(os.path.abspath(price_model.__file__))

app = Flask(__name__)

BRAND_CAT = {'Samsung': 0,
             'Lenovo': 1,
             'Acer': 2,
             'HP': 3,
             'MSI': 4,
             'DELL': 5,
             'Toshiba': 6,
             'asus': 7,
             'Dell': 8,
             'Apple': 9,
             'Asus': 10,
             'Microsoft': 11,
             'hp': 12,
             'unknown': 13}


@app.route('/predict_price', methods=['POST'])
def predict_product():
    try:
        log_headers_and_ip(request)
        _data = request.data.decode('utf-8')
        logger.debug(f'started, data:{_data}')
        j_obj = json.loads(_data)
        logger.debug('get client instance')
        model_path = config_model(j_obj['data'][0]["model"])
        model_client = ModelPredictor(model_path)
        data_for_prediction = get_input_text(j_obj['data'][0], logger)
        data_for_prediction["brand_cat"] = BRAND_CAT[data_for_prediction["brand"]]

        del data_for_prediction["brand"]
        del data_for_prediction["model"]
        data_for_pred = pd.DataFrame([data_for_prediction])
        print(data_for_pred)
        prediction = model_client.predict(data_for_pred)
        result = {"price": round(prediction)}
        response = app.response_class(response=json.dumps(result, indent=True),
                                      status=200,
                                      mimetype='application/json')
        return response
    except Exception as err:
        return error_response(f'error={err}', logger)


def config_model(model_name):
    try:
        if model_name == "rf":
            model_path = os.path.join(ABS_DIR_PATH, app_config['model_1_path'])
            return model_path
        if model_name == "lr":
            model_path = os.path.join(ABS_DIR_PATH, app_config['model_2_path'])
            return model_path
        if model_name == "lasso":
            model_path = os.path.join(ABS_DIR_PATH, app_config['model_3_path'])
            return model_path
        if model_name == "xgb":
            model_path = os.path.join(ABS_DIR_PATH, app_config['model_4_path'])
            return model_path
    except Exception as err:
        return error_response(f'error={err}', logger)


def log_headers_and_ip(request):
    logger.debug('started')
    try:
        logger.debug(f'IP:{request.remote_addr}')
        logger.debug(f'headers:{request.headers}')
    except Exception:
        logger.exception('unable to log headers and IP.')


@app.errorhandler(500)
def server_error(e):
    logger.exception('error occurred during a request.')
    return f"An internal error occurred: <pre>{e}</pre>See logs for full stacktrace.", 500


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
