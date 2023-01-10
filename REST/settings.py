#! /usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from flask_jwt_extended import JWTManager


app = Flask(__name__, static_url_path="/static")
jwt = JWTManager(app)
CORS(app, support_credentials=True)
app.secret_key = "changeme"
engine = create_engine("mysql+pymysql://root:password@localhost:3307/agentless", pool_size=100)

app.config["JWT_JSON_KEY"] = "jwt"
app.config["JWT_QUERY_STRING_NAME"] = "jwt"
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 28800  # 8 hours
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 999928800
app.config["WTF_CSRF_ENABLED"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
