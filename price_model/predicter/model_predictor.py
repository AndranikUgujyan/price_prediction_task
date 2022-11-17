from price_model import logger

from price_model.saving_loading.model_saving_loading import ModelSavingLoading


class ModelPredictor:

    def __init__(self, model_path: str):
        loader = ModelSavingLoading()
        self._model = loader.load_model(model_path)

    def predict(self, product_info_df):
        logger.debug('start prediction')
        predicted_price = self._model.predict(product_info_df)
        return predicted_price[0]
