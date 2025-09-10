from flask import Blueprint, jsonify

agent_x_bp = Blueprint('agent_x', __name__)

@agent_x_bp.route('/')
def index():
    return jsonify({'agent': 'AgentX', 'status': 'active', 'model': 'yi:6b'})