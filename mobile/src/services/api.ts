import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Change this to your Render URL
const API_URL = 'https://ai-travel-assistant-api.onrender.com/api';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

// Request interceptor to add token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('userToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;