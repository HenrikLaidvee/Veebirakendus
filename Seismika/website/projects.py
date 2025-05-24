from flask import Blueprint, render_template, session, redirect, request
from .db import get_db

projects = Blueprint('projects', __name__)

@projects.route("/projektid", methods=["GET", "POST"])
def projektid():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    email = session["user"]["email"]

    # Kustutamine (kui on POST ja valitud projektid)
    if request.method == "POST":
        ids = request.form.getlist("kustutatavad")
        if ids:
            for projekt_id in ids:
                # kustuta seotud regressioonid
                cur.execute("DELETE FROM Regression WHERE projekt_id = %s", (projekt_id,))
                # kustuta projekt
                cur.execute("DELETE FROM Projekt3 WHERE projekt_id = %s", (projekt_id,))
            conn.commit()

    # Lae projektid pärast kustutamist või tavapäraselt
    cur.execute("""
        SELECT projekt_id, nimetus, tahtaeg 
        FROM Projekt3
        WHERE user_id = (
            SELECT user_id FROM Kasutaja WHERE email = %s
        )
        ORDER BY tahtaeg DESC
    """, (email,))
    projektid_data = cur.fetchall()

    projektid_list = []
    for row in projektid_data:
        projektid_list.append({
            "id": row[0],
            "nimetus": row[1],
            "tahtpaev": row[2]
        })

    return render_template("projects.html", projektid=projektid_list)
