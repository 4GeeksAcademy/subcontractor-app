// Job Categories
export const jobCategories = [
    { value: 'residential', label: 'Residential' },
    { value: 'commercial', label: 'Commercial' },
    { value: 'industrial', label: 'Industrial' },
    { value: 'renovation', label: 'Renovation' },
    { value: 'new_construction', label: 'New Construction' },
    { value: 'remodeling', label: 'Remodeling' },
    { value: 'plumbing', label: 'Plumbing' },
    { value: 'electrical', label: 'Electrical' },
    { value: 'hvac', label: 'HVAC' },
    { value: 'roofing', label: 'Roofing' },
    { value: 'painting', label: 'Painting' },
    { value: 'flooring', label: 'Flooring' },
    { value: 'landscaping', label: 'Landscaping' },
    { value: 'concrete', label: 'Concrete' },
    { value: 'carpentry', label: 'Carpentry' }
];

// Job Priorities
export const jobPriorities = [
    { value: 'low', label: 'Low Priority', color: '#28a745' },
    { value: 'medium', label: 'Medium Priority', color: '#ffc107' },
    { value: 'high', label: 'High Priority', color: '#fd7e14' },
    { value: 'urgent', label: 'Urgent Priority', color: '#dc3545' }
];

// Job Statuses
export const jobStatuses = [
    { value: 'pending', label: 'Pending', color: '#6c757d', icon: 'bi-clock-history' },
    { value: 'in_progress', label: 'In Progress', color: '#17a2b8', icon: 'bi-arrow-repeat' },
    { value: 'completed', label: 'Completed', color: '#28a745', icon: 'bi-check-circle' },
    { value: 'cancelled', label: 'Cancelled', color: '#dc3545', icon: 'bi-x-circle' },
    { value: 'on_hold', label: 'On Hold', color: '#ffc107', icon: 'bi-pause-circle' }
];

// Default Job Form Values
export const defaultJobForm = {
    title: '',
    description: '',
    location: '',
    startDate: '',
    endDate: '',
    budget: '',
    priority: 'medium',
    status: 'pending',
    categories: [],
    customerId: '',
    notes: '',
    progress: 0
};

// Job Validation Rules
export const jobValidationRules = {
    title: {
        required: true,
        minLength: 3,
        maxLength: 100,
        message: 'Title must be between 3 and 100 characters'
    },
    description: {
        required: true,
        minLength: 10,
        maxLength: 1000,
        message: 'Description must be between 10 and 1000 characters'
    },
    location: {
        required: true,
        minLength: 5,
        maxLength: 200,
        message: 'Location must be between 5 and 200 characters'
    },
    budget: {
        required: true,
        min: 0,
        max: 1000000,
        message: 'Budget must be between $0 and $1,000,000'
    },
    startDate: {
        required: true,
        message: 'Start date is required'
    },
    customerId: {
        required: true,
        message: 'Customer is required'
    }
};

// Job Status Colors
export const jobStatusColors = {
    pending: '#6c757d',
    in_progress: '#17a2b8',
    completed: '#28a745',
    cancelled: '#dc3545',
    on_hold: '#ffc107'
};

// Job Priority Colors
export const jobPriorityColors = {
    low: '#28a745',
    medium: '#ffc107',
    high: '#fd7e14',
    urgent: '#dc3545'
};

// Job Status Icons
export const jobStatusIcons = {
    pending: 'bi-clock-history',
    in_progress: 'bi-arrow-repeat',
    completed: 'bi-check-circle',
    cancelled: 'bi-x-circle',
    on_hold: 'bi-pause-circle'
};

// Job Activity Types
export const jobActivityTypes = [
    { value: 'created', label: 'Created', icon: 'bi-plus-circle', color: '#28a745' },
    { value: 'updated', label: 'Updated', icon: 'bi-pencil', color: '#17a2b8' },
    { value: 'status_changed', label: 'Status Changed', icon: 'bi-arrow-repeat', color: '#ffc107' },
    { value: 'worker_assigned', label: 'Worker Assigned', icon: 'bi-person-plus', color: '#17a2b8' },
    { value: 'document_uploaded', label: 'Document Uploaded', icon: 'bi-file-earmark-plus', color: '#6f42c1' },
    { value: 'note_added', label: 'Note Added', icon: 'bi-chat-left-text', color: '#fd7e14' },
    { value: 'completed', label: 'Completed', icon: 'bi-check-circle', color: '#28a745' },
    { value: 'cancelled', label: 'Cancelled', icon: 'bi-x-circle', color: '#dc3545' }
];

// Job Sort Options
export const jobSortOptions = [
    { value: 'created_desc', label: 'Newest First' },
    { value: 'created_asc', label: 'Oldest First' },
    { value: 'title_asc', label: 'Title (A-Z)' },
    { value: 'title_desc', label: 'Title (Z-A)' },
    { value: 'budget_desc', label: 'Budget (High to Low)' },
    { value: 'budget_asc', label: 'Budget (Low to High)' },
    { value: 'start_date_asc', label: 'Start Date (Earliest)' },
    { value: 'start_date_desc', label: 'Start Date (Latest)' },
    { value: 'priority_desc', label: 'Priority (High to Low)' },
    { value: 'priority_asc', label: 'Priority (Low to High)' }
];

// Job Export Options
export const jobExportOptions = [
    { value: 'pdf', label: 'PDF Report', icon: 'bi-file-pdf' },
    { value: 'excel', label: 'Excel Spreadsheet', icon: 'bi-file-excel' },
    { value: 'csv', label: 'CSV File', icon: 'bi-file-csv' },
    { value: 'print', label: 'Print', icon: 'bi-printer' }
];

// Job Filter Presets
export const jobFilterPresets = [
    {
        name: 'My Active Jobs',
        filters: { status: 'in_progress', assignedTo: 'me' }
    },
    {
        name: 'Pending Approval',
        filters: { status: 'pending' }
    },
    {
        name: 'High Priority',
        filters: { priority: 'high' }
    },
    {
        name: 'This Week',
        filters: { dateRange: 'week' }
    },
    {
        name: 'Overdue',
        filters: { status: 'in_progress', overdue: true }
    }
];

// Job Permissions
export const jobPermissions = {
    create: 'job:create',
    read: 'job:read',
    update: 'job:update',
    delete: 'job:delete',
    assign_workers: 'job:assign_workers',
    upload_documents: 'job:upload_documents',
    view_timeline: 'job:view_timeline',
    change_status: 'job:change_status'
};
