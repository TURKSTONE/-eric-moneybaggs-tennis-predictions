import os
from flask import Flask, send_from_directory, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

# Tennis Prediction Model (example)
class TennisPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.String(100), nullable=False)
    player2 = db.Column(db.String(100), nullable=False)
    predicted_winner = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'player1': self.player1,
            'player2': self.player2,
            'predicted_winner': self.predicted_winner,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat()
        }

# User Routes Blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Username and email are required'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    
    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_email:
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# Tennis Predictions Routes Blueprint
tennis_bp = Blueprint('tennis', __name__)

@tennis_bp.route('/predictions', methods=['GET'])
def get_predictions():
    predictions = TennisPrediction.query.all()
    return jsonify([prediction.to_dict() for prediction in predictions])

@tennis_bp.route('/predictions', methods=['POST'])
def create_prediction():
    data = request.get_json()
    
    required_fields = ['player1', 'player2', 'predicted_winner', 'confidence']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required: player1, player2, predicted_winner, confidence'}), 400
    
    prediction = TennisPrediction(
        player1=data['player1'],
        player2=data['player2'],
        predicted_winner=data['predicted_winner'],
        confidence=float(data['confidence'])
    )
    db.session.add(prediction)
    db.session.commit()
    
    return jsonify(prediction.to_dict()), 201

@tennis_bp.route('/predictions/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    prediction = TennisPrediction.query.get_or_404(prediction_id)
    return jsonify(prediction.to_dict())

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(tennis_bp, url_prefix='/api/tennis')

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Flask app is running successfully'})

# API info endpoint
@app.route('/api')
def api_info():
    return jsonify({
        'message': 'Flask API is running',
        'endpoints': {
            'users': '/api/users',
            'tennis_predictions': '/api/tennis/predictions',
            'health': '/health'
        }
    })

# Static file serving (for frontend)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return jsonify({'message': 'Welcome to Flask API', 'api_endpoint': '/api'}), 200

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            # If no static files, return API info
            return jsonify({'message': 'Welcome to Flask API', 'api_endpoint': '/api'}), 200

# Initialize database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    print("Starting Flask application...")
    print("Available endpoints:")
    print("- GET /health - Health check")
    print("- GET /api - API information")
    print("- GET /api/users - Get all users")
    print("- POST /api/users - Create new user")
    print("- GET /api/tennis/predictions - Get all predictions")
    print("- POST /api/tennis/predictions - Create new prediction")
    
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)

