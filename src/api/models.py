import enum
from datetime import datetime, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Enum, DateTime, func, ForeignKey, Float, UniqueConstraint, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal

db = SQLAlchemy()


class UserRole(enum.Enum):
    CONTRACTOR = "contractor"
    CUSTOMER = "customer"


class JobStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    canceled = "canceled"


class PaymentMethod(enum.Enum):
    stripe = "stripe"
    square = "square"
    zelle = "zelle"
    cash = "cash"
    check = "check"


class PaymentStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    refunded = "refunded"
    failed = "failed"


class InvoiceStatus(enum.Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    overdue = "overdue"


class SubscriptionStatus(enum.Enum):
    free = "free"
    trial = "trial"
    active = "active"
    past_due = "past_due"
    canceled = "canceled"


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    provider: Mapped['Contractor'] = relationship(back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Contractor(db.Model):
    __tablename__ = 'contractor'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    business_name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    logo_image: Mapped[str] = mapped_column(String(), nullable=False)
    cover_image: Mapped[str] = mapped_column(String(500), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    business_email: Mapped[str] = mapped_column(String())
    website_slug: Mapped[str] = mapped_column(
        String(500), default=False, unique=True, index=True)
    about: Mapped[str] = mapped_column(String())
    payment_link: Mapped[str] = mapped_column(String(500), nullable=True)
    subscription_status: Mapped[SubscriptionStatus] = mapped_column(Enum(
        SubscriptionStatus), default=SubscriptionStatus.free, nullable=False, index=True)
    plan_type: Mapped[str] = mapped_column(String(50), nullable=True)
    subscription_renewal_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)
    tax_rate: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(10), default='USD')
    invoice_prefix: Mapped[str] = mapped_column(String(10), default='INV')
    stripe_account_id: Mapped[str] = mapped_column(String(255), nullable=True)
    stripe_onboarding_complete: Mapped[bool] = mapped_column(
        Boolean, default=False)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    contractor_invoice: Mapped[list['Invoice']] = relationship(
        back_populates='invoice_contractor')
    user: Mapped['User'] = relationship(back_populates='provider')
    contractor_job: Mapped[list['Job']] = relationship(
        back_populates='job_contractor')
    service_contr: Mapped[list['Services']] = relationship(
        back_populates='contractorServices')
    project_provider: Mapped[list['PortfolioProject']
                             ] = relationship(back_populates='provider_project')
    estimate_contractor: Mapped[list['EstimateRequest']] = relationship(
        back_populates='contractor_estimate')

    __table_args__ = (db.Index('idx_contractor_verified',
                               'is_verified', 'subscription_status','plan_type'),)


class Customer(db.Model):
    __tablename__ = 'customer'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contractor_id: Mapped[int] = mapped_column(
        ForeignKey('contractor.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    note: Mapped[str] = mapped_column(String(500))
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    customer_invoice: Mapped[list['Invoice']] = relationship(
        back_populates='invoice_customer')
    customer_job: Mapped[list['Job']] = relationship(
        back_populates='job_customer')

    __table_args__ = (db.Index('idx_customer_contractor',
                      'contractor_id', 'email'),)


class Services(db.Model):
    __tablename__ = 'services'
    __table_args__ = (db.UniqueConstraint(
        'contractor_id', 'name', name='unique_service_per_contractor'),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contractor_id: Mapped[int] = mapped_column(
        ForeignKey('contractor.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[float] = mapped_column(Float)
    duration: Mapped[int] = mapped_column(Integer)
    image: Mapped[str] = mapped_column(String())
    materials_needed: Mapped[str] = mapped_column(String())
    estimate_hours: Mapped[float] = mapped_column(Float, nullable=True)
    base_cost: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    contractorServices: Mapped['Contractor'] = relationship(
        back_populates='service_contr')
    job: Mapped['Job'] = relationship(
        back_populates='service')
    material_service: Mapped[list['ServiceMaterial']] = relationship(
        back_populates='service_mat')


class ServiceMaterial(db.Model):
    __tablename__ = 'servicesMaterial'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_id: Mapped[int] = mapped_column(
        ForeignKey('services.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(120))
    quantity: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    unit_cost: Mapped[float] = mapped_column(Float)

    service_mat: Mapped['Services'] = relationship(
        back_populates='material_service')


class Job(db.Model):
    __tablename__ = 'job'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contractor_id: Mapped[int] = mapped_column(
        ForeignKey('contractor.id'), nullable=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey('customer.id'), nullable=False)
    service_id: Mapped[int] = mapped_column(
        ForeignKey('services.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String())
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), nullable=False)
    schedule_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    estimate_total: Mapped[float] = mapped_column(Float)
    actual_total: Mapped[float] = mapped_column(Float)
    start_date:  Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True)
    end_date:  Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    job_invoice: Mapped[list['Invoice']] = relationship(
        back_populates='invoice_job')
    job_contractor: Mapped['Contractor'] = relationship(
        back_populates='contractor_job')
    job_customer: Mapped['Customer'] = relationship(
        back_populates='customer_job')
    service: Mapped['Services'] = relationship(
        back_populates='job')

    __table_args__ = (db.Index('idx_job_contractor_dates', 'contractor_id', 'schedule_date'),
                      db.Index('idx_job_status', 'status'), )


class Invoice(db.Model):
    __tablename__ = 'invoice'
    __table_args__ = (
        db.CheckConstraint('total_amount = subtotal + tax', name='check_invoice_total'),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contractor_id: Mapped[int] = mapped_column(
        ForeignKey('contractor.id'), nullable=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey('customer.id'), nullable=False)
    job_id: Mapped[int] = mapped_column(
        ForeignKey('job.id'), nullable=False)
    invoice_number: Mapped[int] = mapped_column(Integer, nullable=False)
    issue_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    due_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    subtotal: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    tax:  Mapped[Numeric] = mapped_column(Numeric(10, 2))
    total_amount:  Mapped[Numeric] = mapped_column(Numeric(10, 2))
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus), nullable=False)
    payment_link: Mapped[str] = mapped_column(String(500), nullable=False)
    notes: Mapped[str] = mapped_column(String(500), nullable=False)
    paid_at:  Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    sent_at:  Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    stripe_payment_intent_id: Mapped[str] = mapped_column(
        String(255), nullable=True)
    stripe_payment_link_id: Mapped[str] = mapped_column(
        String(255), nullable=True)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    payment: Mapped['Payment'] = relationship(back_populates='invoice_payment')
    invoice_contractor: Mapped['Contractor'] = relationship(
        back_populates='contractor_invoice')
    invoice_customer: Mapped['Customer'] = relationship(
        back_populates='customer_invoice')
    invoice_job: Mapped['Job'] = relationship(
        back_populates='job_invoice')

    __table_args__ = (db.Index('idx_invoice_contractor_status', 'contractor_id', 'status'),
                      db.Index('idx_invoice_dates', 'issue_date', 'due_date'),
                      db.Index('idx_invoice_overdue', 'status', 'due_date'), )


class InvoiceItem(db.Model):
    __tablename__ = 'invoiceItem'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey('invoice.id'), nullable=False)
    description: Mapped[str] = mapped_column(String())
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    amount: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())


class Payment(db.Model):
    __tablename__ = 'payment'
    __table_args__ = (
        db.CheckConstraint('amount > 0', name='check_payment_amount'),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey('invoice.id'), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod), nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), nullable=False)
    transaction_id: Mapped[str] = mapped_column(String(255))
    paid_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    invoice_payment: Mapped['Invoice'] = relationship(
        back_populates='payment')

    __table_args__ = (db.Index('idx_payment_invoice', 'invoice_id'),
                      db.Index('idx_payment_status', 'payment_status'),)


class PortfolioProject(db.Model):
    __tablename__ = 'portfolioproject'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(
        ForeignKey('contractor.id'), nullable=False)
    title: Mapped[str] = mapped_column(String())
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    provider_project: Mapped['Contractor'] = relationship(
        back_populates='project_provider')
    image: Mapped[list['PortfolioImage']] = relationship(
        back_populates='project')


class PortfolioImage(db.Model):
    __tablename__ = 'portfolioimage'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    portfolioproject_id: Mapped[int] = mapped_column(
        ForeignKey('portfolioproject.id'), nullable=False)
    image_url:  Mapped[str] = mapped_column(String(500), nullable=False)
    is_cover: Mapped[bool] = mapped_column(Boolean, default=False)
    order_index: Mapped[int] = mapped_column(Integer)

    project: Mapped['PortfolioProject'] = relationship(back_populates='image')


class EstimateRequest(db.Model):
    __tablename__ = 'estimateRequest'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contractor_id: Mapped[int] = mapped_column(
        ForeignKey('contractor.id'), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(120))
    customer_email: Mapped[str] = mapped_column(String(120))
    customer_phone: Mapped[str] = mapped_column(String(20))
    service_id: Mapped[int] = mapped_column(
        ForeignKey('services.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    contractor_estimate: Mapped['Contractor'] = relationship(
        back_populates='estimate_contractor')
