import React, { useState } from 'react';
import { jobCategories, jobPriorities, jobStatuses } from '../utils/jobConstants';
import './JobFilters.css';

export const JobFilters = ({ filters, onFiltersChange }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const handleFilterChange = (filterName, value) => {
        onFiltersChange({
            ...filters,
            [filterName]: value
        });
    };

    const handleSearchChange = (e) => {
        handleFilterChange('search', e.target.value);
    };

    const handleQuickFilter = (quickFilter) => {
        switch (quickFilter) {
            case 'today':
                handleFilterChange('dateRange', 'today');
                break;
            case 'week':
                handleFilterChange('dateRange', 'week');
                break;
            case 'month':
                handleFilterChange('dateRange', 'month');
                break;
            case 'active':
                handleFilterChange('status', 'in_progress');
                break;
            case 'completed':
                handleFilterChange('status', 'completed');
                break;
            default:
                break;
        }
    };

    const resetFilters = () => {
        onFiltersChange({
            status: 'all',
            category: 'all',
            priority: 'all',
            dateRange: 'all',
            search: ''
        });
    };

    const hasActiveFilters = filters.status !== 'all' ||
        filters.category !== 'all' ||
        filters.priority !== 'all' ||
        filters.dateRange !== 'all' ||
        filters.search !== '';

    return (
        <div className="job-filters">
            <div className="job-filters-header">
                <h4>Filters</h4>
                <div className="job-filters-controls">
                    <button
                        type="button"
                        className="btn btn-sm btn-outline-secondary"
                        onClick={() => setIsExpanded(!isExpanded)}
                    >
                        <i className={`bi ${isExpanded ? 'bi-chevron-up' : 'bi-chevron-down'}`}></i>
                        {isExpanded ? 'Hide' : 'Show'} Filters
                    </button>
                    {hasActiveFilters && (
                        <button
                            type="button"
                            className="btn btn-sm btn-outline-danger"
                            onClick={resetFilters}
                        >
                            <i className="bi bi-x-circle"></i>
                            Clear
                        </button>
                    )}
                </div>
            </div>

            {isExpanded && (
                <div className="job-filters-content">
                    {/* Search */}
                    <div className="filter-group">
                        <label htmlFor="search" className="form-label">Search Jobs</label>
                        <div className="input-group">
                            <input
                                type="text"
                                className="form-control"
                                id="search"
                                placeholder="Search by title, description, or location..."
                                value={filters.search}
                                onChange={handleSearchChange}
                            />
                            <span className="input-group-text">
                                <i className="bi bi-search"></i>
                            </span>
                        </div>
                    </div>

                    {/* Quick Filters */}
                    <div className="filter-group">
                        <label className="form-label">Quick Filters</label>
                        <div className="quick-filters">
                            <button
                                type="button"
                                className={`btn btn-sm ${filters.dateRange === 'today' ? 'btn-primary' : 'btn-outline-primary'}`}
                                onClick={() => handleQuickFilter('today')}
                            >
                                Today
                            </button>
                            <button
                                type="button"
                                className={`btn btn-sm ${filters.dateRange === 'week' ? 'btn-primary' : 'btn-outline-primary'}`}
                                onClick={() => handleQuickFilter('week')}
                            >
                                This Week
                            </button>
                            <button
                                type="button"
                                className={`btn btn-sm ${filters.dateRange === 'month' ? 'btn-primary' : 'btn-outline-primary'}`}
                                onClick={() => handleQuickFilter('month')}
                            >
                                This Month
                            </button>
                            <button
                                type="button"
                                className={`btn btn-sm ${filters.status === 'in_progress' ? 'btn-primary' : 'btn-outline-primary'}`}
                                onClick={() => handleQuickFilter('active')}
                            >
                                Active
                            </button>
                            <button
                                type="button"
                                className={`btn btn-sm ${filters.status === 'completed' ? 'btn-primary' : 'btn-outline-primary'}`}
                                onClick={() => handleQuickFilter('completed')}
                            >
                                Completed
                            </button>
                        </div>
                    </div>

                    {/* Status Filter */}
                    <div className="filter-group">
                        <label htmlFor="status" className="form-label">Status</label>
                        <select
                            className="form-select"
                            id="status"
                            value={filters.status}
                            onChange={(e) => handleFilterChange('status', e.target.value)}
                        >
                            <option value="all">All Statuses</option>
                            {jobStatuses.map(status => (
                                <option key={status.value} value={status.value}>
                                    {status.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Category Filter */}
                    <div className="filter-group">
                        <label htmlFor="category" className="form-label">Category</label>
                        <select
                            className="form-select"
                            id="category"
                            value={filters.category}
                            onChange={(e) => handleFilterChange('category', e.target.value)}
                        >
                            <option value="all">All Categories</option>
                            {jobCategories.map(category => (
                                <option key={category.value} value={category.value}>
                                    {category.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Priority Filter */}
                    <div className="filter-group">
                        <label htmlFor="priority" className="form-label">Priority</label>
                        <select
                            className="form-select"
                            id="priority"
                            value={filters.priority}
                            onChange={(e) => handleFilterChange('priority', e.target.value)}
                        >
                            <option value="all">All Priorities</option>
                            {jobPriorities.map(priority => (
                                <option key={priority.value} value={priority.value}>
                                    {priority.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Date Range Filter */}
                    <div className="filter-group">
                        <label htmlFor="dateRange" className="form-label">Date Range</label>
                        <select
                            className="form-select"
                            id="dateRange"
                            value={filters.dateRange}
                            onChange={(e) => handleFilterChange('dateRange', e.target.value)}
                        >
                            <option value="all">All Time</option>
                            <option value="today">Today</option>
                            <option value="week">This Week</option>
                            <option value="month">This Month</option>
                            <option value="quarter">This Quarter</option>
                            <option value="year">This Year</option>
                        </select>
                    </div>
                </div>
            )}

            {/* Active Filters Summary */}
            {hasActiveFilters && (
                <div className="job-filters-summary">
                    <small className="text-muted">
                        Active filters:
                        {filters.status !== 'all' && <span className="badge bg-primary me-1">{filters.status}</span>}
                        {filters.category !== 'all' && <span className="badge bg-info me-1">{filters.category}</span>}
                        {filters.priority !== 'all' && <span className="badge bg-warning me-1">{filters.priority}</span>}
                        {filters.dateRange !== 'all' && <span className="badge bg-success me-1">{filters.dateRange}</span>}
                        {filters.search && <span className="badge bg-secondary me-1">Search: "{filters.search}"</span>}
                    </small>
                </div>
            )}
        </div>
    );
};
