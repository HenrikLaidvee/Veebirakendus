from flask import Blueprint, render_template, redirect, request, session, url_for

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/profile")
def profile_view():
    if "user" not in session:
        return redirect(url_for("login.login_view"))
    return render_template("profile.html")

@profile_bp.route("/logout", methods=["POST"])
def logout_view():
    session.pop("user", None)
    return redirect(url_for("login.login_view"))
