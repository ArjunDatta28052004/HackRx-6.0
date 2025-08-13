import api from './authService';

export const queryService = {
  async processQuery(query) {
    try {
      const response = await api.post('/process_query', { query });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Query processing failed');
    }
  },
};