import os
import sqlite3
from datetime import timedelta
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from main import process_insurance_query
from build_index import build_and_save_index_for_dir

# -----------------------------
# App and Config
# -----------------------------
app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["UPLOAD_FOLDER_ROOT"] = os.path.join(os.getcwd(), "user_data")
app.config["DB_PATH"] = os.path.join(os.getcwd(), "users.db")
app.config["FRONTEND_DIR"] = os.path.join(os.getcwd(), "frontend")

ALLOWED_EXTENSIONS = {"pdf", "docx"}

jwt = JWTManager(app)

# -----------------------------
# Database Helpers
# -----------------------------

def get_db_connection():
    connection = sqlite3.connect(app.config["DB_PATH"]) 
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    os.makedirs(os.path.dirname(app.config["DB_PATH"]), exist_ok=True)
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
            """
        )
        conn.commit()


init_db()

# -----------------------------
# Utils
# -----------------------------

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_user_dirs(user_id: int):
    base_dir = os.path.join(app.config["UPLOAD_FOLDER_ROOT"], str(user_id))
    docs_dir = os.path.join(base_dir, "docs")
    index_dir = os.path.join(base_dir, "index")
    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(index_dir, exist_ok=True)
    return docs_dir, index_dir


# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.get("/ui")
def serve_ui():
    index_path = os.path.join(app.config["FRONTEND_DIR"], "index.html")
    if os.path.exists(index_path):
        return send_from_directory(app.config["FRONTEND_DIR"], "index.html")
    return jsonify({"message": "Frontend not found. Open frontend/index.html locally."}), 404


@app.post("/auth/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    password_hash = generate_password_hash(password)

    try:
        with get_db_connection() as conn:
            cur = conn.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, password_hash),
            )
            conn.commit()
            user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        return jsonify({"error": "email already registered"}), 409

    access_token = create_access_token(identity=user_id, additional_claims={"email": email})
    return jsonify({"access_token": access_token}), 201


@app.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    with get_db_connection() as conn:
        row = conn.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,)).fetchone()
        if not row:
            return jsonify({"error": "invalid credentials"}), 401
        user_id = row["id"]
        if not check_password_hash(row["password_hash"], password):
            return jsonify({"error": "invalid credentials"}), 401

    access_token = create_access_token(identity=user_id, additional_claims={"email": email})
    return jsonify({"access_token": access_token}), 200


@app.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    return jsonify({"user_id": user_id}), 200


@app.post("/documents/upload")
@jwt_required()
def upload_documents():
    user_id = get_jwt_identity()

    if len(request.files) == 0:
        return jsonify({"error": "No files provided. Use form field 'files'"}), 400

    docs_dir, index_dir = get_user_dirs(user_id)

    saved_files = []

    # Handle multiple files under the same field name 'files'
    if "files" in request.files:
        incoming_files = request.files.getlist("files")
        for file in incoming_files:
            if not file or file.filename == "":
                continue
            if not allowed_file(file.filename):
                return jsonify({"error": f"File type not allowed: {file.filename}"}), 400
            filename = secure_filename(file.filename)
            file_path = os.path.join(docs_dir, filename)
            file.save(file_path)
            saved_files.append(filename)

    # Handle any other individually named fields
    for key in request.files:
        if key == "files":
            continue
        file = request.files.get(key)
        if not file or file.filename == "":
            continue
        if not allowed_file(file.filename):
            return jsonify({"error": f"File type not allowed: {file.filename}"}), 400
        filename = secure_filename(file.filename)
        file_path = os.path.join(docs_dir, filename)
        file.save(file_path)
        saved_files.append(filename)

    if not saved_files:
        return jsonify({"error": "No valid files uploaded"}), 400

    # Build FAISS index for the user's documents
    built_dir = build_and_save_index_for_dir(docs_dir, index_dir)
    if built_dir is None:
        return jsonify({"error": "No valid documents found to index"}), 400

    return jsonify({"message": "Files uploaded and index built", "files": saved_files}), 201


@app.post("/query")
@jwt_required()
def query():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    user_text = data.get("query", "")
    if not user_text:
        return jsonify({"error": "query is required"}), 400

    _, index_dir = get_user_dirs(user_id)

    result = process_insurance_query(user_text, index_dir=index_dir)
    return jsonify(result), 200


# Backward-compatible endpoint name with auth
@app.post("/process_query")
@jwt_required()
def process_query():
    return query()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
