#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.auth import Auth, BasicAuth, SessionAuth, SessionExpAuth
from api.v1.auth import SessionDBAuth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if os.getenv("AUTH_TYPE", None) == "auth":
    auth = Auth()
elif os.getenv("AUTH_TYPE", None) == "basic_auth":
    auth = BasicAuth()
elif os.getenv("AUTH_TYPE", None) == "session_auth":
    auth = SessionAuth()
elif os.getenv("AUTH_TYPE", None) == "session_exp_auth":
    auth = SessionExpAuth()
elif os.getenv("AUTH_TYPE", None) == "session_db_auth":
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """Function called before any view
    """
    if auth is not None:
        request.current_user = auth.current_user(request)
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/',
            ]
        if not auth.require_auth(request.path, excluded_paths):
            print("Authentication Not required")
            return
        if auth.authorization_header(request) is None \
           and auth.session_cookie(request) is None:
            abort(401)
        if request.current_user is None:
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
