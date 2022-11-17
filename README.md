# Price Prediction API
***
#### Clone repository 
    
    git clone https://github.com/AndranikUgujyan/price_prediction_task.git

#### Install and create virtual environment

    pip install virtualenv

    virtualenv venv

#### Activate a virtual environment

    source venv/bin/activate

#### Install required packages

    pip3 install -r requirements.txt
***
### Data:

We have balanced datasets.
![imbalanced datasets](price_model/data_plots/main_data_plot.png)

To preprocess and split dataset into train/test run:
    
    python -m price_model.data_proc.processor

The command will generate normal sampled datasets and will save as a csv files inside data folder.

***

## Models:

* Model 1: Random Forest Regressor 
* Model 2: XGB Regressor

***
### Model Train and Save

For train and save model based on normalized data run:

    python -m price_model.training.train

***
### Comparing the performance of each of models

Model's performances
![imbalanced datasets](price_model/models_results_plots/all_models_results.png)

Sorted model results by f1-score
![imbalanced datasets](price_model/models_results_plots/all_models_f1_score.png)
***

## Run API
***
We have 2 option to run API:
1. without docker
2. inside docker
***
### Run API without docker

     python3 -m price_model.app

#### Test API without docker

     curl  -X POST -d '{"data": [{"brand":"Samsung","RAM_GB":1000,"GHz":3.2, "HDD_GB":1000,"model":"rf"}]}' http://127.0.0.1:8080/predict_price -H "Content-Type:application/json"

***

### Run API inside docker docker

#### Build docker image

    docker build -t predict-price-api:1.0 -f Dockerfile .
    
#### Run docker

    docker run -e PORT=8080 --name imbd -p "7894:8080" predict-price-api:1.0
    
#### Test API in docker

    curl  -X POST -d '{"data": [{"brand":"Samsung","RAM_GB":1000,"GHz":3.2, "HDD_GB":1000,"model":"rf"}]}'  http://127.0.0.1:7894/predict_price -H "Content-Type:application/json"

***

**Here is an example response of `predict_price` prediction endpoint:**

```json
{
 "price": 81981
}
```