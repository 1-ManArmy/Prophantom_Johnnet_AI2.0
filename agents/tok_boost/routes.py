from flask import Blueprint, jsonify

tok_boost_bp = Blueprint('tok_boost', __name__)

@tok_boost_bp.route('/')
def index():
    return jsonify({'agent': 'TokBoost', 'status': 'active', 'model': 'llama3.2:3b'})