# Insurance Query System

A full-stack AI-powered insurance document analysis and query processing system built with Flask (Python) and React (JavaScript).

## Features

- **User Authentication**: Secure user registration and login system
- **Document Management**: Upload and manage PDF/DOCX insurance documents
- **AI-Powered Analysis**: Advanced NLP processing using spaCy and LangChain
- **Smart Query Processing**: Natural language queries with instant responses
- **Vector Search**: FAISS-based document retrieval system
- **Modern UI**: Responsive React frontend with Tailwind CSS

## System Architecture

```
Frontend (React) ←→ Backend (Flask) ←→ AI Models (spaCy, LangChain, FAISS)
                ↑                    ↑
            Authentication      Document Processing
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- spaCy English model

## Installation

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Download spaCy English model
python -m spacy download en_core_web_sm

# Set environment variables
export SECRET_KEY="your-secret-key-here"
export FLASK_ENV=development

# Run the Flask backend
python app.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

### 1. User Registration/Login
- Navigate to the application
- Register a new account or login with existing credentials
- JWT tokens are automatically managed for authenticated requests

### 2. Document Upload
- Go to the Documents page
- Drag and drop or click to upload PDF/DOCX files
- Supported formats: PDF, DOCX (max 16MB)
- Files are securely stored and processed

### 3. Build Search Index
- After uploading documents, click "Build Index"
- This processes your documents and creates a searchable vector index
- Once complete, documents are marked as "Processed"

### 4. Query Processing
- Navigate to the Query page
- Enter natural language queries about insurance policies
- Example: "A 45-year-old male from Mumbai needs knee surgery with a 2-year policy"
- Get instant AI-powered responses with:
  - Parsed information (age, gender, procedure, location, policy duration)
  - Decision (approved/rejected with justification)
  - Relevant policy clauses from your documents

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User authentication

### Documents
- `POST /upload` - File upload (requires authentication)
- `GET /documents` - List user documents (requires authentication)
- `POST /build_index` - Build search index (requires authentication)

### Queries
- `POST /process_query` - Process insurance queries (requires authentication)

## Technical Details

### Backend Technologies
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Bcrypt**: Password hashing
- **JWT**: Token-based authentication
- **spaCy**: Natural language processing
- **LangChain**: AI/ML framework
- **FAISS**: Vector similarity search
- **SQLite**: Database (can be changed to PostgreSQL/MySQL)

### Frontend Technologies
- **React 18**: UI framework
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Dropzone**: File upload component
- **React Hot Toast**: Notifications

### AI/ML Components
- **Document Processing**: PDF/DOCX parsing and text extraction
- **Text Chunking**: Recursive character splitting for optimal processing
- **Embeddings**: Sentence transformers for vector representation
- **Query Parsing**: Regex-based information extraction
- **Decision Logic**: Rule-based insurance policy evaluation
- **Vector Search**: Semantic similarity search across documents

## File Structure

```
├── app.py                 # Flask backend application
├── main.py               # Core insurance query logic
├── requirements.txt      # Python dependencies
├── frontend/            # React frontend application
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API service functions
│   │   ├── contexts/    # React contexts (auth)
│   │   ├── App.js       # Main application component
│   │   └── index.js     # Application entry point
│   ├── public/          # Static assets
│   └── package.json     # Node.js dependencies
├── uploads/             # File upload directory
└── faiss_index/         # Vector search index
```

## Security Features

- **Password Hashing**: Bcrypt-based password security
- **JWT Authentication**: Secure token-based authentication
- **File Validation**: File type and size restrictions
- **SQL Injection Protection**: SQLAlchemy ORM protection
- **CORS Configuration**: Controlled cross-origin requests

## Performance Features

- **Vector Indexing**: Fast semantic search with FAISS
- **Document Chunking**: Optimal text processing for large documents
- **Lazy Loading**: Efficient document retrieval
- **Caching**: JWT token caching and validation

## Customization

### Adding New Insurance Procedures
Edit the `known_procedures` list in `main.py`:

```python
known_procedures = [
    "knee surgery", "back surgery", "eye surgery", "heart surgery",
    "brain surgery", "neck surgery", "shoulder surgery", "hip replacement",
    "bypass surgery", "dental treatment", "appendix removal", 
    "chemotherapy", "dialysis", "your_new_procedure"  # Add here
]
```

### Adding New Locations
Edit the `known_locations` list in `main.py`:

```python
known_locations = [
    "pune", "delhi", "kolkata", "mumbai", "chennai", "bangalore", 
    "hyderabad", "lucknow", "ahmedabad", "jaipur", "your_city"  # Add here
]
```

### Modifying Decision Logic
Edit the `evaluate_decision` function in `main.py` to implement your specific insurance policy rules.

## Troubleshooting

### Common Issues

1. **spaCy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **FAISS Index Issues**
   - Delete the `faiss_index` directory and rebuild
   - Ensure documents are uploaded before building index

3. **File Upload Errors**
   - Check file size (max 16MB)
   - Ensure file format is PDF or DOCX
   - Verify upload directory permissions

4. **Authentication Issues**
   - Clear browser localStorage
   - Check JWT token expiration
   - Verify backend secret key

### Development Mode

For development, both backend and frontend support hot reloading:

```bash
# Backend (Flask)
export FLASK_ENV=development
python app.py

# Frontend (React)
npm start
```

## Deployment

### Production Considerations

1. **Environment Variables**
   - Set strong `SECRET_KEY`
   - Configure production database
   - Set `FLASK_ENV=production`

2. **Database**
   - Use PostgreSQL or MySQL for production
   - Implement database migrations
   - Regular backups

3. **File Storage**
   - Use cloud storage (AWS S3, Google Cloud Storage)
   - Implement CDN for better performance

4. **Security**
   - HTTPS enforcement
   - Rate limiting
   - Input validation
   - Regular security updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the troubleshooting section
- Review the code comments
- Open an issue on GitHub

## Roadmap

- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Batch document processing
- [ ] API rate limiting
- [ ] User roles and permissions
- [ ] Document versioning
- [ ] Export functionality
- [ ] Mobile app




