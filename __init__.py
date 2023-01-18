from flask import Flask, jsonify, request

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    return app