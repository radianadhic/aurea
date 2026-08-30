/**
 * Authentication Pinia store.
 * Manages current user, login, logout, role checks.
 */
import { defineStore } from 'pinia';
import { useApi } from '~/composables/useApi';

export interface User {
  id: string;
  username: string;
  email: string;
  fullName: string;
  employeeId?: string;
  branchId?: string;
  branchName?: string;
  roles: string[];
  permissions: string[];
  avatarUrl?: string;
  lastLoginAt?: string;
}

interface AuthState {
  user: User | null;
  loading: boolean;
  initialized: boolean;
  loginError: string | null;
  mfaRequired: boolean;
  mfaMethod: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    loading: false,
    initialized: false,
    loginError: null,
    mfaRequired: false,
    mfaMethod: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    isAdmin: (state) => state.user?.roles?.includes('SUPER_ADMIN') || false,
    isSteward: (state) => state.user?.roles?.includes('STEWARD_CIF') || false,
    isAnalyst: (state) => state.user?.roles?.includes('ANALYST') || false,
    isCompliance: (state) => state.user?.roles?.includes('COMPLIANCE') || false,
    fullName: (state) => state.user?.fullName || 'Guest',
    initials: (state) => {
      if (!state.user?.fullName) return '?';
      const parts = state.user.fullName.trim().split(/\s+/);
      if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    },
  },

  actions: {
    hasRole(role: string): boolean {
      return this.user?.roles?.includes(role) || false;
    },

    hasAnyRole(...roles: string[]): boolean {
      return roles.some((role) => this.hasRole(role));
    },

    hasAllRoles(...roles: string[]): boolean {
      return roles.every((role) => this.hasRole(role));
    },

    hasPermission(permission: string): boolean {
      return this.user?.permissions?.includes(permission) || false;
    },

    /**
     * Restore user from localStorage on app start.
     */
    async restoreFromStorage() {
      const api = useApi();
      const token = api.getAccessToken();
      if (!token) {
        this.initialized = true;
        return;
      }

      try {
        // Validate token and get user info
        await this.fetchCurrentUser();
      } catch (e) {
        console.error('Failed to restore auth:', e);
        api.logout();
      } finally {
        this.initialized = true;
      }
    },

    /**
     * Fetch current user from /auth/me endpoint.
     */
    async fetchCurrentUser(): Promise<User> {
      const api = useApi();
      const user = await api.get<User>('/api/v1/auth/me');
      this.user = user;
      if (process.client) {
        localStorage.setItem('user', JSON.stringify(user));
      }
      return user;
    },

    /**
     * Login with username/password.
     */
    async login(username: string, password: string, mfaCode?: string) {
      this.loading = true;
      this.loginError = null;

      try {
        const api = useApi();
        const response: any = await api.post('/api/v1/auth/login', {
          username,
          password,
          mfaCode,
        });

        if (response.mfaRequired) {
          this.mfaRequired = true;
          this.mfaMethod = response.mfaMethod;
          return { mfaRequired: true, mfaMethod: response.mfaMethod };
        }

        api.setTokens(response.accessToken, response.refreshToken);
        this.user = response.user;
        if (process.client) {
          localStorage.setItem('user', JSON.stringify(response.user));
        }

        return { success: true, user: response.user };
      } catch (e: any) {
        this.loginError = e.response?.data?.message || e.message || 'Login failed';
        throw e;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Logout - clear tokens and user state.
     */
    async logout() {
      const api = useApi();
      try {
        await api.post('/api/v1/auth/logout');
      } catch (e) {
        // Ignore logout API errors
      } finally {
        this.clearUser();
        api.clearTokens();
        if (process.client) {
          window.location.href = '/auth/login';
        }
      }
    },

    /**
     * Clear user state (used by API client on 401).
     */
    clearUser() {
      this.user = null;
      if (process.client) {
        localStorage.removeItem('user');
      }
    },

    /**
     * Update user profile fields.
     */
    updateUser(fields: Partial<User>) {
      if (this.user) {
        this.user = { ...this.user, ...fields };
        if (process.client) {
          localStorage.setItem('user', JSON.stringify(this.user));
        }
      }
    },
  },
});
