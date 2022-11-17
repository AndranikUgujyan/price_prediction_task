import yaml


def get_input_text(data, log):
    try:
        log.debug(f'started')
        if data["RAM_GB"] and data["HDD_GB"] and data["GHz"] and data["brand"]:
            return data
    except Exception as e:
        log.exception(f"can't get input text from: {data}")
        raise ValueError(str(e))


def error_response(message, log):
    log.debug(f"started, message={message}")
    return {"result": "Fail", "ErrorMessage": message}, 500


def load_cfg(yaml_file_path: str):
    """
    Load a YAML configuration file.
    """

    with open(yaml_file_path, 'r') as stream:
        cfg = yaml.load(stream, Loader=yaml.SafeLoader)
    return cfg
