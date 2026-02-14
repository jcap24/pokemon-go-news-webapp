import axios from 'axios';

// Base API URL - change this to your backend URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// News API calls
export const newsAPI = {
  getAll: async (params = {}) => {
    try {
      const response = await api.get('/api/news', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getById: async (id) => {
    try {
      const response = await api.get(`/api/news/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getSources: async () => {
    try {
      const response = await api.get('/api/news/sources');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Events API calls
export const eventsAPI = {
  getAll: async (params = {}) => {
    try {
      const response = await api.get('/api/events', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getById: async (id) => {
    try {
      const response = await api.get(`/api/events/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getCalendar: async (month, year) => {
    try {
      const response = await api.get('/api/events/calendar', {
        params: { month, year },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getTypes: async () => {
    try {
      const response = await api.get('/api/events/types');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Raids API calls
export const raidsAPI = {
  getAll: async (params = {}) => {
    try {
      const response = await api.get('/api/raids', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getCounters: async (bossName, params = {}) => {
    try {
      const response = await api.get(`/api/raids/${bossName}/counters`, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  search: async (query) => {
    try {
      const response = await api.get('/api/raids/search', { params: { q: query } });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getTiers: async () => {
    try {
      const response = await api.get('/api/raids/tiers');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  refreshData: async () => {
    try {
      const response = await api.post('/api/raids/refresh');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Assistant API calls
export const assistantAPI = {
  ask: async (question, conversationHistory = null) => {
    try {
      const response = await api.post('/api/assistant/ask', {
        question,
        conversation_history: conversationHistory,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getSuggestions: async () => {
    try {
      const response = await api.get('/api/assistant/suggestions');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getEventRecommendations: async (preferences) => {
    try {
      const response = await api.post('/api/assistant/recommend-events', preferences);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  healthCheck: async () => {
    try {
      const response = await api.get('/api/assistant/health');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Admin API calls
export const adminAPI = {
  triggerScrape: async () => {
    try {
      const response = await api.post('/api/scrape');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  healthCheck: async () => {
    try {
      const response = await api.get('/api/health');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default api;
