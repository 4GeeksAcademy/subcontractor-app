from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os

# Import models directly to avoid circular imports
from ...models import db, Job

# Create Blueprint
jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

# Job CRUD routes
@jobs_bp.route('', methods=['GET'])
@jwt_required()
def get_all_jobs():
    """Get all jobs with optional filtering"""
    try:
        provider_id = 1  # Hardcoded for testing - replace with get_jwt_identity()
        
        # Get query parameters
        status = request.args.get('status', 'all')
        category = request.args.get('category', 'all')
        priority = request.args.get('priority', 'all')
        date_range = request.args.get('dateRange', 'all')
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        
        # Build query
        query = Job.query.filter_by(contractor_id=provider_id)
        
        # Apply filters
        if status != 'all':
            query = query.filter(Job.status == status)
        
        if priority != 'all':
            query = query.filter(Job.estimate_total == float(priority))  # Using estimate_total as priority for testing
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                Job.title.ilike(search_term) |
                Job.description.ilike(search_term)
            )
        
        # Order by created_at desc
        query = query.order_by(Job.create_at.desc())
        
        # Get all jobs (simplified for testing)
        jobs = query.all()
        
        return jsonify({
            'jobs': [{
                'id': job.id,
                'title': job.title,
                'description': job.description,
                'status': job.status.value if job.status else 'pending',
                'priority': 'medium',
                'budget': float(job.estimate_total) if job.estimate_total else 1000,
                'startDate': job.create_at.isoformat() if job.create_at else None,
                'customerId': job.customer_id,
                'createdAt': job.create_at.isoformat() if job.create_at else None
            } for job in jobs],
            'total': len(jobs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch jobs: {str(e)}'}), 500

@jobs_bp.route('', methods=['POST'])
@jwt_required()
def create_job():
    """Create a new job"""
    try:
        data = request.get_json()
        
        # Create simple job for testing
        job = Job(
            contractor_id=1,  # Hardcoded for testing
            customer_id=data.get('customerId', 1),
            service_id=1,  # Hardcoded for testing
            title=data.get('title', 'Test Job'),
            description=data.get('description', 'Test Description'),
            status=JobStatus.pending,
            estimate_total=float(data.get('budget', 1000))
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'status': job.status.value,
            'budget': float(job.estimate_total),
            'customerId': job.customer_id,
            'createdAt': job.create_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create job: {str(e)}'}), 500

@jobs_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_job_categories():
    """Get available job categories"""
    try:
        categories = [
            {'value': 'residential', 'label': 'Residential'},
            {'value': 'commercial', 'label': 'Commercial'},
            {'value': 'industrial', 'label': 'Industrial'},
            {'value': 'renovation', 'label': 'Renovation'},
            {'value': 'new_construction', 'label': 'New Construction'},
            {'value': 'remodeling', 'label': 'Remodeling'},
            {'value': 'plumbing', 'label': 'Plumbing'},
            {'value': 'electrical', 'label': 'Electrical'},
            {'value': 'hvac', 'label': 'HVAC'},
            {'value': 'roofing', 'label': 'Roofing'},
            {'value': 'painting', 'label': 'Painting'},
            {'value': 'flooring', 'label': 'Flooring'},
            {'value': 'landscaping', 'label': 'Landscaping'},
            {'value': 'concrete', 'label': 'Concrete'},
            {'value': 'carpentry', 'label': 'Carpentry'}
        ]
        
        return jsonify(categories), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch categories: {str(e)}'}), 500

@jobs_bp.route('/test', methods=['GET'])
def test_jobs():
    """Test endpoint to verify jobs routes are working"""
    return jsonify({
        'message': 'Jobs routes are working!',
        'endpoints': [
            'GET /api/jobs',
            'POST /api/jobs',
            'GET /api/jobs/categories'
        ]
    }), 200
