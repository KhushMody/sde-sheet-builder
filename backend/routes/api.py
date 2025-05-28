from flask import Blueprint, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from ..services.question_service import analyze_question
from ..utils.decorators import login_required # Import the login decorator
from ..app import limiter # Import the limiter instance

api_bp = Blueprint('api', __name__, url_prefix='/api')
CORS(api_bp)

@api_bp.route('/analyze', methods=['POST'])
@limiter.limit("10 per hour;100 per day") # Apply rate limiting
@login_required # Apply the login decorator (after rate limiting)
def analyze_code():
    data = request.get_json()
    user_question = data.get("question", "")

    if not user_question:
        return jsonify({"error": "User question is required"}), 400
    
    result = analyze_question(user_question)

    return result


