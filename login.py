from flask import Blueprint, request, redirect, render_template_string, make_response
from flask_login import login_user, logout_user, current_user

from auth import User
from utils.google_users import authenticate

login_bp = Blueprint("login", __name__)


# ==========================================================
# PAGE LOGIN
# ==========================================================
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Connexion</title>

<style>

body{
    font-family:Arial;
    background:#f5f5f5;
}

.login-box{
    width:380px;
    margin:80px auto;
    background:white;
    padding:30px;
    border-radius:10px;
    box-shadow:0 0 12px rgba(0,0,0,.15);
}

input{
    width:100%;
    padding:10px;
    margin-top:8px;
    margin-bottom:18px;
    box-sizing:border-box;
}

button{
    width:100%;
    padding:12px;
    background:#0d6efd;
    color:white;
    border:none;
    cursor:pointer;
    font-size:16px;
}

button:hover{
    background:#0b5ed7;
}

.error{
    color:red;
    margin-bottom:15px;
}

</style>

</head>

<body>

<div class="login-box">

<h2>Connexion</h2>

{% if error %}
<div class="error">{{ error }}</div>
{% endif %}

<form method="POST">

<label>Nom d'utilisateur</label>
<input
    type="text"
    name="username"
    required
    autofocus>

<label>Mot de passe</label>
<input
    type="password"
    name="password"
    required>

<button type="submit">
    Se connecter
</button>

</form>

</div>

</body>
</html>
"""


# ==========================================================
# LOGIN
# ==========================================================
@login_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect("/")

    error = None

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = authenticate(username, password)

        if user:

            login_user(
                User(user),
                remember=True
            )

            return redirect("/")

        error = "Nom d'utilisateur ou mot de passe incorrect."

    response = make_response(
        render_template_string(
            LOGIN_HTML,
            error=error
        )
    )

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


# ==========================================================
# LOGOUT
# ==========================================================
@login_bp.route("/logout")
def logout():

    logout_user()

    return redirect("/login")