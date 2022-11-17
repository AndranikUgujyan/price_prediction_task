import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_log_error, mean_absolute_error, r2_score
import price_model
from price_model import app_config
from sklearn.linear_model import LinearRegression, Lasso
import pickle
import xgboost as xg
import dataframe_image as dfi

abs_dir_path = os.path.dirname(os.path.abspath(price_model.__file__))

ALL_MODELS_RESULT_PLOT_ABS_PATH = os.path.join(abs_dir_path, app_config["all_models_result_plot_path"])

train_data_abs_path = os.path.join(abs_dir_path, app_config['train_data_path'])
test_data_abs_path = os.path.join(abs_dir_path, app_config['test_data_path'])

train_df = pd.read_csv(train_data_abs_path)
test_df = pd.read_csv(test_data_abs_path)

train_data = train_df.drop(["price", "brand"], axis=1)
train_labels = train_df["price"]

test_data = test_df.drop(["price", "brand"], axis=1)
test_labels = test_df["price"]


def rmsle(y_test, y_preds):
    """
    Caculates root mean squared log error between predictions and
    true labels.
    """
    return np.sqrt(mean_squared_log_error(y_test, y_preds))


def show_scores(model, model_name):
    train_preds = model.predict(train_data)
    test_preds = model.predict(test_data)

    scores = {"Training MAE": mean_absolute_error(train_labels, train_preds),
              "Test MAE": mean_absolute_error(test_labels, test_preds),
              "Training RMSLE": rmsle(train_labels, train_preds),
              "Test RMSLE": rmsle(test_labels, test_preds),
              "Training R^2": r2_score(train_labels, train_preds),
              "Test R^2": r2_score(test_labels, test_preds),
              "model_name": model_name}
    return scores


rf_model = RandomForestRegressor(n_jobs=-1, random_state=42)
rf_model.fit(train_data, train_labels)
rf_score = show_scores(rf_model, "rf")

lr_model = LinearRegression()
lr_model.fit(train_data, train_labels)
lr_score = show_scores(rf_model, "lr")

lasso_model = Lasso()
lasso_model.fit(train_data, train_labels)
lasso_score = show_scores(rf_model, "lasso")

xgb_model = xg.XGBRegressor(objective='reg:linear', n_estimators=10, seed=42)
xgb_model.fit(train_data, train_labels)
xgb_score = show_scores(xgb_model, "xgb")

score_df = pd.DataFrame([rf_score, xgb_score, lr_score, lasso_score])
all_models_results_path = os.path.join(abs_dir_path, app_config['all_models_result_plot_path'])
df_styled = score_df.style.background_gradient()
dfi.export(df_styled, all_models_results_path)


print(score_df)

model_1_abs_path = os.path.join(abs_dir_path, app_config['model_1_path'])
model_2_abs_path = os.path.join(abs_dir_path, app_config['model_2_path'])
model_3_abs_path = os.path.join(abs_dir_path, app_config['model_3_path'])
model_4_abs_path = os.path.join(abs_dir_path, app_config['model_3_path'])

pickle.dump(rf_model, open(model_1_abs_path, 'wb'))
pickle.dump(lr_model, open(model_2_abs_path, 'wb'))
pickle.dump(lasso_model, open(model_3_abs_path, 'wb'))
pickle.dump(xgb_model, open(model_4_abs_path, 'wb'))
