from flask import Blueprint, jsonify

chat_revive_bp = Blueprint('chat_revive', __name__)

@chat_revive_bp.route('/')
def index():
    return jsonify({'agent': 'ChatRevive', 'status': 'active', 'model': 'mistral:7b'})