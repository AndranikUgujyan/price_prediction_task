import pickle

from price_model import logger
from price_model.utils.help_func import error_response


class ModelSavingLoading:

    def __init__(self):
        super(ModelSavingLoading, self).__init__()

    def load_model(self, model_path):
        logger.debug(f'Start loading model from {model_path}')
        try:
            with open(model_path, 'rb') as handle:
                model = pickle.load(handle)

            logger.debug(f'Loading complete from {model_path}')
            return model
        except Exception as err:
            return error_response(f'error={err}', logger)



