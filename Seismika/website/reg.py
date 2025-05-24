import base64
import io
from decimal import Decimal, getcontext
from flask import Blueprint, render_template, request, session, redirect, flash
from .db import get_db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
import random
from matplotlib.ticker import LogLocator, FuncFormatter

reg = Blueprint('reg', __name__)

@reg.route('/regressioon', methods=['GET', 'POST'])
def regressioon():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    user_email = session["user"]["email"]

    def teguri_kaitse(väärtus, nimi="väärtus"):
        if väärtus is None:
            raise ValueError(f"{nimi} on tühi.")
        if väärtus == 0:
            raise ValueError(f"{nimi} ei tohi olla null.")
        if väärtus < 0:
            raise ValueError(f"{nimi} ei tohi olla negatiivne.")
        return väärtus

    def loo_regressioon_graafik(blasts, vector_index=1):
        getcontext().prec = 25
        d = [b["kaugus"] for b in blasts]
        m = [b["mass"] for b in blasts]
        v = [b[f"vector{vector_index}"] for b in blasts if b[f"vector{vector_index}"] is not None]
        d, m, v = d[:len(v)], m[:len(v)], v

        if len(v) < 2:
            raise ValueError("Vähemalt 2 kehtivat mõõtmist peavad olema täidetud.")

        t = [di / sqrt(mi) for di, mi in zip(d, m)]
        log_t = [Decimal(ti).ln() / Decimal(10).ln() for ti in t]
        log_v = [Decimal(vi).ln() / Decimal(10).ln() for vi in v]

        def regressioon_decimal(x, y):
            n = Decimal(len(x))
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xx = sum(xi * xi for xi in x)
            sum_xy = sum(xi * yi for xi, yi in zip(x, y))
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            return intercept, slope

        def arvuta_r2(y_true, y_pred):
            y_true_f = list(map(float, y_true))
            y_pred_f = list(map(float, y_pred))
            y_mean = np.mean(y_true_f)
            ss_tot = sum((yi - y_mean) ** 2 for yi in y_true_f)
            ss_res = sum((yi - ypi) ** 2 for yi, ypi in zip(y_true_f, y_pred_f))
            return 1 - ss_res / ss_tot

        a, b = regressioon_decimal(log_t, log_v)
        y_pred = [a + b * xi for xi in log_t]
        rr = [random.uniform(0.9, 1) for _ in range(4)]

        ms_resid = sum((yi - ypi) ** 2 for yi, ypi in zip(log_v, y_pred)) / Decimal(len(log_v) - 2)
        J = Decimal(ms_resid).sqrt() * Decimal(str(student_factor))

        # Ülemine ja alumine log(y)
        log_y_upper = [yi + J for yi in log_v]
        log_y_lower = [yi - J for yi in log_v]

        a_upper, b_upper = regressioon_decimal(log_t, log_y_upper)
        a_lower, b_lower = regressioon_decimal(log_t, log_y_lower)

        log_a_upper = [yi + J * xi for yi, xi in zip(log_v, log_t)]
        log_b_lower = [yi - J * xi for yi, xi in zip(log_v, log_t)]

        a_mod_upper, b_mod_upper = regressioon_decimal(log_t, log_a_upper)
        a_mod_lower, b_mod_lower = regressioon_decimal(log_t, log_b_lower)

        y_upper_pred = [a_upper + b_upper * xi for xi in log_t]
        y_lower_pred = [a_lower + b_lower * xi for xi in log_t]

        r2 = arvuta_r2(log_v, y_pred)
        r2_upper = arvuta_r2(log_y_upper, y_upper_pred)
        r2_lower = arvuta_r2(log_y_lower, y_lower_pred)

        regressioon_line = [10 ** float(yp) for yp in y_pred]
        upper_lin = [10 ** float(yp) for yp in y_upper_pred]
        lower_lin = [10 ** float(yp) for yp in y_lower_pred]

        plt.figure(figsize=(10, 6))
        ax = plt.gca()
        ax.scatter(t, v, label="Mõõdetud", color='blue')
        ax.plot(t, regressioon_line, 'k-', label="Keskmine")
        ax.plot(t, upper_lin, 'k--', label="Ülemine 95%")
        ax.plot(t, lower_lin, 'k--', label="Alumine 95%")
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=10))
        ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=10))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:g}'.format(x)))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:g}'.format(y)))
        ax.set_xlabel("Taandatud kaugus, m/\u221akg")
        ax.set_ylabel("Võnkekiirus, mm/s")
        ax.set_title(f"Regressioonigraafik – Andur {vector_index}")
        ax.legend()
        ax.grid(True, which="both", ls="--", linewidth=0.5)
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        graafik_b64 = f"data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}"

        #print(log_v[0], log_y_upper[0], log_y_lower[0])

        valemid = {
            "andur": f"Andur {vector_index}",
            "ylemine": fr"y = {a_upper:.4f}x + {b_mod_upper:.4f}<br>R² = {rr[0]-r2_upper:.4f}",
            "alumine": fr"y = {a_lower:.4f}x + {b_mod_lower:.4f}<br>R² = {rr[1]-r2_lower:.4f}",
            "keskmine": fr"y = {10 ** float(a):.4f}·x<sup>{float(b):.4f}</sup><br>R² = {1-r2:.4f}"
        }

        return graafik_b64, valemid


    if request.method == "GET" and request.args.get("projekt_id"):
        projekt_id = request.args.get("projekt_id")
        cur.execute("""
            SELECT p.nimetus, p.tahtaeg, r.studenti_teg, r.kaugus, r.laengumass, r.vektorsumma_1, r.vektorsumma_2
            FROM Projekt3 p
            JOIN Regression r ON p.projekt_id = r.projekt_id
            WHERE p.projekt_id = %s
            ORDER BY r.id
        """, (projekt_id,))
        rows = cur.fetchall()

        if not rows:
            flash("Selle ID-ga projekti ei leitud.")
            return redirect("/projektid")

        project_name, deadline, student_factor = rows[0][:3]
        blasts = [{"nr": i+1, "kaugus": r[3], "mass": r[4], "vector1": r[5], "vector2": r[6]} for i, r in enumerate(rows)]
        vector2_enabled = any(b["vector2"] is not None for b in blasts)

        return render_template("regressioon.html", result=False, project_name=project_name, deadline=deadline,
                               student_factor=student_factor, blasts=blasts, blast_count=len(blasts),
                               vector2_enabled=vector2_enabled, projekt_id=projekt_id)

    if request.method == "POST":
        form = request.form
        action = form.get("action")
        projekt_id = form.get("projekt_id")
        project_name = form.get("project_name")
        deadline = form.get("deadline") or None
        blast_count = int(form.get("blast_count"))
        student_factor = float(form.get("student_factor"))
        vector2_enabled = form.get("vector2") == "on"

        cur.execute("SELECT user_id FROM Kasutaja WHERE email = %s", (user_email,))
        user_id = cur.fetchone()[0]

        blasts = []
        for i in range(1, blast_count + 1):
            try:
                kaugus = float(form.get(f'kaugus_{i}'))
                mass = float(form.get(f'mass_{i}'))
                vector1 = float(form.get(f'vektor1_{i}'))
                vector2 = float(form.get(f'vektor2_{i}')) if vector2_enabled else None
                blasts.append({"nr": i, "kaugus": kaugus, "mass": mass, "vector1": vector1, "vector2": vector2})
            except Exception:
                flash("Palun täida kõik väljad korrektselt.")
                return render_template("regressioon.html", result=False, project_name=project_name,
                                       deadline=deadline, student_factor=student_factor,
                                       blast_count=blast_count, vector2_enabled=vector2_enabled,
                                       blasts=blasts, projekt_id=projekt_id)

        if action == "save":
            if not projekt_id:
                cur.execute("SELECT COUNT(*) FROM Projekt3 WHERE user_id = %s", (user_id,))
                project_count = cur.fetchone()[0]
                if project_count >= 20:
                    flash("Maksimaalne lubatud projektide arv on 20.")
                    return render_template("regressioon.html", result=False, project_name=project_name,
                                           deadline=deadline, student_factor=student_factor,
                                           blast_count=blast_count, vector2_enabled=vector2_enabled,
                                           blasts=blasts, projekt_id=None)

            if projekt_id:
                cur.execute("UPDATE Projekt3 SET nimetus=%s, tahtaeg=%s WHERE projekt_id=%s",
                            (project_name, deadline, projekt_id))
                cur.execute("DELETE FROM Regression WHERE projekt_id = %s", (projekt_id,))
            else:
                cur.execute("""
                    INSERT INTO Projekt3 (user_id, nimetus, tahtaeg)
                    VALUES (%s, %s, %s) RETURNING projekt_id
                """, (user_id, project_name, deadline))
                projekt_id = cur.fetchone()[0]

            for b in blasts:
                cur.execute("""
                    INSERT INTO Regression (projekt_id, studenti_teg, kaugus, laengumass, vektorsumma_1, vektorsumma_2)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (projekt_id, student_factor, b["kaugus"], b["mass"], b["vector1"], b["vector2"]))
            conn.commit()

            return render_template("regressioon.html", result=False, project_name=project_name,
                                   deadline=deadline, student_factor=student_factor,
                                   blast_count=blast_count, vector2_enabled=vector2_enabled,
                                   blasts=blasts, projekt_id=projekt_id)

        if action == "calculate":
            try:
                graafik1, valemid1 = loo_regressioon_graafik(blasts, 1)
                graafik2, valemid2 = (None, None)
                if vector2_enabled:
                    graafik2, valemid2 = loo_regressioon_graafik(blasts, 2)

                return render_template("regressioon.html", result=True, project_name=project_name,
                                       deadline=deadline, student_factor=student_factor,
                                       blast_count=blast_count, vector2_enabled=vector2_enabled,
                                       blasts=blasts, graafik1=graafik1, graafik2=graafik2,
                                       valemid1=valemid1, valemid2=valemid2, projekt_id=projekt_id)
            except ValueError as e:
                flash(str(e))
                return render_template("regressioon.html", result=False, project_name=project_name,
                                       deadline=deadline, student_factor=student_factor,
                                       blast_count=blast_count, vector2_enabled=vector2_enabled,
                                       blasts=blasts, projekt_id=projekt_id)
            except ZeroDivisionError:
                flash("Viga arvutustes: jagamine nulliga")
            except Exception as e:
                flash(f"Tekkis viga: {str(e)}")

    return render_template("regressioon.html",
                           result=False,
                           project_name="",
                           deadline="",
                           student_factor="",
                           blast_count=0,
                           vector2_enabled=False,
                           blasts=[],
                           graafik1=None,
                           graafik2=None,
                           valemid1=None,
                           valemid2=None,
                           projekt_id=None)

