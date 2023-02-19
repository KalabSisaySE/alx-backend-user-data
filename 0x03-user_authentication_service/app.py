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
    """saves login information using a session_id and stores it in a cookie"""
    email = request.form["email"]
    password = request.form["password"]
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response(jsonify({"email": email, "message": "logged in"}))
        resp.set_cookie("session_id", session_id)
        return resp
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """deletes the session of the logged in user"""
    session_id = request.cookies.get("session_id")
    if AUTH.get_user_from_session_id(session_id):
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(session_id)
        return make_response(redirect("/"), 302)
    else:
        abort(403)


@app.route("/profile")
def profile():
    """checks if the user is logged in and returns the email"""
    if request.cookies.get("session_id"):
        session_id = request.cookies.get("session_id")
        if AUTH.get_user_from_session_id(session_id):
            user = AUTH.get_user_from_session_id(session_id)
            return make_response(jsonify({"email": user.email}))
    abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """endpoint to get a password reset token"""
    email = request.form['email']
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return make_response(
            jsonify({"email": email, "reset_token": reset_token}), 200
        )
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """endpoint to update an existing password using a reset token"""
    try:
        AUTH.update_password(
            request.form['reset_token'],
            request.form['new_password']
        )
        return make_response(
            jsonify(
                {
                    "email": request.form['email'],
                    "message": "Password updated"
                }
            )
        )
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
