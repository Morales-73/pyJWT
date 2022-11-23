from flask import Flask, request, jsonify, make_response
from functools import wraps
import jwt

app = Flask(__name__)

app.config["SECRET_KEY"] = "holamundo"

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token: request.args.get("token")
#         print(token)
#         if not token:
#             return jsonify({"Alert":"Token is missing!"})
#         try:
#             payload = jwt.decode(token, app.config["SECRET_KEY"])
#         except:
#             return jsonify({"Alert":"Invalid token!"})
        
#         return f(payload, *args, **kwargs)
#     return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        
        if not token:
            return jsonify({"message":"Token is missing!"}), 401

        try:
            data = jwt.decode(token, app.secret_key, algorithms="HS256")
        except:
            response = jsonify({"message":"Invalid token or expired"})
            response.status_code = 401
            return response 

        # # try:
        # data = jwt.decode(token, app.secret_key)
        # # except:
        # #     return jsonify({"message":"Invalid token!"}), 401

        return f(data, *args, **kwargs)
    return decorated

@app.route("/public")
@token_required
def public():
    return "For public"

@app.route("/auth")
@token_required
def auth(data):
    if data:
        return jsonify({"message":"Succes","Token decoded":data})

# @app.route("/login", methods=["POST"])
# def login():
#     username = request.form["username"]
#     password = request.form["password"]
#     print(username, password)
#     if username and password:
#         token = jwt.encode({"username":username,"password": password},app.config["SECRET_KEY"], algorithm="HS256")
#         return jsonify({"token":token})
#     else:
#         return jsonify("Unable to verify", 403)

@app.route("/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify",401, {"WWW-Authnticate":"Basic realm='Login required!'"})

    username = auth["username"]
    password = auth["password"]

    if not username and password:
        return make_response("Could not verify",401, {"WWW-Authnticate":"Basic realm='Login required!'"})
    
    if username and password:
        token = jwt.encode({"username": username, "password":password}, app.secret_key)
        return jsonify({"token": token})
    return make_response("Could not verify",401, {"WWW-Authnticate":"Basic realm='Login required!'"})


# @app.route("/")
# def home():
#     return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)