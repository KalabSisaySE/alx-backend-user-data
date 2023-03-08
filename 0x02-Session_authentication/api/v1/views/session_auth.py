#!/usr/bin/env python3
"""the `session_auth` module
creates a new view for `session_auth` module
"""
from flask import abort, jsonify, request, make_response
import os
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", strict_slashes=False, methods=["POST"])
def login():
    """creates a session when a user logs in"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if len(users) > 0:
        user = users[0]
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth

            session_id = auth.create_session(user.id)
            resp = make_response(jsonify(user.to_json()))
            name = os.getenv("SESSION_NAME")
            resp.set_cookie(name, session_id)
            return resp
    else:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route("/auth_session/logout",
                 strict_slashes=False,
                 methods=["DELETE"])
def logout():
    """deletes the current session of a user"""
    from api.v1.app import auth
    session_deleted = auth.destroy_session(request)
    if session_deleted:
        return jsonify({}), 200
    else:
        abort(404)
