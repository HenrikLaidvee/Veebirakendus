from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
import firebase_admin
from firebase_admin import auth, credentials
from .db import get_db

login = Blueprint('login', __name__)

@login.route("/login", methods=["GET"])
def login_view():
    return render_template("login.html")

@login.route("/session", methods=["POST"])
def create_session():
    id_token = request.json.get("idToken")
    try:
        # Firebase tokeni valideerimine
        decoded_token = auth.verify_id_token(id_token)
        email = decoded_token.get("email")
        display_name = decoded_token.get("name", "")

        # Salvesta sessiooni
        session["user"] = {
            "email": email,
            "displayName": display_name
        }

        # Kontrolli või lisa kasutaja PostgreSQL andmebaasi
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM Kasutaja WHERE email = %s", (email,))
        row = cur.fetchone()

        if not row:
            # Lisa uus kasutaja, kui teda pole
            cur.execute("INSERT INTO Kasutaja (email) VALUES (%s) RETURNING user_id", (email,))
            user_id = cur.fetchone()[0]
            conn.commit()
        else:
            user_id = row[0]

        # Salvesta ka kasutaja ID sessiooni
        session["user_id"] = user_id

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Sessiooni loomise viga:", e)
        return jsonify({"error": str(e)}), 401
