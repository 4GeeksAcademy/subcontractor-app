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

    provider: Mapped['Provider'] = relationship(back_populates='user')
    client: Mapped['Client'] = relationship(back_populates='userClient')

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
    cover_image: Mapped[str] = mapped_column(String(20), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    business_email: Mapped[str] = mapped_column(str())
    website_slug: Mapped[str] = mapped_column(String())
    about: Mapped[str] = mapped_column(str())
    payment_link: Mapped[str] = mapped_column(str())
    subscription_status: Mapped[str] = mapped_column()
    plan_type: Mapped[str] = mapped_column(str)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    contractor_invoice: Mapped[list['Invoice']] = relationship(
        back_populates='invoice_contractor')
    services: Mapped[list['Services']] = relationship(
        back_populates='providerServices', cascade='all, delete-orphan')
    user: Mapped['User'] = relationship(back_populates='provider')
    contractor_job: Mapped[list['Job']] = relationship(
        back_populates='job_contractor')
    service_contr: Mapped[list['Services']] = relationship(
        back_populates='contractorServices')

    project_provider: Mapped[list['PortfolioProject']
                             ] = relationship(back_populates='provider_project')


class Customer(db.Model):
    __tablename__ = 'client'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    contractor_id: Mapped[int] = mapped_column(
        ForeignKey('contractor.id'), nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    note: Mapped[str] = mapped_column(String(500))
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    userClient: Mapped['User'] = relationship(back_populates='client')
    customer_invoice: Mapped[list['Invoice']] = relationship(
        back_populates='invoice_customer')
    customer_job: Mapped[list['Job']] = relationship(
        back_populates='job_customer')
    reviewClient: Mapped[list['Review']] = relationship(
        back_populates='clientReview')
    favorite_client: Mapped[list['Favorite']] = relationship(
        back_populates='client_fav')


class Services(db.Model):
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(
        ForeignKey('provider.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[float] = mapped_column(Float)
    duration: Mapped[int] = mapped_column(Integer)
    image: Mapped[str] = mapped_column(String())
    materials_needed: Mapped[str] = mapped_column(String())
    estimate_hours: Mapped[float] = mapped_column(float, nullable=True)
    base_cost: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    contractorServices: Mapped['Contractor'] = relationship(
        back_populates='')
    job: Mapped['Job'] = relationship(
        back_populates='service')
    material_service: Mapped[list['ServiceMaterial']] = relationship(
        back_populates='service_mat')


class ServiceMaterial(db.Model):
    __tablename__ = 'servicesMaterial'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_id: Mapped[int] = mapped_column(
        ForeignKey('service.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(120))
    quantity: Mapped[Numeric] = mapped_column(Numeric())
    unit_cost: Mapped[float] = mapped_column(Float)

    service_mat: Mapped['Services'] = relationship(
        back_populates='')


class Job(db.Model):
    __tablename__ = 'job'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contractor_id: Mapped[int] = mapped_column(
        ForeignKey('contractor.id'), nullable=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey('customer.id'), nullable=False)
    service_id: Mapped[int] = mapped_column(
        ForeignKey('service.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String())
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), nullable=False)
    schedule_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    estimate_total: Mapped[float] = mapped_column(Float)
    actual_total: Mapped[float] = mapped_column(Float)
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


class Invoice(db.Model):
    __tablename__ = 'invoice'
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
    subtotal: Mapped[Decimal] = mapped_column(Decimal)
    tax:  Mapped[Decimal] = mapped_column(Decimal)
    total_amout:  Mapped[Decimal] = mapped_column(Decimal)
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus), nullable=False)
    payment_link: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod), nullable=False)
    notes: Mapped[str] = mapped_column(String(500), nullable=False)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    payment: Mapped['Payment'] = relationship(backpopulates='invoice_payment')
    invoice_contractor: Mapped['Contractor'] = relationship(
        back_populates='contractor_invoice')
    invoice_customer: Mapped['Customer'] = relationship(
        back_populates='customer_invoice')
    invoice_job: Mapped['Job'] = relationship(
        back_populates='job_invoice')


class InvoiceItem(db.Model):
    __tablename__ = 'invoiceItem'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey('invoice.id'), nullable=False)
    description: Mapped[str] = mapped_column(String())
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(float)
    amount: Mapped[Decimal] = mapped_column(Decimal)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())


class Payment(db.Model):
    __tablename__ = 'payment'
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


class PortfolioProject(db.Model):
    __tablename__ = 'portfolioproject'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(
        ForeignKey('provider.id'), nullable=False)
    title: Mapped[str] = mapped_column(String())
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    provider_project: Mapped['Provider'] = relationship(
        back_populates='project_provider')
    image: Mapped[list['PortfolioImage']] = relationship(
        back_populates='project')


class PortfolioImage(db.Model):
    __tablename__ = 'portfolioimage'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    portfolioproject_id: Mapped[int] = mapped_column(
        ForeignKey('portfolioproject.id'), nullable=False)
    image_url:  Mapped[str] = mapped_column(String(500), nullable=False)
    is_corver: Mapped[bool] = mapped_column(Boolean, default=False)
    order_index: Mapped[int] = mapped_column(Integer)

    project: Mapped['PortfolioProject'] = relationship(back_populates='image')
