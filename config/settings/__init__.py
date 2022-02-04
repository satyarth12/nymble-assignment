# Selecting appropriate settings
import os
import configparser

config = configparser.ConfigParser()
config.optionxform = str
config.read(os.path.abspath("config/settings/__env__.ini"))

ENV_INFO_ = config["env"]
SESNSITIVE_ = config["sensitive"]

if ENV_INFO_.get("SERVER_ENV") == "dev":
    from config.settings.dev import *
elif ENV_INFO_.get("SERVER_ENV") == "prod":
    from config.settings.prod import *
else:
    raise ValueError('No environment given')