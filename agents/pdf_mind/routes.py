from flask import Blueprint, jsonify

pdf_mind_bp = Blueprint('pdf_mind', __name__)

@pdf_mind_bp.route('/')
def index():
    return jsonify({'agent': 'PDFMind', 'status': 'active', 'model': 'qwen2.5:7b'})