/**
 * Auth Pinia store template.
 * Copy this file to your project's stores folder.
 */
import { defineStore } from 'pinia';

export interface User {
  id: string;
  username: string;
  email: string;
  fullName: string;
  roles: string[];
  permissions: string[];
}

interface AuthState {
  user: User | null;
  loading: boolean;
  initialized: boolean;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    loading: false,
    initialized: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    isAdmin: (state) => state.user?.roles.includes('ADMIN') || false,
  },

  actions: {
    hasRole(role: string) {
      return this.user?.roles.includes(role) || false;
    },

    hasPermission(permission: string) {
      return this.user?.permissions.includes(permission) || false;
    },

    async login(username: string, password: string) {
      this.loading = true;
      try {
        // Your API call here
        // const response = await $fetch('/api/v1/auth/login', {
        //   method: 'POST',
        //   body: { username, password },
        // });
        // this.user = response.user;
        // localStorage.setItem('user', JSON.stringify(response.user));
      } finally {
        this.loading = false;
      }
    },

    async logout() {
      this.user = null;
      localStorage.removeItem('user');
    },

    async restoreFromStorage() {
      const stored = localStorage.getItem('user');
      if (stored) {
        try {
          this.user = JSON.parse(stored);
        } catch (e) {
          localStorage.removeItem('user');
        }
      }
      this.initialized = true;
    },
  },
});
