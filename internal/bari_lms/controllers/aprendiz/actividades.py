"""Controlador aprendiz — Fases, actividades y entrega de evidencias."""

import uuid
from datetime import date as date_class

from flask import flash, redirect, render_template, request, url_for

from bari_lms.db import get_db
from bari_lms.middleware.auth import current_user, role_required


def register_routes(app):

    @app.route("/aprendiz/curso/<ficha_id>/fases")
    @role_required("Aprendiz")
    def aprendiz_fases(ficha_id):
        user = current_user()
        db = get_db()

        # Verificar acceso a la ficha mediante ficha_aprendiz
        ficha = db.execute(
            """
            SELECT f.id, f.numero,
                   p.nombre  AS programa_nombre,
                   pf.nombre AS proyecto_nombre,
                   pf.codigo AS proyecto_codigo,
                   pf.id     AS proyecto_id,
                   n.nombre  AS nivel_nombre
            FROM ficha_formacion f
            JOIN programa_formacion p  ON p.id  = f.programa_formacion_id
            LEFT JOIN proyecto_formativo pf ON pf.id = f.proyecto_formativo_id
            LEFT JOIN nivel_formacion n     ON n.id  = p.nivel_formacion_id
            JOIN ficha_aprendiz fa ON fa.ficha_id = f.id
            JOIN aprendiz a        ON a.id        = fa.aprendiz_id
            WHERE f.id = ? AND a.persona_id = ?
            """,
            (ficha_id, user["id"]),
        ).fetchone()

        if not ficha:
            flash("No tienes acceso a este curso.", "danger")
            return redirect(url_for("aprendiz_cursos"))

        proyecto_id = ficha["proyecto_id"]
        arbol = []
        cal_arbol = []
        resumen = {"total": 0, "aprobadas": 0, "pendientes": 0, "promedio": "—"}
        today = date_class.today()

        if proyecto_id:
            # ── Árbol: Fase → Actividad Proyecto → Actividad Aprendizaje ──────
            rows = db.execute(
                """
                SELECT fp.id   AS fase_id,   fp.nombre AS fase_nombre,
                       ap.id   AS act_proy_id, ap.nombre AS act_proy_nombre,
                       aa.id   AS act_apr_id,  aa.nombre AS act_apr_nombre,
                       aa.descripcion           AS act_apr_descripcion,
                       aa.fecha_fin             AS act_apr_fecha_fin,
                       ga.url                   AS guia_url,
                       ea.id                    AS evidencia_id,
                       ea.descripcion           AS evidencia_descripcion,
                       ent.id                   AS entrega_id,
                       ent.url                  AS entrega_url,
                       ent.calificacion,
                       ent.observaciones,
                       ent.retroalimentacion,
                       ent.aprueba,
                       ent.entregado_en
                FROM fase_proyecto fp
                JOIN actividad_proyecto ap ON ap.fase_proyecto_id = fp.id
                LEFT JOIN actividad_aprendizaje aa ON aa.actividad_proyecto_id = ap.id
                LEFT JOIN guia_aprendizaje ga ON ga.actividad_aprendizaje_id = aa.id
                LEFT JOIN evidencia_aprendizaje ea ON ea.actividad_aprendizaje_id = aa.id
                LEFT JOIN entrega_evidencia ent
                       ON ent.evidencia_aprendizaje_id = ea.id AND ent.usuario_id = ?
                WHERE fp.proyecto_formativo_id = ?
                ORDER BY fp.id ASC, ap.id ASC, aa.orden ASC, aa.id ASC
                """,
                (user["id"], proyecto_id),
            ).fetchall()

            fase_dict = {}
            ap_dict = {}
            aa_dict = {}

            for row in rows:
                fid = row["fase_id"]
                if fid not in fase_dict:
                    fase_dict[fid] = {
                        "id": fid,
                        "nombre": row["fase_nombre"],
                        "actividades_proyecto": {},
                    }

                apid = row["act_proy_id"]
                if apid and apid not in fase_dict[fid]["actividades_proyecto"]:
                    ap_entry = {
                        "id": apid,
                        "nombre": row["act_proy_nombre"],
                        "guias_concertado": [],
                        "actividades_aprendizaje": [],
                    }
                    fase_dict[fid]["actividades_proyecto"][apid] = ap_entry
                    ap_dict[apid] = ap_entry

                aaid = row["act_apr_id"]
                if aaid and aaid not in aa_dict:
                    aa_entry = {
                        "id": aaid,
                        "nombre": row["act_apr_nombre"],
                        "descripcion": row["act_apr_descripcion"],
                        "fecha_fin": row["act_apr_fecha_fin"],
                        "guia_url": row["guia_url"],
                        "evidencia_id": row["evidencia_id"],
                        "entrega_id": row["entrega_id"],
                        "entrega_url": row["entrega_url"],
                        "calificacion": row["calificacion"],
                        "observaciones": row["observaciones"],
                        "retroalimentacion": row["retroalimentacion"],
                        "aprueba": row["aprueba"],
                        "entregado_en": row["entregado_en"],
                    }
                    if apid:
                        fase_dict[fid]["actividades_proyecto"][apid]["actividades_aprendizaje"].append(aa_entry)
                    aa_dict[aaid] = aa_entry

            # Cargar guías de trabajo concertado
            if ap_dict:
                ap_ids = list(ap_dict.keys())
                placeholders = ",".join(["?" for _ in ap_ids])
                guias = db.execute(
                    f"SELECT actividad_proyecto_id, nombre, url "
                    f"FROM guia_actividad_proyecto "
                    f"WHERE actividad_proyecto_id IN ({placeholders}) "
                    f"ORDER BY orden ASC, id ASC",
                    ap_ids,
                ).fetchall()
                for g in guias:
                    ap_dict[g["actividad_proyecto_id"]]["guias_concertado"].append({
                        "nombre": g["nombre"],
                        "url": g["url"],
                    })

            for fase in fase_dict.values():
                fase["actividades_proyecto"] = list(fase["actividades_proyecto"].values())
                arbol.append(fase)

            # ── Calificaciones (mismo proyecto, solo el aprendiz) ─────────────
            cal_rows = db.execute(
                """
                SELECT fp.id   AS fase_id,   fp.nombre AS fase_nombre,
                       ap.id   AS ap_id,     ap.nombre AS ap_nombre,
                       aa.id   AS aa_id,     aa.nombre AS aa_nombre,
                       aa.fecha_fin          AS aa_fecha_fin,
                       ent.id                AS entrega_id,
                       ent.url               AS entrega_url,
                       ent.calificacion,
                       ent.observaciones,
                       ent.retroalimentacion,
                       ent.aprueba,
                       ent.entregado_en,
                       ent.calificado_en
                FROM fase_proyecto fp
                JOIN actividad_proyecto ap ON ap.fase_proyecto_id = fp.id
                JOIN actividad_aprendizaje aa ON aa.actividad_proyecto_id = ap.id
                LEFT JOIN evidencia_aprendizaje ea ON ea.actividad_aprendizaje_id = aa.id
                LEFT JOIN entrega_evidencia ent
                       ON ent.evidencia_aprendizaje_id = ea.id AND ent.usuario_id = ?
                WHERE fp.proyecto_formativo_id = ?
                ORDER BY fp.id ASC, ap.id ASC, aa.orden ASC, aa.id ASC
                """,
                (user["id"], proyecto_id),
            ).fetchall()

            cal_fases = {}
            for r in cal_rows:
                fid = r["fase_id"]
                if fid not in cal_fases:
                    cal_fases[fid] = {
                        "id": fid,
                        "nombre": r["fase_nombre"],
                        "actividades_proyecto": {},
                    }
                apid = r["ap_id"]
                if apid not in cal_fases[fid]["actividades_proyecto"]:
                    cal_fases[fid]["actividades_proyecto"][apid] = {
                        "id": apid,
                        "nombre": r["ap_nombre"],
                        "actividades_aprendizaje": [],
                    }
                cal_fases[fid]["actividades_proyecto"][apid]["actividades_aprendizaje"].append({
                    "id": str(r["aa_id"]),
                    "nombre": r["aa_nombre"],
                    "fecha_fin": r["aa_fecha_fin"].isoformat() if r["aa_fecha_fin"] else None,
                    "entrega_id": str(r["entrega_id"]) if r["entrega_id"] else None,
                    "entrega_url": r["entrega_url"],
                    "calificacion": float(r["calificacion"]) if r["calificacion"] is not None else None,
                    "observaciones": r["observaciones"],
                    "retroalimentacion": r["retroalimentacion"],
                    "aprueba": bool(r["aprueba"]) if r["aprueba"] is not None else None,
                    "entregado_en": r["entregado_en"].isoformat() if r["entregado_en"] else None,
                    "calificado_en": r["calificado_en"].isoformat() if r["calificado_en"] else None,
                })

            for f in cal_fases.values():
                f["actividades_proyecto"] = list(f["actividades_proyecto"].values())
            cal_arbol = list(cal_fases.values())

            entregas = [r for r in cal_rows if r["entrega_id"]]
            cals_num = [r["calificacion"] for r in entregas if r["calificacion"] is not None]
            resumen = {
                "total": len(entregas),
                "aprobadas": sum(1 for r in entregas if r["aprueba"]),
                "pendientes": sum(1 for r in entregas if r["calificacion"] is None),
                "promedio": f"{sum(cals_num)/len(cals_num):.1f}" if cals_num else "—",
            }

        return render_template(
            "aprendiz/fases.html",
            user=user,
            ficha=ficha,
            arbol=arbol,
            cal_arbol=cal_arbol,
            resumen=resumen,
            today=today,
            notificaciones=[],
        )

    @app.route("/aprendiz/entregar-evidencia", methods=["POST"])
    @role_required("Aprendiz")
    def entregar_evidencia():
        user = current_user()
        db = get_db()

        evidencia_id = request.form.get("evidencia_id")
        url_evidencia = request.form.get("url_evidencia", "").strip()
        comentario = request.form.get("comentario", "").strip()

        if not evidencia_id:
            flash("ID de evidencia no proporcionado.", "danger")
            return redirect(request.referrer or url_for("aprendiz_cursos"))

        if not url_evidencia:
            flash("Debes ingresar un enlace válido.", "warning")
            return redirect(request.referrer or url_for("aprendiz_cursos"))

        # Verificar fecha límite
        aa_row = db.execute(
            """
            SELECT aa.fecha_fin
            FROM actividad_aprendizaje aa
            JOIN evidencia_aprendizaje ea ON ea.actividad_aprendizaje_id = aa.id
            WHERE ea.id = ?
            """,
            (evidencia_id,),
        ).fetchone()

        if aa_row and aa_row["fecha_fin"] and date_class.today() > aa_row["fecha_fin"]:
            flash("La fecha límite para entregar esta evidencia ya venció.", "danger")
            return redirect(request.referrer or url_for("aprendiz_cursos"))

        try:
            existente = db.execute(
                "SELECT id FROM entrega_evidencia WHERE evidencia_aprendizaje_id = ? AND usuario_id = ?",
                (evidencia_id, user["id"]),
            ).fetchone()

            if existente:
                db.execute(
                    """
                    UPDATE entrega_evidencia
                    SET url = ?, observaciones = ?, entregado_en = NOW()
                    WHERE id = ?
                    """,
                    (url_evidencia, comentario or None, existente["id"]),
                )
                flash("Evidencia actualizada correctamente.", "success")
            else:
                db.execute(
                    """
                    INSERT INTO entrega_evidencia
                        (id, evidencia_aprendizaje_id, usuario_id, url, observaciones, creado_por)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (str(uuid.uuid4()), evidencia_id, user["id"],
                     url_evidencia, comentario or None, user["id"]),
                )
                flash("Evidencia entregada correctamente.", "success")

            db.commit()
        except Exception as e:
            db.rollback()
            flash(f"Error al guardar la evidencia: {str(e)}", "danger")

        return redirect(request.referrer or url_for("aprendiz_cursos"))
