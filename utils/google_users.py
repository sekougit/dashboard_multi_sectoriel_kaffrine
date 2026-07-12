import io
import os
import time
import bcrypt
import requests
import pandas as pd

# ==========================================================
# CONFIGURATION
# ==========================================================
SHEET_ID = os.getenv("USERS_SHEET_ID"
)

CACHE_DURATION = 60  # 5 minutes

DOWNLOAD_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"
)

# ==========================================================
# CACHE
# ==========================================================
_users_cache = None
_last_refresh = 0


# ==========================================================
# TELECHARGEMENT
# ==========================================================
def download_users():

    response = requests.get(
        DOWNLOAD_URL,
        timeout=30
    )

    response.raise_for_status()

    # Vérifie que Google renvoie bien un fichier Excel
    if "application/vnd.openxmlformats" not in response.headers.get(
        "Content-Type", ""
    ):
        raise Exception(
            "Le Google Sheet n'est pas accessible. Vérifiez le partage du fichier."
        )

    df = pd.read_excel(
        io.BytesIO(response.content)
    )

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    df.fillna("", inplace=True)

    return df.to_dict("records")


# ==========================================================
# UTILISATEURS
# ==========================================================
def get_all_users():

    global _users_cache
    global _last_refresh

    now = time.time()

    if (
        _users_cache is None
        or now - _last_refresh > CACHE_DURATION
    ):

        try:

            print("🔄 Actualisation des utilisateurs...")

            _users_cache = download_users()

            _last_refresh = now

            print(f"✅ {len(_users_cache)} utilisateurs chargés.")

        except Exception as e:

            print("❌ Erreur téléchargement :", e)

            if _users_cache is None:
                return []

    return _users_cache


# ==========================================================
# RECHERCHE
# ==========================================================
def get_user(username):

    username = username.strip().lower()

    for user in get_all_users():

        if str(user.get("username", "")).strip().lower() == username:
            return user

    return None


# ==========================================================
# AUTHENTIFICATION
# ==========================================================
def authenticate(username, password):

    user = get_user(username)

    if user is None:
        return None

    active = str(
        user.get("active", True)
    ).strip().lower()

    if active not in ("true", "1", "yes", "oui"):
        return None

    password_hash = str(
        user.get("password", "")
    ).strip()

    if password_hash == "":
        return None

    try:

        if not bcrypt.checkpw(
            password.encode(),
            password_hash.encode()
        ):
            return None

    except Exception:
        return None

    return {
        "username": user["username"],
        "fullname": user["fullname"],
        "role": user["role"],
        "direction": user["direction"],
        "active": True
    }


# ==========================================================
# HASH PASSWORD
# ==========================================================
def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()