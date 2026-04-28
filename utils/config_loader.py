import yaml
import os

def config_loader(config_path:str ="config/config.yaml"):
    try:
        with open(config_path,"r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print("No Config file exists")
    
    return config
