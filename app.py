from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
from functools import wraps
import jwt

app = Flask(__name__)

app.config["SECRET_KEY"] = "holamundo"

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token: request.args.get("token")
        if not token:
            return jsonify({"Alert":"Token is missing!"})
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"])
            return payload
        except:
            return jsonify({"Alert":"Invalid token!"})
    return decorated

@app.route("/public")
def public():
    return "For public"

@app.route("/auth")
@token_required
def auth(payload):
    if payload.password == "hola":
        return "JWT is verified. Welcome to your deshboard!"

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    print(username, password)
    if username and password:
        token = jwt.encode({"username":username,"password": password},app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"token":token})
    else:
        return jsonify("Unable to verify", 403)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)