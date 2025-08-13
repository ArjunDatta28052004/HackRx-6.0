import api from './authService';

export const documentService = {
  async uploadFile(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'File upload failed');
    }
  },

  async getDocuments() {
    try {
      const response = await api.get('/documents');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fetch documents');
    }
  },

  async buildIndex() {
    try {
      const response = await api.post('/build_index');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to build index');
    }
  },
};