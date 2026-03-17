import { useEffect } from "react";
import useGlobalReducer from "../../hooks/useGlobalReducer";

export const DashboardHome = () => {
    const { store, dispatch } = useGlobalReducer();

    useEffect(() => {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(b => b.remove());

        document.body.classList.remove('modal-open');
        document.body.style.overflow = 'auto';
        document.body.style.paddingRight = '0';
    }, []);

    return (
        <>
            <div className="dashboard-welcome-section">
                <div className="dashboard-welcome-content">
                    <h1 className="dashboard-welcome-title">Welcome back, {store.provider ? store.provider?.name : "Contractor"}!</h1>
                    <p className="dashboard-welcome-subtitle">Here's what's happening with your business today.</p>
                </div>
            </div>

            <div className="row dashboard-stats-grid">
                <div className="col-12 col-sm-6 col-lg-3 mb-4">
                    <div className="dashboard-stat-card">
                        <div className="dashboard-stat-content">
                            <div className="dashboard-stat-info">
                                <p className="dashboard-stat-label">Total Revenue</p>
                                <p className="dashboard-stat-value">$12,450</p>
                                <p className="dashboard-stat-change positive">+12% from last month</p>
                            </div>
                            <div className="dashboard-stat-icon revenue">
                                <span className="dashboard-stat-icon-symbol">$</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="col-12 col-sm-6 col-lg-3 mb-4">
                    <div className="dashboard-stat-card">
                        <div className="dashboard-stat-content">
                            <div className="dashboard-stat-info">
                                <p className="dashboard-stat-label">Active Jobs</p>
                                <p className="dashboard-stat-value">24</p>
                                <p className="dashboard-stat-change neutral">3 new today</p>
                            </div>
                            <div className="dashboard-stat-icon jobs">
                                <span className="dashboard-stat-icon-symbol">📋</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="col-12 col-sm-6 col-lg-3 mb-4">
                    <div className="dashboard-stat-card">
                        <div className="dashboard-stat-content">
                            <div className="dashboard-stat-info">
                                <p className="dashboard-stat-label">New Customers</p>
                                <p className="dashboard-stat-value">8</p>
                                <p className="dashboard-stat-change positive">+2 from last week</p>
                            </div>
                            <div className="dashboard-stat-icon customers">
                                <span className="dashboard-stat-icon-symbol">👥</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="col-12 col-sm-6 col-lg-3 mb-4">
                    <div className="dashboard-stat-card">
                        <div className="dashboard-stat-content">
                            <div className="dashboard-stat-info">
                                <p className="dashboard-stat-label">Pending Invoices</p>
                                <p className="dashboard-stat-value">$3,200</p>
                                <p className="dashboard-stat-change negative">2 overdue</p>
                            </div>
                            <div className="dashboard-stat-icon invoices">
                                <span className="dashboard-stat-icon-symbol">📄</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row mb-4">
                <div className="col-12">
                    <h2 className="dashboard-section-title mb-3">Quick Actions</h2>
                    <div className="dashboard-quick-actions">
                        <div className="quick-action-card">
                            <div className="quick-action-icon">
                                <i className="bi bi-plus-circle"></i>
                            </div>
                            <h4>Create Job</h4>
                            <p>Add a new job or project</p>
                        </div>

                        <div className="quick-action-card">
                            <div className="quick-action-icon">
                                <i className="bi bi-file-text"></i>
                            </div>
                            <h4>New Estimate</h4>
                            <p>Create estimate for customer</p>
                        </div>

                        <div className="quick-action-card">
                            <div className="quick-action-icon">
                                <i className="bi bi-receipt"></i>
                            </div>
                            <h4>Send Invoice</h4>
                            <p>Bill for completed work</p>
                        </div>

                        <div className="quick-action-card">
                            <div className="quick-action-icon">
                                <i className="bi bi-person-plus"></i>
                            </div>
                            <h4>Add Customer</h4>
                            <p>Register new customer</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row">
                <div className="col-lg-8 mb-4">
                    <div className="dashboard-recent-activity">
                        <h2 className="dashboard-section-title mb-3">Recent Activity</h2>
                        <div className="activity-list">
                            <div className="activity-item">
                                <div className="activity-icon">
                                    <i className="bi bi-check-circle text-success"></i>
                                </div>
                                <div className="activity-content">
                                    <h5>Job Completed</h5>
                                    <p>Kitchen Renovation - John Smith</p>
                                    <small className="text-muted">2 hours ago</small>
                                </div>
                                <div className="activity-amount">
                                    <span className="text-success">+$2,500</span>
                                </div>
                            </div>

                            <div className="activity-item">
                                <div className="activity-icon">
                                    <i className="bi bi-file-text text-primary"></i>
                                </div>
                                <div className="activity-content">
                                    <h5>New Estimate Request</h5>
                                    <p>Bathroom Remodel - Sarah Johnson</p>
                                    <small className="text-muted">5 hours ago</small>
                                </div>
                                <div className="activity-amount">
                                    <span className="text-primary">Pending</span>
                                </div>
                            </div>

                            <div className="activity-item">
                                <div className="activity-icon">
                                    <i className="bi bi-receipt text-warning"></i>
                                </div>
                                <div className="activity-content">
                                    <h5>Invoice Sent</h5>
                                    <p>Deck Construction - Mike Wilson</p>
                                    <small className="text-muted">1 day ago</small>
                                </div>
                                <div className="activity-amount">
                                    <span className="text-warning">$1,800</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="col-lg-4 mb-4">
                    <div className="dashboard-upcoming">
                        <h2 className="dashboard-section-title mb-3">Upcoming Jobs</h2>
                        <div className="upcoming-list">
                            <div className="upcoming-item">
                                <div className="upcoming-date">
                                    <span className="date-day">15</span>
                                    <span className="date-month">MAR</span>
                                </div>
                                <div className="upcoming-content">
                                    <h5>Roof Repair</h5>
                                    <p className="text-muted">Customer: Tom Brown</p>
                                    <span className="badge bg-primary">In Progress</span>
                                </div>
                            </div>

                            <div className="upcoming-item">
                                <div className="upcoming-date">
                                    <span className="date-day">18</span>
                                    <span className="date-month">MAR</span>
                                </div>
                                <div className="upcoming-content">
                                    <h5>Window Installation</h5>
                                    <p className="text-muted">Customer: Lisa Davis</p>
                                    <span className="badge bg-warning">Scheduled</span>
                                </div>
                            </div>

                            <div className="upcoming-item">
                                <div className="upcoming-date">
                                    <span className="date-day">22</span>
                                    <span className="date-month">MAR</span>
                                </div>
                                <div className="upcoming-content">
                                    <h5>Painting Project</h5>
                                    <p className="text-muted">Customer: Robert Lee</p>
                                    <span className="badge bg-info">Estimate</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};
