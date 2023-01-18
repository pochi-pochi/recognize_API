import os

from flask import Flask

from study_api.api import api
from study_api.api.config import config

config_name = os.environ.get("CONFIG", "local")

app = Flask(__name__)
app.config.from_object(config[config_name])

#blueprintをアプリケーションに登録
app.register_blueprint(api)