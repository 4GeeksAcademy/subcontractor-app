import React, { useState } from 'react';
import { JobCard } from './JobCard';
import './JobList.css';

export const JobList = ({ jobs, loading, error, onUpdate, onDelete }) => {
    const [viewMode, setViewMode] = useState('grid'); // grid or list

    if (loading) {
        return (
            <div className="job-list-loading">
                <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="job-list-error">
                <div className="alert alert-danger" role="alert">
                    {error}
                </div>
            </div>
        );
    }

    if (!jobs || jobs.length === 0) {
        return (
            <div className="job-list-empty">
                <div className="empty-state-icon">
                    <i className="bi bi-briefcase"></i>
                </div>
                <h3>No jobs found</h3>
                <p>Start by creating your first job or adjust your filters.</p>
            </div>
        );
    }

    return (
        <div className="job-list">
            <div className="job-list-header">
                <div className="job-list-info">
                    <h3>Jobs ({jobs.length})</h3>
                </div>
                <div className="job-list-controls">
                    <div className="btn-group" role="group">
                        <button
                            type="button"
                            className={`btn ${viewMode === 'grid' ? 'btn-primary' : 'btn-outline-primary'}`}
                            onClick={() => setViewMode('grid')}
                        >
                            <i className="bi bi-grid-3x3-gap"></i>
                        </button>
                        <button
                            type="button"
                            className={`btn ${viewMode === 'list' ? 'btn-primary' : 'btn-outline-primary'}`}
                            onClick={() => setViewMode('list')}
                        >
                            <i className="bi bi-list-ul"></i>
                        </button>
                    </div>
                </div>
            </div>
            
            <div className={`job-list-content ${viewMode}`}>
                {jobs.map(job => (
                    <JobCard
                        key={job.id}
                        job={job}
                        viewMode={viewMode}
                        onUpdate={onUpdate}
                        onDelete={onDelete}
                    />
                ))}
            </div>
        </div>
    );
};
