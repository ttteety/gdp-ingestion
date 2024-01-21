import yaml 

def read_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)
    return config_data