from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..models import db

class Job(db.Model):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(200), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    budget = Column(Float, nullable=False)
    priority = Column(String(20), nullable=False, default='medium')
    status = Column(String(20), nullable=False, default='pending')
    categories = Column(JSON)  # List of categories
    notes = Column(Text)
    progress = Column(Integer, default=0)
    
    # Foreign Keys
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    provider_id = Column(Integer, ForeignKey('providers.id'), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    customer = relationship('Customer', back_populates='jobs')
    provider = relationship('Provider', back_populates='jobs')
    documents = relationship('JobDocument', back_populates='job', cascade='all, delete-orphan')
    workers = relationship('JobWorker', back_populates='job', cascade='all, delete-orphan')
    timeline = relationship('JobTimeline', back_populates='job', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Job {self.id}: {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'startDate': self.start_date.isoformat() if self.start_date else None,
            'endDate': self.end_date.isoformat() if self.end_date else None,
            'budget': self.budget,
            'priority': self.priority,
            'status': self.status,
            'categories': self.categories or [],
            'notes': self.notes,
            'progress': self.progress,
            'customerId': self.customer_id,
            'providerId': self.provider_id,
            'customer': self.customer.to_dict() if self.customer else None,
            'provider': self.provider.to_dict() if self.provider else None,
            'documents': [doc.to_dict() for doc in self.documents],
            'workers': [worker.to_dict() for worker in self.workers],
            'timeline': [activity.to_dict() for activity in self.timeline],
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_valid_priorities(cls):
        return ['low', 'medium', 'high', 'urgent']
    
    @classmethod
    def get_valid_statuses(cls):
        return ['pending', 'in_progress', 'completed', 'cancelled', 'on_hold']
    
    def is_valid_priority(self, priority):
        return priority in self.get_valid_priorities()
    
    def is_valid_status(self, status):
        return status in self.get_valid_statuses()
    
    def can_change_status(self, new_status):
        """Check if status change is valid"""
        valid_transitions = {
            'pending': ['in_progress', 'cancelled'],
            'in_progress': ['completed', 'cancelled', 'on_hold'],
            'on_hold': ['in_progress', 'cancelled'],
            'completed': [],  # Terminal state
            'cancelled': []   # Terminal state
        }
        return new_status in valid_transitions.get(self.status, [])
    
    def is_overdue(self):
        """Check if job is overdue"""
        if self.status in ['completed', 'cancelled']:
            return False
        if self.end_date and self.end_date < func.now():
            return True
        return False
    
    def get_duration_days(self):
        """Get job duration in days"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None


class JobDocument(db.Model):
    __tablename__ = 'job_documents'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(100))
    uploaded_by = Column(Integer, ForeignKey('providers.id'), nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    job = relationship('Job', back_populates='documents')
    uploader = relationship('Provider')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'filePath': self.file_path,
            'fileSize': self.file_size,
            'fileType': self.file_type,
            'uploadedAt': self.created_at.isoformat() if self.created_at else None
        }


class JobWorker(db.Model):
    __tablename__ = 'job_workers'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    role = Column(String(100))
    assigned_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    job = relationship('Job', back_populates='workers')
    worker = relationship('Worker')
    
    def to_dict(self):
        return {
            'id': self.id,
            'workerId': self.worker_id,
            'role': self.role,
            'assignedAt': self.assigned_at.isoformat() if self.assigned_at else None,
            'isActive': self.is_active,
            'worker': self.worker.to_dict() if self.worker else None
        }


class JobTimeline(db.Model):
    __tablename__ = 'job_timeline'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)  # created, updated, status_changed, etc.
    created_by = Column(Integer, ForeignKey('providers.id'), nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    job = relationship('Job', back_populates='timeline')
    creator = relationship('Provider')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'createdBy': self.created_by
        }
