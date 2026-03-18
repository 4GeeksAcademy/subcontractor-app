import axios from 'axios';

// Create axios instance with default configuration
const api = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:3001',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token') || localStorage.getItem('provider');

        console.log(localStorage.getItem('provider'));
console.log(localStorage.getItem('token'));

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
    
);


api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('provider');
            localStorage.removeItem('name');
            window.location.href = '/loginprovider';
        }
        return Promise.reject(error);
    }
);

export default api;
