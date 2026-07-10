/**
 * Central place for API calls, grouped by resource. Keeps components free
 * of raw axios calls / URL strings.
 */
import apiClient from './client';

export const authApi = {
  login: (data) => apiClient.post('/api/auth/login-json', data),
  register: (data) => apiClient.post('/api/auth/register', data),
  me: () => apiClient.get('/api/me'),
};

export const doctorApi = {
  list: (params) => apiClient.get('/api/doctors', { params }),
  get: (id) => apiClient.get(`/api/doctors/${id}`),
  create: (data) => apiClient.post('/api/doctor', data),
  update: (id, data) => apiClient.put(`/api/doctor/${id}`, data),
  remove: (id) => apiClient.delete(`/api/doctor/${id}`),
};

export const interactionApi = {
  list: (params) => apiClient.get('/api/interaction', { params }),
  create: (data) => apiClient.post('/api/interaction', data),
  update: (id, data) => apiClient.put(`/api/interaction/${id}`, data),
  remove: (id) => apiClient.delete(`/api/interaction/${id}`),
};

export const chatApi = {
  send: (data) => apiClient.post('/api/chat', data),
};

export const dashboardApi = {
  get: () => apiClient.get('/api/dashboard'),
  analytics: () => apiClient.get('/api/analytics'),
};

export const notificationApi = {
  list: () => apiClient.get('/api/notifications'),
  markRead: (id) => apiClient.put(`/api/notifications/${id}/read`),
};
