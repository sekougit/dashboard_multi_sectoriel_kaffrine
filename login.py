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
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Connexion — Dashboard Multi-Sectoriel Kaffrine</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<style>

:root{
    --vert-fonce:#14532d;
    --vert:#1f7a4d;
    --vert-vif:#27ae60;
    --terre:#d9a066;
    --creme:#f7f5ef;
    --texte:#16241c;
    --texte-att:rgba(255,255,255,.72);
}

*{
    box-sizing:border-box;
    margin:0;
    padding:0;
}

body{
    font-family:"Inter",Arial,sans-serif;
    color:var(--texte);
    min-height:100vh;
    display:flex;
}

/* ===================== PANNEAU GAUCHE (identité) ===================== */

.panneau-marque{
    position:relative;
    flex:1.1;
    min-height:100vh;
    background:var(--vert-fonce);
    color:white;
    overflow:hidden;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    padding:48px 56px;
}

.marque-scene{
    position:absolute;
    inset:0;
    z-index:0;
    background-image: url("/assets/fond_kaffrien.png");
    background-size:cover;
    background-position:center;
}

.marque-scene::before{
    content:"";
    position:absolute;
    inset:0;
    background:
        linear-gradient(180deg, rgba(20,83,45,.88) 0%, rgba(20,83,45,.55) 45%, rgba(20,83,45,.82) 100%);
}

.marque-contenu{
    position:relative;
    z-index:1;
}

.marque-eyebrow{
    font-size:12px;
    letter-spacing:.14em;
    text-transform:uppercase;
    color:var(--terre);
    font-weight:600;
    margin-bottom:18px;
}

.marque-titre{
    font-family:"Fraunces",serif;
    font-size:44px;
    font-weight:600;
    line-height:1.15;
    max-width:420px;
}

.marque-soustitre{
    margin-top:18px;
    font-size:15px;
    line-height:1.6;
    color:var(--texte-att);
    max-width:360px;
}

.marque-secteurs{
    position:relative;
    z-index:1;
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    max-width:420px;
}

.secteur-tag{
    font-size:12px;
    color:var(--texte-att);
    border:1px solid rgba(255,255,255,.22);
    border-radius:20px;
    padding:6px 12px;
}

/* ===================== PANNEAU DROIT (formulaire) ===================== */

.panneau-form{
    flex:1;
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    background:var(--creme);
    padding:40px 24px;
}

.login-box{
    width:100%;
    max-width:380px;
}

.login-header{
    margin-bottom:32px;
}

.login-badge{
    width:44px;
    height:44px;
    border-radius:12px;
    background:var(--vert-vif);
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:"Fraunces",serif;
    font-size:20px;
    font-weight:600;
    margin-bottom:20px;
}

.login-header h2{
    font-family:"Fraunces",serif;
    font-size:26px;
    font-weight:600;
    color:var(--texte);
}

.login-header p{
    margin-top:6px;
    font-size:14px;
    color:#5b6b60;
}

.error{
    background:#fdeceb;
    border:1px solid #f3c2bd;
    color:#9c3323;
    font-size:13px;
    padding:10px 14px;
    border-radius:8px;
    margin-bottom:20px;
}

form label{
    display:block;
    font-size:13px;
    font-weight:500;
    color:var(--texte);
    margin-bottom:6px;
}

form input{
    width:100%;
    padding:12px 14px;
    margin-bottom:18px;
    border:1px solid #d9d5c9;
    border-radius:10px;
    background:white;
    font-family:"Inter",sans-serif;
    font-size:14px;
    color:var(--texte);
    transition:border-color .15s, box-shadow .15s;
}

form input:focus{
    outline:none;
    border-color:var(--vert-vif);
    box-shadow:0 0 0 3px rgba(39,174,96,.15);
}

form input::placeholder{
    color:#a6a296;
}

button{
    width:100%;
    padding:13px;
    background:var(--vert-vif);
    color:white;
    border:none;
    border-radius:10px;
    cursor:pointer;
    font-family:"Inter",sans-serif;
    font-size:15px;
    font-weight:600;
    transition:background .15s;
}

button:hover{
    background:var(--vert-fonce);
}

.login-footer{
    margin-top:24px;
    text-align:center;
    font-size:12px;
    color:#8a8778;
}

/* ===================== RESPONSIVE ===================== */

@media(max-width:900px){

    body{
        flex-direction:column;
    }

    .panneau-marque{
        min-height:auto;
        padding:32px 28px;
        flex:none;
    }

    .marque-titre{
        font-size:28px;
    }

    .marque-soustitre,
    .marque-secteurs{
        display:none;
    }

    .panneau-form{
        min-height:auto;
        padding:36px 24px 48px;
    }

}

</style>
</head>

<body>

<div class="panneau-marque">

    <div class="marque-scene"></div>

    <div class="marque-contenu">
        <div class="marque-eyebrow">Région de Kaffrine</div>
        <h1 class="marque-titre">Dashboard Multi&#8209;Sectoriel</h1>
        <p class="marque-soustitre">
            Le suivi des indicateurs de développement territorial,
            secteur par secteur, commune par commune.
        </p>
    </div>

    <div class="marque-secteurs">
        <span class="secteur-tag">Agriculture</span>
        <span class="secteur-tag">Santé</span>
        <span class="secteur-tag">Éducation</span>
        <span class="secteur-tag">Élevage</span>
        <span class="secteur-tag">Eau</span>
        <span class="secteur-tag">+ 18 secteurs</span>
    </div>

</div>

<div class="panneau-form">

    <div class="login-box">

        <div class="login-header">
            <div class="login-badge">K</div>
            <h2>Connexion</h2>
            <p>Accédez à votre espace de suivi.</p>
        </div>

        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}

        <form method="POST">

            <label>Nom d'utilisateur</label>
            <input
                type="text"
                name="username"
                placeholder="Votre identifiant"
                required
                autofocus>

            <label>Mot de passe</label>
            <input
                type="password"
                name="password"
                placeholder="••••••••"
                required>

            <button type="submit">Se connecter</button>

        </form>

        <div class="login-footer">
            Dashboard Multi-Sectoriel Kaffrine — accès réservé
        </div>

    </div>

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

        error = "Nom d'utilisateur ou mot de passe incorrect ou utilisateur inactif."

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