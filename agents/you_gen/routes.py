from flask import Blueprint, jsonify

you_gen_bp = Blueprint('you_gen', __name__)

@you_gen_bp.route('/')
def index():
    return jsonify({'agent': 'YouGen', 'status': 'active', 'model': 'deepseek-coder:6.7b'})