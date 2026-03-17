import api from '../../../utils/api';

export const jobsService = {
    // Get all jobs with optional filters
    getAll: async (filters = {}) => {
        const params = new URLSearchParams();
        
        if (filters.status && filters.status !== 'all') {
            params.append('status', filters.status);
        }
        if (filters.category && filters.category !== 'all') {
            params.append('category', filters.category);
        }
        if (filters.dateRange && filters.dateRange !== 'all') {
            params.append('dateRange', filters.dateRange);
        }
        if (filters.search) {
            params.append('search', filters.search);
        }

        const response = await api.get(`/api/jobs?${params.toString()}`);
        return response.data;
    },

    // Get job by ID
    getById: async (id) => {
        const response = await api.get(`/api/jobs/${id}`);
        return response.data;
    },

    // Create new job
    create: async (jobData) => {
        const response = await api.post('/api/jobs', jobData);
        return response.data;
    },

    // Update job
    update: async (id, jobData) => {
        const response = await api.put(`/api/jobs/${id}`, jobData);
        return response.data;
    },

    // Delete job
    delete: async (id) => {
        await api.delete(`/api/jobs/${id}`);
    },

    // Update job status
    updateStatus: async (id, status) => {
        const response = await api.patch(`/api/jobs/${id}/status`, { status });
        return response.data;
    },

    // Get job statistics
    getStats: async () => {
        const response = await api.get('/api/jobs/stats');
        return response.data;
    },

    // Get job categories
    getCategories: async () => {
        const response = await api.get('/api/jobs/categories');
        return response.data;
    },

    // Upload job documents
    uploadDocument: async (jobId, formData) => {
        const response = await api.post(`/api/jobs/${jobId}/documents`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    // Get job documents
    getDocuments: async (jobId) => {
        const response = await api.get(`/api/jobs/${jobId}/documents`);
        return response.data;
    },

    // Delete job document
    deleteDocument: async (jobId, documentId) => {
        await api.delete(`/api/jobs/${jobId}/documents/${documentId}`);
    },

    // Assign worker to job
    assignWorker: async (jobId, workerId) => {
        const response = await api.post(`/api/jobs/${jobId}/workers`, { workerId });
        return response.data;
    },

    // Remove worker from job
    removeWorker: async (jobId, workerId) => {
        await api.delete(`/api/jobs/${jobId}/workers/${workerId}`);
    },

    // Get job timeline/activities
    getTimeline: async (jobId) => {
        const response = await api.get(`/api/jobs/${jobId}/timeline`);
        return response.data;
    },

    // Add job activity to timeline
    addActivity: async (jobId, activity) => {
        const response = await api.post(`/api/jobs/${jobId}/timeline`, activity);
        return response.data;
    }
};
