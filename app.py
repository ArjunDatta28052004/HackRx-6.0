import os
import jwt
import datetime
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.utils import secure_filename
from main import process_insurance_query, load_documents, split_documents, embed_documents
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///insurance_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt_manager = JWTManager(app)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    documents = db.relationship('Document', backref='user', lazy=True)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    processed = db.Column(db.Boolean, default=False)

# Create database tables
with app.app_context():
    db.create_all()

# JWT token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Invalid token!'}), 401
        except:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Routes
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Insurance Query API is running"}), 200

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Hash password and create user
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            token = jwt.encode(
                {'user_id': user.id, 'username': user.username},
                app.config['SECRET_KEY'],
                algorithm="HS256"
            )
            return jsonify({
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/upload", methods=["POST"])
@token_required
def upload_file(current_user):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            # Generate unique filename
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            if file_extension not in ['pdf', 'docx']:
                return jsonify({'error': 'Only PDF and DOCX files are allowed'}), 400
            
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Save document info to database
            new_document = Document(
                filename=unique_filename,
                original_filename=filename,
                file_path=file_path,
                file_type=file_extension,
                user_id=current_user.id
            )
            db.session.add(new_document)
            db.session.commit()
            
            return jsonify({
                'message': 'File uploaded successfully',
                'document_id': new_document.id,
                'filename': filename
            }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/documents", methods=["GET"])
@token_required
def get_documents(current_user):
    try:
        documents = Document.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'documents': [{
                'id': doc.id,
                'filename': doc.original_filename,
                'file_type': doc.file_type,
                'uploaded_at': doc.uploaded_at.isoformat(),
                'processed': doc.processed
            } for doc in documents]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/process_query", methods=["POST"])
@token_required
def process_query(current_user):
    try:
        data = request.get_json()
        user_text = data.get("query", "")
        
        if not user_text:
            return jsonify({'error': 'Query is required'}), 400
        
        result = process_insurance_query(user_text)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/build_index", methods=["POST"])
@token_required
def build_index(current_user):
    try:
        # Get user's documents
        user_documents = Document.query.filter_by(user_id=current_user.id).all()
        
        if not user_documents:
            return jsonify({'error': 'No documents found'}), 400
        
        # Load and process documents
        file_paths = [doc.file_path for doc in user_documents]
        documents = load_documents(file_paths)
        
        if not documents:
            return jsonify({'error': 'No valid documents found'}), 400
        
        # Split documents
        split_docs = split_documents(documents)
        
        # Create embeddings and save to FAISS
        embeddings, _ = embed_documents(split_docs)
        
        # Save FAISS index
        from langchain_community.vectorstores import FAISS
        vectorstore = FAISS.from_documents(split_docs, embeddings)
        vectorstore.save_local("faiss_index")
        
        # Mark documents as processed
        for doc in user_documents:
            doc.processed = True
        db.session.commit()
        
        return jsonify({'message': 'Index built successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
