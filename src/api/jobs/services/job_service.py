from datetime import datetime, timedelta
from sqlalchemy import func
from ..models import Job, JobDocument, JobWorker, JobTimeline
from ....models import db
import os
import uuid
from werkzeug.utils import secure_filename

class JobService:
    def __init__(self):
        self.upload_folder = os.path.join(os.getcwd(), 'uploads', 'job_documents')
        self.allowed_extensions = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png', 'gif'}
        
        # Create upload folder if it doesn't exist
        os.makedirs(self.upload_folder, exist_ok=True)

    def create_job(self, data, provider_id):
        """Create a new job"""
        try:
            job = Job(
                title=data['title'],
                description=data['description'],
                location=data['location'],
                start_date=datetime.fromisoformat(data['startDate'].replace('Z', '+00:00')),
                end_date=datetime.fromisoformat(data['endDate'].replace('Z', '+00:00')) if data.get('endDate') else None,
                budget=float(data['budget']),
                priority=data.get('priority', 'medium'),
                status=data.get('status', 'pending'),
                categories=data.get('categories', []),
                notes=data.get('notes', ''),
                customer_id=data['customerId'],
                provider_id=provider_id,
                progress=0
            )
            
            db.session.add(job)
            db.session.commit()
            
            return job
            
        except Exception as e:
            db.session.rollback()
            raise e

    def update_job(self, job, data):
        """Update an existing job"""
        try:
            # Update fields if provided
            if 'title' in data:
                job.title = data['title']
            if 'description' in data:
                job.description = data['description']
            if 'location' in data:
                job.location = data['location']
            if 'startDate' in data:
                job.start_date = datetime.fromisoformat(data['startDate'].replace('Z', '+00:00'))
            if 'endDate' in data and data['endDate']:
                job.end_date = datetime.fromisoformat(data['endDate'].replace('Z', '+00:00'))
            if 'budget' in data:
                job.budget = float(data['budget'])
            if 'priority' in data:
                job.priority = data['priority']
            if 'status' in data:
                job.status = data['status']
            if 'categories' in data:
                job.categories = data['categories']
            if 'notes' in data:
                job.notes = data['notes']
            if 'progress' in data:
                job.progress = int(data['progress'])
            if 'customerId' in data:
                job.customer_id = data['customerId']
            
            job.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return job
            
        except Exception as e:
            db.session.rollback()
            raise e

    def get_job_stats(self, provider_id):
        """Get job statistics for a provider"""
        try:
            # Total jobs
            total_jobs = Job.query.filter_by(provider_id=provider_id).count()
            
            # Jobs by status
            status_stats = db.session.query(
                Job.status,
                func.count(Job.id).label('count')
            ).filter_by(provider_id=provider_id).group_by(Job.status).all()
            
            status_dict = {status: count for status, count in status_stats}
            
            # Jobs by priority
            priority_stats = db.session.query(
                Job.priority,
                func.count(Job.id).label('count')
            ).filter_by(provider_id=provider_id).group_by(Job.priority).all()
            
            priority_dict = {priority: count for priority, count in priority_stats}
            
            # Total budget
            total_budget = db.session.query(
                func.sum(Job.budget)
            ).filter_by(provider_id=provider_id).scalar() or 0
            
            # Average budget
            avg_budget = db.session.query(
                func.avg(Job.budget)
            ).filter_by(provider_id=provider_id).scalar() or 0
            
            # Overdue jobs
            overdue_count = Job.query.filter(
                Job.provider_id == provider_id,
                Job.status == 'in_progress',
                Job.end_date < datetime.utcnow()
            ).count()
            
            # Recent jobs (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_jobs = Job.query.filter(
                Job.provider_id == provider_id,
                Job.created_at >= thirty_days_ago
            ).count()
            
            return {
                'total': total_jobs,
                'byStatus': status_dict,
                'byPriority': priority_dict,
                'totalBudget': float(total_budget),
                'averageBudget': float(avg_budget),
                'overdueCount': overdue_count,
                'recentCount': recent_jobs,
                'pending': status_dict.get('pending', 0),
                'inProgress': status_dict.get('in_progress', 0),
                'completed': status_dict.get('completed', 0),
                'cancelled': status_dict.get('cancelled', 0),
                'onHold': status_dict.get('on_hold', 0)
            }
            
        except Exception as e:
            raise e

    def upload_document(self, job_id, file, provider_id):
        """Upload a document for a job"""
        try:
            if file and self.allowed_file(file.filename):
                # Generate unique filename
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file_path = os.path.join(self.upload_folder, unique_filename)
                
                # Save file
                file.save(file_path)
                
                # Create document record
                document = JobDocument(
                    job_id=job_id,
                    name=filename,
                    file_path=file_path,
                    file_size=os.path.getsize(file_path),
                    file_type=file.content_type or 'application/octet-stream',
                    uploaded_by=provider_id
                )
                
                db.session.add(document)
                db.session.commit()
                
                return document
            else:
                raise ValueError("Invalid file type")
                
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_document_file(self, file_path):
        """Delete a document file from storage"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            # Log error but don't raise - file deletion failure shouldn't break the operation
            print(f"Error deleting file {file_path}: {str(e)}")

    def assign_worker(self, job_id, worker_id, role):
        """Assign a worker to a job"""
        try:
            # Check if worker is already assigned
            existing_assignment = JobWorker.query.filter_by(
                job_id=job_id,
                worker_id=worker_id,
                is_active=True
            ).first()
            
            if existing_assignment:
                # Update role if different
                existing_assignment.role = role
                existing_assignment.assigned_at = datetime.utcnow()
            else:
                # Create new assignment
                job_worker = JobWorker(
                    job_id=job_id,
                    worker_id=worker_id,
                    role=role,
                    assigned_at=datetime.utcnow()
                )
                db.session.add(job_worker)
            
            db.session.commit()
            
            return existing_assignment or job_worker
            
        except Exception as e:
            db.session.rollback()
            raise e

    def remove_worker(self, job_id, worker_id):
        """Remove a worker from a job"""
        try:
            assignment = JobWorker.query.filter_by(
                job_id=job_id,
                worker_id=worker_id,
                is_active=True
            ).first()
            
            if assignment:
                assignment.is_active = False
                db.session.commit()
                return True
            
            return False
            
        except Exception as e:
            db.session.rollback()
            raise e

    def add_timeline_entry(self, job_id, title, description, activity_type, created_by):
        """Add an entry to the job timeline"""
        try:
            timeline_entry = JobTimeline(
                job_id=job_id,
                title=title,
                description=description,
                type=activity_type,
                created_by=created_by
            )
            
            db.session.add(timeline_entry)
            db.session.commit()
            
            return timeline_entry
            
        except Exception as e:
            db.session.rollback()
            raise e

    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def get_file_size_human(self, size_bytes):
        """Get human readable file size"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

    def search_jobs(self, provider_id, search_term, filters=None):
        """Search jobs with filters"""
        try:
            query = Job.query.filter_by(provider_id=provider_id)
            
            # Apply search term
            if search_term:
                search_term = f"%{search_term}%"
                query = query.filter(
                    Job.title.ilike(search_term) |
                    Job.description.ilike(search_term) |
                    Job.location.ilike(search_term)
                )
            
            # Apply filters
            if filters:
                if filters.get('status') and filters['status'] != 'all':
                    query = query.filter(Job.status == filters['status'])
                
                if filters.get('priority') and filters['priority'] != 'all':
                    query = query.filter(Job.priority == filters['priority'])
                
                if filters.get('category') and filters['category'] != 'all':
                    query = query.filter(Job.categories.contains([filters['category']]))
                
                if filters.get('dateRange') and filters['dateRange'] != 'all':
                    date_range = filters['dateRange']
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
            
            return query.order_by(Job.created_at.desc()).all()
            
        except Exception as e:
            raise e

    def get_jobs_by_customer(self, provider_id, customer_id):
        """Get all jobs for a specific customer"""
        try:
            return Job.query.filter_by(
                provider_id=provider_id,
                customer_id=customer_id
            ).order_by(Job.created_at.desc()).all()
            
        except Exception as e:
            raise e

    def get_upcoming_jobs(self, provider_id, days=7):
        """Get jobs starting in the next N days"""
        try:
            from datetime import timedelta
            future_date = datetime.utcnow() + timedelta(days=days)
            
            return Job.query.filter(
                Job.provider_id == provider_id,
                Job.status.in_(['pending', 'in_progress']),
                Job.start_date <= future_date,
                Job.start_date >= datetime.utcnow()
            ).order_by(Job.start_date.asc()).all()
            
        except Exception as e:
            raise e

    def get_overdue_jobs(self, provider_id):
        """Get overdue jobs"""
        try:
            return Job.query.filter(
                Job.provider_id == provider_id,
                Job.status == 'in_progress',
                Job.end_date < datetime.utcnow()
            ).order_by(Job.end_date.asc()).all()
            
        except Exception as e:
            raise e
