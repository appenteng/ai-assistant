import api from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const authService = {
  async register(email: string, username: string, password: string, fullName?: string) {
    const response = await api.post('/auth/register', {
      email,
      username,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  async login(username: string, password: string) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.access_token) {
      await AsyncStorage.setItem('userToken', response.data.access_token);
    }

    return response.data;
  },

  async logout() {
    await AsyncStorage.removeItem('userToken');
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me');
    return response.data;
  },

  async isLoggedIn(): Promise<boolean> {
    const token = await AsyncStorage.getItem('userToken');
    return !!token;
  },
};