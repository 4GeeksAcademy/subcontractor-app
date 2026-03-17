from flask import Blueprint, request
from ..controllers.job_controller import JobController
from ..middleware.auth_middleware import jwt_required

# Create Blueprint
jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

# Initialize controller
job_controller = JobController()

# Job CRUD routes
@jobs_bp.route('', methods=['GET'])
@jwt_required()
def get_all_jobs():
    """Get all jobs with optional filtering"""
    return job_controller.get_all_jobs()

@jobs_bp.route('', methods=['POST'])
@jwt_required()
def create_job():
    """Create a new job"""
    return job_controller.create_job()

@jobs_bp.route('/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Get a specific job by ID"""
    return job_controller.get_job(job_id)

@jobs_bp.route('/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """Update an existing job"""
    return job_controller.update_job(job_id)

@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """Delete a job"""
    return job_controller.delete_job(job_id)

@jobs_bp.route('/<int:job_id>/status', methods=['PATCH'])
@jwt_required()
def update_job_status(job_id):
    """Update job status"""
    return job_controller.update_job_status(job_id)

# Job statistics and utilities
@jobs_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_job_stats():
    """Get job statistics for the provider"""
    return job_controller.get_job_stats()

@jobs_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_job_categories():
    """Get available job categories"""
    return job_controller.get_job_categories()

# Document management
@jobs_bp.route('/<int:job_id>/documents', methods=['POST'])
@jwt_required()
def upload_document(job_id):
    """Upload document for a job"""
    return job_controller.upload_document(job_id)

@jobs_bp.route('/<int:job_id>/documents', methods=['GET'])
@jwt_required()
def get_documents(job_id):
    """Get documents for a job"""
    return job_controller.get_documents(job_id)

@jobs_bp.route('/<int:job_id>/documents/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(job_id, document_id):
    """Delete a job document"""
    return job_controller.delete_document(job_id, document_id)

# Worker management
@jobs_bp.route('/<int:job_id>/workers', methods=['POST'])
@jwt_required()
def assign_worker(job_id):
    """Assign worker to job"""
    return job_controller.assign_worker(job_id)

@jobs_bp.route('/<int:job_id>/workers/<int:worker_id>', methods=['DELETE'])
@jwt_required()
def remove_worker(job_id, worker_id):
    """Remove worker from job"""
    return job_controller.remove_worker(job_id, worker_id)

# Timeline
@jobs_bp.route('/<int:job_id>/timeline', methods=['GET'])
@jwt_required()
def get_timeline(job_id):
    """Get job timeline"""
    return job_controller.get_timeline(job_id)
