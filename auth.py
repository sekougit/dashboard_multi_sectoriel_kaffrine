from flask_login import LoginManager, UserMixin
from utils.google_users import get_user
import os
# ==========================================================
# LOGIN MANAGER
# ==========================================================
login_manager = LoginManager()

login_manager.login_view = "login.login"
login_manager.login_message = ""
login_manager.session_protection = "strong"
login_manager.refresh_view = "login.login"


# ==========================================================
# USER CLASS
# ==========================================================
class User(UserMixin):

    def __init__(self, user_data):

        self.id = user_data["username"]

        self.username = user_data["username"]

        self.fullname = user_data["fullname"]

        self.role = user_data["role"]

        self.direction = user_data["direction"]

        self.active = bool(user_data.get("active", True))

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return self.username


# ==========================================================
# USER LOADER
# ==========================================================
@login_manager.user_loader
def load_user(username):

    user = get_user(username)

    if user is None:
        return None

    return User(user)


# ==========================================================
# INITIALISATION
# ==========================================================
def init_auth(app):

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    # Sécurité des cookies
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Mettre True lorsque le site sera en HTTPS sur Render
    app.config["SESSION_COOKIE_SECURE"] = False

    # Durée de la session
    app.config["REMEMBER_COOKIE_DURATION"] = 60 * 60 * 24 * 30

    login_manager.init_app(app)