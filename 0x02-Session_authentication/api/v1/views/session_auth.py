#!/usr/bin/env python3
""" Module of session Auth views
"""
import os
from flask.json import jsonify
from flask import request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')

    if user_email is None:
        return jsonify({'error': 'email missing'}), 400

    if user_pwd is None:
        return jsonify({'error': 'password missing'}), 400

    user_list = User.search({'email': user_email})

    if len(user_list) == 0:
        return jsonify({'error': 'no user found for this email'}), 404

    user = user_list[0]
    if not user.is_valid_password(user_pwd):
        return jsonify({'error': 'wrong password'}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response
