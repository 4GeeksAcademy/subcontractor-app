import { useEffect } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";

export const ProviderDashboard = () => {
    useEffect(() => {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(b => b.remove());

        document.body.classList.remove('modal-open');
        document.body.style.overflow = 'auto';
        document.body.style.paddingRight = '0';
    }, []);

    return (
        <DashboardLayout>
            <div className="dashboard-welcome-section">
                <div className="dashboard-welcome-content">
                    <h1 className="dashboard-welcome-title">Welcome back, John!</h1>
                    <p className="dashboard-welcome-subtitle">Here's what's happening with your business today.</p>
                </div>
            </div>

            {/* Stats Grid */}
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
                                <p className="dashboard-stat-change neutral">This week</p>
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
                                <p className="dashboard-stat-label">Pending Estimates</p>
                                <p className="dashboard-stat-value">5</p>
                                <p className="dashboard-stat-change neutral">Awaiting response</p>
                            </div>
                            <div className="dashboard-stat-icon estimates">
                                <span className="dashboard-stat-icon-symbol">📄</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Recent Activity */}
            <div className="dashboard-activity-section">
                <div className="dashboard-activity-header">
                    <h2 className="dashboard-activity-title">Recent Activity</h2>
                </div>
                <div className="dashboard-activity-content">
                    <div className="dashboard-activity-list">
                        <div className="dashboard-activity-item">
                            <div className="dashboard-activity-icon payment">
                                <span className="dashboard-activity-icon-symbol">✓</span>
                            </div>
                            <div className="dashboard-activity-details">
                                <p className="dashboard-activity-title">New payment received</p>
                                <p className="dashboard-activity-description">John Smith paid $500 for Kitchen Renovation</p>
                            </div>
                            <span className="dashboard-activity-time">2 hours ago</span>
                        </div>

                        <div className="dashboard-activity-item">
                            <div className="dashboard-activity-icon job">
                                <span className="dashboard-activity-icon-symbol">📋</span>
                            </div>
                            <div className="dashboard-activity-details">
                                <p className="dashboard-activity-title">New job created</p>
                                <p className="dashboard-activity-description">Bathroom remodeling for Sarah Johnson</p>
                            </div>
                            <span className="dashboard-activity-time">5 hours ago</span>
                        </div>

                        <div className="dashboard-activity-item">
                            <div className="dashboard-activity-icon customer">
                                <span className="dashboard-activity-icon-symbol">👥</span>
                            </div>
                            <div className="dashboard-activity-details">
                                <p className="dashboard-activity-title">New customer registered</p>
                                <p className="dashboard-activity-description">Mike Wilson signed up for services</p>
                            </div>
                            <span className="dashboard-activity-time">1 day ago</span>
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
};