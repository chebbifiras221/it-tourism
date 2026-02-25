import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '30000'),
  headers: {
    'Content-Type': 'application/json',
  }
});

export const analytics = {
  getOverview: () => apiClient.get('/api/analytics/overview'),
  getRegions: (limit = 20, sortBy = 'visitors') => 
    apiClient.get('/api/analytics/regions', { params: { limit, sort_by: sortBy } }),
  getTemporal: (period: string, days = 30, region?: string) =>
    apiClient.get(`/api/analytics/temporal/${period}`, { params: { days, region } }),
  getRegionDetails: (region: string) =>
    apiClient.get(`/api/analytics/regions/${region}`),
};

export const forecasts = {
  getForecast: (region: string, daysAhead = 30, model = 'prophet') =>
    apiClient.post('/api/forecasts/visitors', { region, days_ahead: daysAhead, model }),
  getSeasonality: (region: string, period = 'monthly') =>
    apiClient.get(`/api/forecasts/seasonality/${region}`, { params: { period } }),
  compareModels: (region: string, daysAhead = 30) =>
    apiClient.get(`/api/forecasts/comparison/${region}`, { params: { days_ahead: daysAhead } }),
  detectAnomalies: (region: string, sensitivity = 2.0) =>
    apiClient.get(`/api/forecasts/anomalies/${region}`, { params: { sensitivity } }),
};

export const sites = {
  listSites: (region?: string, ratingMin = 0, limit = 50, offset = 0) =>
    apiClient.get('/api/sites/', { params: { region, rating_min: ratingMin, limit, offset } }),
  getSiteDetails: (siteId: string) =>
    apiClient.get(`/api/sites/${siteId}`),
  getSimilarSites: (siteId: string, limit = 5) =>
    apiClient.get(`/api/sites/${siteId}/similar`, { params: { limit } }),
  getSitesByRegion: (region: string, sortBy = 'rating') =>
    apiClient.get(`/api/sites/by-region/${region}`, { params: { sort_by: sortBy } }),
  getTopRated: (limit = 10) =>
    apiClient.get('/api/sites/stats/top-rated', { params: { limit } }),
  getMostVisited: (limit = 10) =>
    apiClient.get('/api/sites/stats/most-visited', { params: { limit } }),
};

export const health = {
  check: () => apiClient.get('/api/health'),
  status: () => apiClient.get('/api/status'),
};

export const chatbot = {
  chat: (message: string) => apiClient.post('/api/chat', { message }),
  getSuggestions: () => apiClient.get('/api/chat/suggestions'),
  getExamples: () => apiClient.get('/api/chat/examples'),
};

export default apiClient;
