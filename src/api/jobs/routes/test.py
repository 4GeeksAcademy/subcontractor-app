from flask import jsonify, Blueprint

# Create a test blueprint to verify routes are working
test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/jobs-routes', methods=['GET'])
def test_jobs_routes():
    """Test if jobs routes are registered"""
    return jsonify({
        'message': 'Jobs routes are working!',
        'endpoints': [
            'GET /api/jobs',
            'POST /api/jobs',
            'GET /api/jobs/<id>',
            'PUT /api/jobs/<id>',
            'DELETE /api/jobs/<id>',
            'PATCH /api/jobs/<id>/status',
            'GET /api/jobs/stats',
            'GET /api/jobs/categories'
        ]
    }), 200
