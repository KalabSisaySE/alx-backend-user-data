#!/usr/bin/env python3
"""the `app` module
a basic Flask app
"""
from flask import Flask, jsonify, request, make_response


app = Flask(__name__)
from auth import Auth


AUTH = Auth()

@app.route("/")
def index():
    """returns a simple json"""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def users():
    """a route function that accepts a user's data and registers it"""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return make_response(jsonify({"message": "email already registered"}), 400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
