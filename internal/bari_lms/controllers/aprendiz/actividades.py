"""Controlador aprendiz — Vistas de fases y actividades de aprendizaje/proyecto."""

from datetime import date as date_class

from flask import flash, redirect, render_template, request, url_for, current_app
from bari_lms.db import get_db
from bari_lms.middleware.auth import current_user, role_required
import os
import uuid
from werkzeug.utils import secure_filename

def register_routes(app):
    @app.route("/aprendiz/curso/<ficha_id>/fases")
    @role_required("Aprendiz")
    def aprendiz_fases(ficha_id):
        user = current_user()
        db = get_db()

        aprendiz = db.execute(
            "SELECT id, ficha FROM aprendiz WHERE persona_id = ?", (user["id"],)
        ).fetchone()

        ficha = db.execute(
            """
            SELECT f.id, f.numero, p.nombre AS programa_nombre, pf.nombre AS proyecto_nombre,
                   pf.codigo AS proyecto_codigo, pf.id AS proyecto_id, n.nombre AS nivel_nombre
            FROM ficha_formacion f
            JOIN programa_formacion p ON p.id = f.programa_formacion_id
            LEFT JOIN proyecto_formativo pf ON pf.id = f.proyecto_formativo_id
            LEFT JOIN nivel_formacion n ON n.id = p.nivel_formacion_id
            WHERE f.id = ?
            """,
            (ficha_id,),
        ).fetchone()

        if not ficha or not aprendiz or ficha["numero"] != aprendiz["ficha"]:
            flash("No tienes acceso a este curso.", "danger")
            return redirect(url_for("aprendiz_cursos"))

        proyecto_id = ficha["proyecto_id"]
        arbol = []
        cal_arbol = []
        resumen = {"total": 0, "aprobadas": 0, "pendientes": 0, "promedio": "—"}
        today = date_class.today()

        if proyecto_id:
            # Árbol: Competencia -> Fase -> Act Proyecto -> Act Aprendizaje
            rows = db.execute(
                """
                SELECT c.id AS comp_id, c.nombre AS comp_nombre,
                       fp.id AS fase_id, fp.nombre AS fase_nombre,
                       ap.id AS act_proy_id, ap.nombre AS act_proy_nombre,
                       aa.id AS act_apr_id, aa.nombre AS act_apr_nombre,
                       aa.descripcion AS act_apr_descripcion,
                       aa.fecha_fin AS act_apr_fecha_fin,
                       ga.url AS guia_url,
                       ea.id AS evidencia_id, ea.descripcion AS evidencia_descripcion,
                       ent.id AS entrega_id, ent.calificacion, ent.observaciones, ent.entregado_en
                FROM fase_proyecto fp
                JOIN actividad_proyecto ap ON ap.fase_proyecto_id = fp.id
                LEFT JOIN competencia c ON ap.competencia_id = c.id
                LEFT JOIN actividad_aprendizaje aa ON aa.actividad_proyecto_id = ap.id
                LEFT JOIN guia_aprendizaje ga ON ga.actividad_aprendizaje_id = aa.id
                LEFT JOIN evidencia_aprendizaje ea ON ea.actividad_aprendizaje_id = aa.id
                LEFT JOIN entrega_evidencia ent ON ent.evidencia_aprendizaje_id = ea.id AND ent.usuario_id = ?
                WHERE fp.proyecto_formativo_id = ?
                ORDER BY c.nombre ASC, fp.nombre ASC, ap.nombre ASC, aa.nombre ASC
                """,
                (user["id"], proyecto_id),
            ).fetchall()

            comp_dict = {}
            aa_dict = {}   # aa_id  -> aa entry dict (para adjuntar secciones después)
            ap_dict = {}   # ap_id  -> ap entry dict (para adjuntar guías después)

            for row in rows:
                cid = row["comp_id"] or "sin_competencia"
                cnombre = row["comp_nombre"] or "Competencia General"

                if cid not in comp_dict:
                    comp_dict[cid] = {
                        "id": cid, "nombre": cnombre, "fases": {}
                    }

                fid = row["fase_id"]
                if fid not in comp_dict[cid]["fases"]:
                    comp_dict[cid]["fases"][fid] = {
                        "id": fid, "nombre": row["fase_nombre"], "actividades_proyecto": {}
                    }

                apid = row["act_proy_id"]
                if apid:
                    if apid not in comp_dict[cid]["fases"][fid]["actividades_proyecto"]:
                        ap_entry = {
                            "id": apid,
                            "nombre": row["act_proy_nombre"],
                            "guias_concertado": [],
                            "guias_aprendizaje": [],
                            "actividades_aprendizaje": [],
                        }
                        comp_dict[cid]["fases"][fid]["actividades_proyecto"][apid] = ap_entry
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
                            "evidencia_descripcion": row["evidencia_descripcion"],
                            "entrega_id": row["entrega_id"],
                            "calificacion": row["calificacion"],
                            "observaciones": row["observaciones"],
                            "entregado_en": row["entregado_en"],
                            "secciones": [],
                        }
                        comp_dict[cid]["fases"][fid]["actividades_proyecto"][apid]["actividades_aprendizaje"].append(aa_entry)
                        aa_dict[aaid] = aa_entry

            # Cargar secciones y sub-secciones de todas las actividades_aprendizaje
            if aa_dict:
                aa_ids = list(aa_dict.keys())
                placeholders = ",".join(["?" for _ in aa_ids])
                secciones = db.execute(
                    f"SELECT id, actividad_aprendizaje_id, nombre, descripcion, "
                    f"archivo_url, archivo_tipo, fecha_fin "
                    f"FROM seccion_actividad "
                    f"WHERE actividad_aprendizaje_id IN ({placeholders}) ORDER BY orden",
                    aa_ids,
                ).fetchall()

                sec_dict = {}
                for sec in secciones:
                    sec_entry = {
                        "id": sec["id"],
                        "nombre": sec["nombre"],
                        "descripcion": sec["descripcion"],
                        "archivo_url": sec["archivo_url"],
                        "archivo_tipo": sec["archivo_tipo"],
                        "fecha_fin": sec["fecha_fin"],
                        "sub_secciones": [],
                    }
                    aa_dict[sec["actividad_aprendizaje_id"]]["secciones"].append(sec_entry)
                    sec_dict[sec["id"]] = sec_entry

                if sec_dict:
                    sec_ids = list(sec_dict.keys())
                    placeholders2 = ",".join(["?" for _ in sec_ids])
                    sub_secciones = db.execute(
                        f"SELECT id, seccion_id, nombre, descripcion, "
                        f"archivo_url, archivo_tipo, fecha_fin "
                        f"FROM sub_seccion_actividad "
                        f"WHERE seccion_id IN ({placeholders2}) ORDER BY orden",
                        sec_ids,
                    ).fetchall()
                    for sub in sub_secciones:
                        sec_dict[sub["seccion_id"]]["sub_secciones"].append({
                            "id": sub["id"],
                            "nombre": sub["nombre"],
                            "descripcion": sub["descripcion"],
                            "archivo_url": sub["archivo_url"],
                            "archivo_tipo": sub["archivo_tipo"],
                            "fecha_fin": sub["fecha_fin"],
                        })

            # Cargar guías de trabajo concertado y de actividades de aprendizaje
            if ap_dict:
                ap_ids = list(ap_dict.keys())
                placeholders_ap = ",".join(["?" for _ in ap_ids])
                guias_ap = db.execute(
                    f"SELECT id, actividad_proyecto_id, nombre, url, "
                    f"COALESCE(tipo, 'concertado') AS tipo "
                    f"FROM guia_actividad_proyecto "
                    f"WHERE actividad_proyecto_id IN ({placeholders_ap}) "
                    f"ORDER BY orden ASC, id ASC",
                    ap_ids,
                ).fetchall()
                for g in guias_ap:
                    entry = {"id": g["id"], "nombre": g["nombre"], "url": g["url"]}
                    if g["tipo"] == "aprendizaje":
                        ap_dict[g["actividad_proyecto_id"]]["guias_aprendizaje"].append(entry)
                    else:
                        ap_dict[g["actividad_proyecto_id"]]["guias_concertado"].append(entry)

            for comp in comp_dict.values():
                for fase in comp["fases"].values():
                    fase["actividades_proyecto"] = list(fase["actividades_proyecto"].values())
                comp["fases"] = list(comp["fases"].values())
                arbol.append(comp)

            # ── Calificaciones del aprendiz (mismo proyecto, solo su usuario) ──
            cal_rows = db.execute(
                """
                SELECT fp.id   AS fase_id,   fp.nombre AS fase_nombre,
                       ap.id   AS ap_id,     ap.nombre AS ap_nombre,
                       aa.id   AS aa_id,     aa.nombre AS aa_nombre,
                       aa.fecha_fin          AS aa_fecha_fin,
                       ent.id  AS entrega_id,
                       ent.url AS entrega_url,
                       ent.calificacion, ent.observaciones,
                       ent.retroalimentacion, ent.aprueba,
                       ent.entregado_en, ent.calificado_en
                FROM fase_proyecto fp
                JOIN actividad_proyecto ap ON ap.fase_proyecto_id = fp.id
                JOIN actividad_aprendizaje aa ON aa.actividad_proyecto_id = ap.id
                LEFT JOIN evidencia_aprendizaje ea ON ea.actividad_aprendizaje_id = aa.id
                LEFT JOIN entrega_evidencia ent
                       ON ent.evidencia_aprendizaje_id = ea.id AND ent.usuario_id = ?
                WHERE fp.proyecto_formativo_id = ?
                ORDER BY fp.nombre ASC, ap.nombre ASC, aa.nombre ASC
                """,
                (user["id"], proyecto_id),
            ).fetchall()

            cal_fases = {}
            for r in cal_rows:
                fid = r["fase_id"]
                if fid not in cal_fases:
                    cal_fases[fid] = {"id": fid, "nombre": r["fase_nombre"], "actividades_proyecto": {}}
                apid = r["ap_id"]
                if apid not in cal_fases[fid]["actividades_proyecto"]:
                    cal_fases[fid]["actividades_proyecto"][apid] = {"id": apid, "nombre": r["ap_nombre"], "actividades_aprendizaje": []}
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
            user=user, ficha=ficha, arbol=arbol,
            cal_arbol=cal_arbol, resumen=resumen,
            today=today,
        )

    @app.route("/aprendiz/entregar-evidencia", methods=["POST"])
    @role_required("Aprendiz")
    def entregar_evidencia():
        user = current_user()
        db = get_db()

        evidencia_id = request.form.get("evidencia_id")
        comentario = request.form.get("comentario")
        url_evidencia = request.form.get("url_evidencia")
        archivo = request.files.get("archivo")

        if not evidencia_id:
            flash("ID de evidencia no proporcionado.", "danger")
            return redirect(request.referrer or url_for("aprendiz_cursos"))

        # Verificar fecha límite de la actividad
        aa_row = db.execute(
            """
            SELECT aa.fecha_fin
            FROM actividad_aprendizaje aa
            JOIN evidencia_aprendizaje ea ON ea.actividad_aprendizaje_id = aa.id
            WHERE ea.id = ?
            """,
            (evidencia_id,),
        ).fetchone()

        if aa_row and aa_row["fecha_fin"]:
            if date_class.today() > aa_row["fecha_fin"]:
                flash("La fecha límite para entregar esta evidencia ya venció.", "danger")
                return redirect(request.referrer or url_for("aprendiz_cursos"))

        final_url = None

        if archivo and archivo.filename:
            filename = secure_filename(archivo.filename)
            upload_folder = os.path.join(current_app.root_path, "static", "uploads", "evidencias")
            os.makedirs(upload_folder, exist_ok=True)

            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(upload_folder, unique_filename)
            try:
                archivo.save(file_path)
                final_url = f"/static/uploads/evidencias/{unique_filename}"
            except Exception as e:
                flash(f"Error al subir el archivo: {str(e)}", "danger")
                return redirect(request.referrer or url_for("aprendiz_cursos"))
        elif url_evidencia:
            final_url = url_evidencia

        if not final_url:
            flash("Debes adjuntar un archivo o enviar un enlace válido.", "warning")
            return redirect(request.referrer or url_for("aprendiz_cursos"))

        try:
            existente = db.execute(
                "SELECT id FROM entrega_evidencia WHERE evidencia_aprendizaje_id = ? AND usuario_id = ?",
                (evidencia_id, user["id"])
            ).fetchone()

            if existente:
                db.execute(
                    """
                    UPDATE entrega_evidencia
                    SET url = ?, observaciones = ?, entregado_en = NOW()
                    WHERE id = ?
                    """,
                    (final_url, comentario, existente["id"])
                )
                flash("Evidencia actualizada correctamente.", "success")
            else:
                new_id = str(uuid.uuid4())
                db.execute(
                    """
                    INSERT INTO entrega_evidencia (id, evidencia_aprendizaje_id, usuario_id, url, observaciones, creado_por)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (new_id, evidencia_id, user["id"], final_url, comentario, user["id"])
                )
                flash("Evidencia entregada correctamente.", "success")

            db.commit()
        except Exception as e:
            db.rollback()
            flash(f"Error al guardar la evidencia: {str(e)}", "danger")

        return redirect(request.referrer or url_for("aprendiz_cursos"))
