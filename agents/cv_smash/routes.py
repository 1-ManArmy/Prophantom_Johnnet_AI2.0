from flask import Blueprint, jsonify

cv_smash_bp = Blueprint('cv_smash', __name__)

@cv_smash_bp.route('/')
def index():
    return jsonify({'agent': 'CVSmash', 'status': 'active', 'model': 'llava:7b'})