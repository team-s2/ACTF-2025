import base64, json, time
import os, sys, binascii
from dataclasses import dataclass, asdict
from typing import Dict, Tuple
from secret import KEY, ADMIN_PASSWORD
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
)

app = Flask(__name__)
app.secret_key = KEY

if os.path.exists("/etc/ssl/nginx/local.key"):
    private_key = RSA.importKey(open("/etc/ssl/nginx/local.key", "r").read())
else:
    private_key = RSA.generate(2048)

public_key = private_key.publickey()


@dataclass
class APPUser:
    name: str
    password_raw: str
    register_time: int


#  In-memory store for user registration
users: Dict[str, APPUser] = {
    "admin": APPUser(name="admin", password_raw=ADMIN_PASSWORD, register_time=-1)
}


def validate_cookie(cookie_b64: str) -> bool:
    valid, _ = parse_cookie(cookie_b64)
    return valid


def parse_cookie(cookie_b64: str) -> Tuple[bool, str]:
    if not cookie_b64:
        return False, ""

    try:
        cookie = base64.b64decode(cookie_b64, validate=True).decode()
    except binascii.Error:
        return False, ""

    try:
        msg_str, sig_hex = cookie.split("&")
    except Exception:
        return False, ""

    msg_dict = json.loads(msg_str)
    msg_str_bytes = msg_str.encode()
    msg_hash = SHA256.new(msg_str_bytes)
    sig = bytes.fromhex(sig_hex)
    try:
        PKCS1_v1_5.new(public_key).verify(msg_hash, sig)
        valid = True
    except (ValueError, TypeError):
        valid = False
    return valid, msg_dict.get("user_name")


def generate_cookie(user: APPUser) -> str:
    msg_dict = {"user_name": user.name, "login_time": int(time.time())}
    msg_str = json.dumps(msg_dict)
    msg_str_bytes = msg_str.encode()
    msg_hash = SHA256.new(msg_str_bytes)
    sig = PKCS1_v1_5.new(private_key).sign(msg_hash)
    sig_hex = sig.hex()
    packed = msg_str + "&" + sig_hex
    return base64.b64encode(packed.encode()).decode()


@app.route("/")
def index():
    if validate_cookie(request.cookies.get("jwbcookie")):
        return redirect(url_for("home"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]
        if user_name in users:
            flash("Username already exists!", "danger")
        else:
            users[user_name] = APPUser(
                name=user_name, password_raw=password, register_time=int(time.time())
            )
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username].password_raw == password:
            resp = redirect(url_for("home"))
            resp.set_cookie("jwbcookie", generate_cookie(users[username]))
            return resp
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")


@app.route("/home")
def home():
    valid, current_username = parse_cookie(request.cookies.get("jwbcookie"))
    if not valid or not current_username:
        return redirect(url_for("logout"))

    user_profile = users.get(current_username)
    if not user_profile:
        return redirect(url_for("logout"))

    if current_username == "admin":
        payload = request.args.get("payload")
        if payload:
            for char in payload:
                if char in "'_#&;":
                    abort(403)
                    return

        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <h2 class="text-center">Welcome, %s !</h2>
        <div class="text-center">
            Your payload: %s
        </div>
        <img src="{{ url_for('static', filename='interesting.jpeg') }}" alt="Embedded Image">
        <div class="text-center">
            <a href="/logout" class="btn btn-danger">Logout</a>
        </div>
    </div>
</body>
</html>
""" % (
            current_username,
            payload,
        )
    else:
        html_template = (
            """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <h2 class="text-center">server code (encoded)</h2>
        <div class="text-center" style="word-break:break-all;">
        {%% raw %%}
            %s
        {%% endraw %%}
        </div>
        <div class="text-center">
            <a href="/logout" class="btn btn-danger">Logout</a>
        </div>
    </div>
</body>
</html>
"""
            % base64.b64encode(open(__file__, "rb").read()).decode()
        )
    return render_template_string(html_template)


@app.route("/logout")
def logout():
    resp = redirect(url_for("login"))
    resp.delete_cookie("jwbcookie")
    return resp


if __name__ == "__main__":
    app.run()