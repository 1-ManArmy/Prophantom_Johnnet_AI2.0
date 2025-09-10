from flask import Blueprint, jsonify

auto_chat_bp = Blueprint('auto_chat', __name__)

@auto_chat_bp.route('/')
def index():
    return jsonify({'agent': 'AutoChat', 'status': 'active', 'model': 'mathstral:7b'})