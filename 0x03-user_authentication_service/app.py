#!/usr/bin/env python3
"""the `app` module
a basic Flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, make_response, abort, redirect


app = Flask(__name__)


AUTH = Auth()


@app.route("/")
def index():
    """returns a simple json"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """a route function that accepts a user's data and registers it"""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return make_response(
            jsonify({"message": "email already registered"}), 400
        )


@app.route("/sessions", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response(jsonify({"email": email, "message": "logged in"}))
        resp.set_cookie("session_id", session_id)
        return resp
    abort(401)


@aqpp.route("/sessions", methods=['POST'])
def logout():
    session_id = request.form["session_id"]
    if AUTH.get_user_from_session_id(session_id):
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(session_id)
        return make_response(redirect("/"), 302)
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
