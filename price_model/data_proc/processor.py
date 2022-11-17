import os
import price_model
import pandas as pd
from sklearn.model_selection import train_test_split

from price_model import app_config

random_state = 42
ABS_DIR_PATH = os.path.dirname(os.path.abspath(price_model.__file__))


def read_and_normalize_dataset(dataset_path):
    dataset_df = pd.read_csv(dataset_path, sep='\t')

    dataset_df["brand"] = dataset_df["brand"].astype('category')

    dataset_df["brand_cat"] = dataset_df.brand.replace(
        to_replace=['Samsung',
                    'Lenovo',
                    'Acer',
                    'HP',
                    'MSI',
                    'DELL',
                    'Toshiba',
                    'asus',
                    'Dell',
                    'Apple',
                    'Asus',
                    'Microsoft',
                    'hp',
                    'unknown'],
        value=[0,
               1,
               2,
               3,
               4,
               5,
               6,
               7,
               8,
               9,
               10,
               11,
               12,
               13])

    return dataset_df


def split_train_val_test(normalized_df):
    train_df, test_df = train_test_split(normalized_df.drop("productid", axis=1), test_size=0.1)
    return train_df, test_df


if __name__ == "__main__":
    abs_dir_path = os.path.dirname(os.path.abspath(price_model.__file__))

    path_of_dataset = os.path.join(abs_dir_path, app_config['main_dataset'])

    path_of_train = os.path.join(abs_dir_path, app_config['train_data_path'])
    path_of_test = os.path.join(abs_dir_path, app_config['test_data_path'])

    main_data_plot_abs_path = os.path.join(ABS_DIR_PATH, app_config["main_data_plot_path"])
    data_df = read_and_normalize_dataset(path_of_dataset)

    train, test = split_train_val_test(data_df)

    train.to_csv(path_of_train, index=False)
    test.to_csv(path_of_test, index=False)
