import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'sena_key_2026'

# --- CONFIGURACIÓN DE BASE DE DATOS ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', # Agrega tu contraseña si configuraste una en XAMPP/MariaDB
    'database': 'senalearn',
    'port': 5435
}

def get_db_connection():
    """Establece conexión con MariaDB con manejo de errores."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error crítico de conexión: {e}")
        return None

# --- FUNCIONES DE CONSULTA ---

def get_user_by_email(email):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    try:
        # Buscamos el correo de forma exacta
        cursor.execute("SELECT * FROM usuarios WHERE LOWER(email) = LOWER(%s)", (email.strip(),))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def get_aprendiz_full_data(user_id):
    """Trae la información de perfil, ficha y programa."""
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    try:
        # Los alias coinciden con tu HTML: user_info.ficha_numero y user_info.programa_nombre
        query = """
            SELECT u.nombre, f.numero AS ficha_numero, p.nombre AS programa_nombre
            FROM usuarios u
            LEFT JOIN aprendices a ON u.id = a.id
            LEFT JOIN fichas f ON a.ficha_id = f.id
            LEFT JOIN programas_formacion p ON f.programa_id = p.id
            WHERE u.id = %s
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# --- RUTAS DE AUTENTICACIÓN ---

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        rol_seleccionado = request.form.get("role", "")

        user = get_user_by_email(email)

        if user:
            # Validamos el hash generado previamente en la terminal
            if check_password_hash(user["password_hash"], password):
                # Validamos que el rol coincida
                if user["rol"].lower() == rol_seleccionado.lower():
                    session.clear()
                    session["user_id"] = user["id"]
                    session["nombre"] = user["nombre"]
                    session["rol"] = user["rol"]
                    
                    role_path = "aprendiz" if user["rol"].lower() == "aprendiz" else "admin"
                    return redirect(url_for("dashboard", role_slug=role_path))
                else:
                    flash("El perfil seleccionado no coincide con tu cuenta.", "warning")
            else:
                flash("Correo o contraseña incorrectos.", "danger")
        else:
            flash("El correo no está registrado.", "danger")
            
    return render_template("login.html")

# --- RUTAS DEL DASHBOARD Y MÓDULOS ---

@app.route("/dashboard/<role_slug>")
def dashboard(role_slug):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_info = get_aprendiz_full_data(session["user_id"])
    
    if role_slug == "aprendiz":
        # Renderiza templates/aprendiz/dashboard.html
        return render_template("aprendiz/dashboard.html", user_info=user_info)
    
    return render_template("dashboard.html", user_info=user_info)

@app.route("/aprendiz/fichas")
def aprendiz_fichas():
    if "user_id" not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    fichas = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT f.id, f.numero, p.nombre AS programa_nombre
            FROM aprendices a
            JOIN fichas f ON a.ficha_id = f.id
            JOIN programas_formacion p ON f.programa_id = p.id
            WHERE a.id = %s
        """, (session["user_id"],))
        fichas = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template("aprendiz/fichas.html", fichas=fichas)

@app.route("/aprendiz/fases")
def aprendiz_fases():
    if "user_id" not in session:
        return redirect(url_for('login'))

    ficha = get_aprendiz_full_data(session["user_id"])
    return render_template("aprendiz/fases.html", ficha=ficha)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)