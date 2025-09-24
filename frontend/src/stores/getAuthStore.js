import { create } from 'zustand';
import axios from 'axios';
import toast from 'react-hot-toast';

const API_URL = 'http://localhost:5000/api/auth';

export const useAuthStore = create((set, get) => ({
  user: null,
  loading: false,
  error: null,

  register: async (userData) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${API_URL}/register`, userData);
      set({ user: response.data.user, loading: false });
      toast.success('Account created successfully!');
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Registration failed';
      set({ error: errorMessage, loading: false });
      toast.error(errorMessage);
      return { success: false };
    }
  },

  login: async (credentials) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${API_URL}/login`, credentials);
      localStorage.setItem('token', response.data.token);
      set({ user: response.data.user, loading: false });
      toast.success('Logged in successfully!');
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Login failed';
      set({ error: errorMessage, loading: false });
      toast.error(errorMessage);
      return { success: false };
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    set({ user: null });
    toast.success('Logged out successfully');
  },

  clearError: () => set({ error: null }),

  checkAuth: async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await axios.get(`${API_URL}/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      set({ user: response.data.user });
    } catch (error) {
      localStorage.removeItem('token');
      set({ user: null });
    }
  }
}));
