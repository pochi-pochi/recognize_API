from flask import Blueprint, jsonify, request
from study_api.api import calculation

api = Blueprint("api", __name__)

@api.get("/")
def index():
    return jsonify({"column": "value"}), 201

@api.post("/recognize")
def recognition():
    return calculation.recognition(request)