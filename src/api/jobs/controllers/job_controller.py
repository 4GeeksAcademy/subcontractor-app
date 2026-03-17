from flask import request, jsonify, current_app
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from ..models import Job, JobDocument, JobWorker, JobTimeline
from ..services.job_service import JobService
from ..utils.job_validation import validate_job_data
from ....models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

class JobController:
    def __init__(self):
        self.job_service = JobService()

    @jwt_required()
    def get_all_jobs(self):
        """Get all jobs with optional filtering"""
        try:
            provider_id = get_jwt_identity()
            
            # Get query parameters
            status = request.args.get('status', 'all')
            category = request.args.get('category', 'all')
            priority = request.args.get('priority', 'all')
            date_range = request.args.get('dateRange', 'all')
            search = request.args.get('search', '')
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 20)), 100)
            
            # Build query
            query = Job.query.filter_by(provider_id=provider_id)
            
            # Apply filters
            if status != 'all':
                query = query.filter(Job.status == status)
            
            if priority != 'all':
                query = query.filter(Job.priority == priority)
            
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    Job.title.ilike(search_term) |
                    Job.description.ilike(search_term) |
                    Job.location.ilike(search_term)
                )
            
            # Date range filter
            if date_range != 'all':
                today = datetime.utcnow().date()
                if date_range == 'today':
                    query = query.filter(Job.start_date >= today)
                elif date_range == 'week':
                    from datetime import timedelta
                    week_start = today - timedelta(days=today.weekday())
                    query = query.filter(Job.start_date >= week_start)
                elif date_range == 'month':
                    month_start = today.replace(day=1)
                    query = query.filter(Job.start_date >= month_start)
                elif date_range == 'quarter':
                    quarter_start = today.replace(month=((today.month - 1) // 3) * 3 + 1, day=1)
                    query = query.filter(Job.start_date >= quarter_start)
                elif date_range == 'year':
                    year_start = today.replace(month=1, day=1)
                    query = query.filter(Job.start_date >= year_start)
            
            # Category filter
            if category != 'all':
                query = query.filter(Job.categories.contains([category]))
            
            # Order by created_at desc
            query = query.order_by(Job.created_at.desc())
            
            # Paginate
            jobs = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return jsonify({
                'jobs': [job.to_dict() for job in jobs.items],
                'pagination': {
                    'page': jobs.page,
                    'per_page': jobs.per_page,
                    'total': jobs.total,
                    'pages': jobs.pages,
                    'has_next': jobs.has_next,
                    'has_prev': jobs.has_prev
                }
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Error fetching jobs: {str(e)}")
            return jsonify({'error': 'Failed to fetch jobs'}), 500

    @jwt_required()
    def get_job(self, job_id):
        """Get a specific job by ID"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            return jsonify(job.to_dict()), 200
            
        except Exception as e:
            current_app.logger.error(f"Error fetching job {job_id}: {str(e)}")
            return jsonify({'error': 'Failed to fetch job'}), 500

    @jwt_required()
    def create_job(self):
        """Create a new job"""
        try:
            provider_id = get_jwt_identity()
            data = request.get_json()
            
            # Validate input data
            validation_errors = validate_job_data(data)
            if validation_errors:
                return jsonify({'errors': validation_errors}), 400
            
            # Create job
            job = self.job_service.create_job(data, provider_id)
            
            # Add timeline entry
            self.job_service.add_timeline_entry(
                job.id,
                'Job Created',
                f'New job "{job.title}" was created',
                'created',
                provider_id
            )
            
            return jsonify(job.to_dict()), 201
            
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.error(f"Integrity error creating job: {str(e)}")
            return jsonify({'error': 'Invalid customer or provider ID'}), 400
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating job: {str(e)}")
            return jsonify({'error': 'Failed to create job'}), 500

    @jwt_required()
    def update_job(self, job_id):
        """Update an existing job"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            data = request.get_json()
            
            # Validate input data
            validation_errors = validate_job_data(data, is_update=True)
            if validation_errors:
                return jsonify({'errors': validation_errors}), 400
            
            # Update job
            updated_job = self.job_service.update_job(job, data)
            
            # Add timeline entry
            self.job_service.add_timeline_entry(
                job.id,
                'Job Updated',
                f'Job "{job.title}" was updated',
                'updated',
                provider_id
            )
            
            return jsonify(updated_job.to_dict()), 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating job {job_id}: {str(e)}")
            return jsonify({'error': 'Failed to update job'}), 500

    @jwt_required()
    def delete_job(self, job_id):
        """Delete a job"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            # Check if job can be deleted (not in progress)
            if job.status == 'in_progress':
                return jsonify({'error': 'Cannot delete job that is in progress'}), 400
            
            # Delete job (cascade will handle related records)
            db.session.delete(job)
            db.session.commit()
            
            return jsonify({'message': 'Job deleted successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting job {job_id}: {str(e)}")
            return jsonify({'error': 'Failed to delete job'}), 500

    @jwt_required()
    def update_job_status(self, job_id):
        """Update job status"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            data = request.get_json()
            new_status = data.get('status')
            
            if not new_status:
                return jsonify({'error': 'Status is required'}), 400
            
            if not job.is_valid_status(new_status):
                return jsonify({'error': 'Invalid status'}), 400
            
            if not job.can_change_status(new_status):
                return jsonify({'error': f'Cannot change status from {job.status} to {new_status}'}), 400
            
            # Update status
            old_status = job.status
            job.status = new_status
            job.updated_at = datetime.utcnow()
            
            # Update progress if completed
            if new_status == 'completed':
                job.progress = 100
            
            db.session.commit()
            
            # Add timeline entry
            self.job_service.add_timeline_entry(
                job.id,
                'Status Changed',
                f'Status changed from {old_status} to {new_status}',
                'status_changed',
                provider_id
            )
            
            return jsonify(job.to_dict()), 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating job status {job_id}: {str(e)}")
            return jsonify({'error': 'Failed to update job status'}), 500

    @jwt_required()
    def get_job_stats(self):
        """Get job statistics for the provider"""
        try:
            provider_id = get_jwt_identity()
            
            stats = self.job_service.get_job_stats(provider_id)
            
            return jsonify(stats), 200
            
        except Exception as e:
            current_app.logger.error(f"Error fetching job stats: {str(e)}")
            return jsonify({'error': 'Failed to fetch job statistics'}), 500

    @jwt_required()
    def get_job_categories(self):
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
            current_app.logger.error(f"Error fetching job categories: {str(e)}")
            return jsonify({'error': 'Failed to fetch job categories'}), 500

    @jwt_required()
    def upload_document(self, job_id):
        """Upload document for a job"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Upload file
            document = self.job_service.upload_document(job.id, file, provider_id)
            
            # Add timeline entry
            self.job_service.add_timeline_entry(
                job.id,
                'Document Uploaded',
                f'Document "{document.name}" was uploaded',
                'document_uploaded',
                provider_id
            )
            
            return jsonify(document.to_dict()), 201
            
        except Exception as e:
            current_app.logger.error(f"Error uploading document for job {job_id}: {str(e)}")
            return jsonify({'error': 'Failed to upload document'}), 500

    @jwt_required()
    def get_documents(self, job_id):
        """Get documents for a job"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            documents = JobDocument.query.filter_by(job_id=job_id).all()
            
            return jsonify([doc.to_dict() for doc in documents]), 200
            
        except Exception as e:
            current_app.logger.error(f"Error fetching documents for job {job_id}: {str(e)}")
            return jsonify({'error': 'Failed to fetch documents'}), 500

    @jwt_required()
    def delete_document(self, job_id, document_id):
        """Delete a job document"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            document = JobDocument.query.filter_by(id=document_id, job_id=job_id).first()
            if not document:
                return jsonify({'error': 'Document not found'}), 404
            
            # Delete file from storage
            self.job_service.delete_document_file(document.file_path)
            
            # Delete from database
            db.session.delete(document)
            db.session.commit()
            
            return jsonify({'message': 'Document deleted successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting document {document_id}: {str(e)}")
            return jsonify({'error': 'Failed to delete document'}), 500

    @jwt_required()
    def assign_worker(self, job_id):
        """Assign worker to job"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            data = request.get_json()
            worker_id = data.get('workerId')
            role = data.get('role', 'Worker')
            
            if not worker_id:
                return jsonify({'error': 'Worker ID is required'}), 400
            
            # Assign worker
            job_worker = self.job_service.assign_worker(job.id, worker_id, role)
            
            # Add timeline entry
            self.job_service.add_timeline_entry(
                job.id,
                'Worker Assigned',
                f'Worker assigned to job with role: {role}',
                'worker_assigned',
                provider_id
            )
            
            return jsonify(job_worker.to_dict()), 201
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error assigning worker to job {job_id}: {str(e)}")
            return jsonify({'error': 'Failed to assign worker'}), 500

    @jwt_required()
    def remove_worker(self, job_id, worker_id):
        """Remove worker from job"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            # Remove worker
            success = self.job_service.remove_worker(job.id, worker_id)
            
            if not success:
                return jsonify({'error': 'Worker assignment not found'}), 404
            
            return jsonify({'message': 'Worker removed successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error removing worker from job {job_id}: {str(e)}")
            return jsonify({'error': 'Failed to remove worker'}), 500

    @jwt_required()
    def get_timeline(self, job_id):
        """Get job timeline"""
        try:
            provider_id = get_jwt_identity()
            
            job = Job.query.filter_by(id=job_id, provider_id=provider_id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            timeline = JobTimeline.query.filter_by(job_id=job_id).order_by(JobTimeline.created_at.desc()).all()
            
            return jsonify([activity.to_dict() for activity in timeline]), 200
            
        except Exception as e:
            current_app.logger.error(f"Error fetching timeline for job {job_id}: {str(e)}")
            return jsonify({'error': 'Failed to fetch timeline'}), 500
