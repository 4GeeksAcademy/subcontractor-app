import { format, parseISO, isValid } from 'date-fns';

// Date formatting utilities
export const formatDate = (dateString, formatString = 'MMM dd, yyyy') => {
    try {
        const date = parseISO(dateString);
        return isValid(date) ? format(date, formatString) : 'Invalid date';
    } catch {
        return 'Invalid date';
    }
};

export const formatDateTime = (dateString) => {
    return formatDate(dateString, 'MMM dd, yyyy HH:mm');
};

export const formatRelativeTime = (dateString) => {
    try {
        const date = parseISO(dateString);
        const now = new Date();
        const diffInMs = now - date;
        const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
        const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
        const diffInMinutes = Math.floor(diffInMs / (1000 * 60));

        if (diffInDays > 0) {
            return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`;
        } else if (diffInHours > 0) {
            return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;
        } else if (diffInMinutes > 0) {
            return `${diffInMinutes} minute${diffInMinutes > 1 ? 's' : ''} ago`;
        } else {
            return 'Just now';
        }
    } catch {
        return 'Unknown time';
    }
};

// Currency formatting utilities
export const formatCurrency = (amount, currency = 'USD') => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
};

export const formatCurrencyCompact = (amount) => {
    if (amount >= 1000000) {
        return `$${(amount / 1000000).toFixed(1)}M`;
    } else if (amount >= 1000) {
        return `$${(amount / 1000).toFixed(1)}K`;
    }
    return `$${amount}`;
};

// Job status utilities
export const getStatusColor = (status) => {
    const colors = {
        pending: '#6c757d',
        in_progress: '#17a2b8',
        completed: '#28a745',
        cancelled: '#dc3545',
        on_hold: '#ffc107'
    };
    return colors[status] || '#6c757d';
};

export const getStatusIcon = (status) => {
    const icons = {
        pending: 'bi-clock-history',
        in_progress: 'bi-arrow-repeat',
        completed: 'bi-check-circle',
        cancelled: 'bi-x-circle',
        on_hold: 'bi-pause-circle'
    };
    return icons[status] || 'bi-question-circle';
};

export const getStatusLabel = (status) => {
    const labels = {
        pending: 'Pending',
        in_progress: 'In Progress',
        completed: 'Completed',
        cancelled: 'Cancelled',
        on_hold: 'On Hold'
    };
    return labels[status] || status;
};

// Priority utilities
export const getPriorityColor = (priority) => {
    const colors = {
        low: '#28a745',
        medium: '#ffc107',
        high: '#fd7e14',
        urgent: '#dc3545'
    };
    return colors[priority] || '#ffc107';
};

export const getPriorityLabel = (priority) => {
    const labels = {
        low: 'Low',
        medium: 'Medium',
        high: 'High',
        urgent: 'Urgent'
    };
    return labels[priority] || priority;
};

// Job validation utilities
export const validateJobForm = (formData) => {
    const errors = {};

    // Title validation
    if (!formData.title?.trim()) {
        errors.title = 'Title is required';
    } else if (formData.title.length < 3) {
        errors.title = 'Title must be at least 3 characters';
    } else if (formData.title.length > 100) {
        errors.title = 'Title must be less than 100 characters';
    }

    // Description validation
    if (!formData.description?.trim()) {
        errors.description = 'Description is required';
    } else if (formData.description.length < 10) {
        errors.description = 'Description must be at least 10 characters';
    } else if (formData.description.length > 1000) {
        errors.description = 'Description must be less than 1000 characters';
    }

    // Location validation
    if (!formData.location?.trim()) {
        errors.location = 'Location is required';
    } else if (formData.location.length < 5) {
        errors.location = 'Location must be at least 5 characters';
    }

    // Budget validation
    if (!formData.budget) {
        errors.budget = 'Budget is required';
    } else if (parseFloat(formData.budget) <= 0) {
        errors.budget = 'Budget must be greater than 0';
    } else if (parseFloat(formData.budget) > 1000000) {
        errors.budget = 'Budget must be less than $1,000,000';
    }

    // Start date validation
    if (!formData.startDate) {
        errors.startDate = 'Start date is required';
    } else {
        const startDate = new Date(formData.startDate);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        if (startDate < today) {
            errors.startDate = 'Start date cannot be in the past';
        }
    }

    // End date validation
    if (formData.endDate && formData.startDate) {
        const startDate = new Date(formData.startDate);
        const endDate = new Date(formData.endDate);
        if (endDate <= startDate) {
            errors.endDate = 'End date must be after start date';
        }
    }

    // Customer validation
    if (!formData.customerId) {
        errors.customerId = 'Customer is required';
    }

    return errors;
};

// Job search utilities
export const searchJobs = (jobs, searchTerm) => {
    if (!searchTerm) return jobs;

    const term = searchTerm.toLowerCase();
    return jobs.filter(job => 
        job.title?.toLowerCase().includes(term) ||
        job.description?.toLowerCase().includes(term) ||
        job.location?.toLowerCase().includes(term) ||
        job.customer?.name?.toLowerCase().includes(term) ||
        job.categories?.some(cat => cat.toLowerCase().includes(term))
    );
};

// Job filtering utilities
export const filterJobs = (jobs, filters) => {
    let filteredJobs = [...jobs];

    // Status filter
    if (filters.status && filters.status !== 'all') {
        filteredJobs = filteredJobs.filter(job => job.status === filters.status);
    }

    // Category filter
    if (filters.category && filters.category !== 'all') {
        filteredJobs = filteredJobs.filter(job => 
            job.categories?.includes(filters.category)
        );
    }

    // Priority filter
    if (filters.priority && filters.priority !== 'all') {
        filteredJobs = filteredJobs.filter(job => job.priority === filters.priority);
    }

    // Date range filter
    if (filters.dateRange && filters.dateRange !== 'all') {
        const now = new Date();
        let startDate;

        switch (filters.dateRange) {
            case 'today':
                startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
                break;
            case 'week':
                startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7);
                break;
            case 'month':
                startDate = new Date(now.getFullYear(), now.getMonth(), 1);
                break;
            case 'quarter':
                const quarter = Math.floor(now.getMonth() / 3);
                startDate = new Date(now.getFullYear(), quarter * 3, 1);
                break;
            case 'year':
                startDate = new Date(now.getFullYear(), 0, 1);
                break;
            default:
                break;
        }

        if (startDate) {
            filteredJobs = filteredJobs.filter(job => 
                new Date(job.startDate) >= startDate
            );
        }
    }

    // Search filter
    if (filters.search) {
        filteredJobs = searchJobs(filteredJobs, filters.search);
    }

    return filteredJobs;
};

// Job sorting utilities
export const sortJobs = (jobs, sortBy) => {
    const sortedJobs = [...jobs];

    switch (sortBy) {
        case 'created_asc':
            return sortedJobs.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
        case 'created_desc':
            return sortedJobs.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        case 'title_asc':
            return sortedJobs.sort((a, b) => a.title.localeCompare(b.title));
        case 'title_desc':
            return sortedJobs.sort((a, b) => b.title.localeCompare(a.title));
        case 'budget_asc':
            return sortedJobs.sort((a, b) => a.budget - b.budget);
        case 'budget_desc':
            return sortedJobs.sort((a, b) => b.budget - a.budget);
        case 'start_date_asc':
            return sortedJobs.sort((a, b) => new Date(a.startDate) - new Date(b.startDate));
        case 'start_date_desc':
            return sortedJobs.sort((a, b) => new Date(b.startDate) - new Date(a.startDate));
        case 'priority_asc':
            const priorityOrder = { low: 1, medium: 2, high: 3, urgent: 4 };
            return sortedJobs.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
        case 'priority_desc':
            const priorityOrderDesc = { low: 4, medium: 3, high: 2, urgent: 1 };
            return sortedJobs.sort((a, b) => priorityOrderDesc[a.priority] - priorityOrderDesc[b.priority]);
        default:
            return sortedJobs;
    }
};

// Job statistics utilities
export const calculateJobStats = (jobs) => {
    const stats = {
        total: jobs.length,
        pending: 0,
        inProgress: 0,
        completed: 0,
        cancelled: 0,
        onHold: 0,
        totalBudget: 0,
        averageBudget: 0,
        highPriorityCount: 0,
        overdueCount: 0
    };

    jobs.forEach(job => {
        // Status counts
        switch (job.status) {
            case 'pending':
                stats.pending++;
                break;
            case 'in_progress':
                stats.inProgress++;
                break;
            case 'completed':
                stats.completed++;
                break;
            case 'cancelled':
                stats.cancelled++;
                break;
            case 'on_hold':
                stats.onHold++;
                break;
        }

        // Budget calculations
        if (job.budget) {
            stats.totalBudget += parseFloat(job.budget);
        }

        // Priority counts
        if (job.priority === 'high' || job.priority === 'urgent') {
            stats.highPriorityCount++;
        }

        // Overdue check
        if (job.status === 'in_progress' && job.endDate) {
            const endDate = new Date(job.endDate);
            const today = new Date();
            if (endDate < today) {
                stats.overdueCount++;
            }
        }
    });

    stats.averageBudget = stats.total > 0 ? stats.totalBudget / stats.total : 0;

    return stats;
};

// File size formatting utilities
export const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Generate unique ID
export const generateJobId = () => {
    return `job_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

// Export utilities
export const exportJobsToCSV = (jobs) => {
    const headers = ['ID', 'Title', 'Status', 'Priority', 'Budget', 'Start Date', 'Customer', 'Location'];
    const csvContent = [
        headers.join(','),
        ...jobs.map(job => [
            job.id,
            `"${job.title}"`,
            job.status,
            job.priority,
            job.budget,
            job.startDate,
            `"${job.customer?.name || ''}"`,
            `"${job.location}"`
        ].join(','))
    ].join('\n');

    return csvContent;
};

export const downloadCSV = (csvContent, filename = 'jobs.csv') => {
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
};
