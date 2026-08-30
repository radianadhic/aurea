/**
 * Authentication module - handles login, logout, and current user state.
 */
import api from './api.js';

const TOKEN_KEY = 'accessToken';
const REFRESH_KEY = 'refreshToken';
const USER_KEY = 'user';

export const auth = {
  /**
   * Get stored access token
   */
  getAccessToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  /**
   * Get stored refresh token
   */
  getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
  },

  /**
   * Get stored user info
   */
  getUser() {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  },

  /**
   * Save auth state
   */
  saveAuth(accessToken, refreshToken, user) {
    localStorage.setItem(TOKEN_KEY, accessToken);
    if (refreshToken) localStorage.setItem(REFRESH_KEY, refreshToken);
    if (user) localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return !!this.getAccessToken();
  },

  /**
   * Check if user has a specific role
   */
  hasRole(role) {
    const user = this.getUser();
    return user?.roles?.includes(role) || false;
  },

  /**
   * Check if user has any of the specified roles
   */
  hasAnyRole(...roles) {
    return roles.some((role) => this.hasRole(role));
  },

  /**
   * Login
   */
  async login(username, password, mfaCode) {
    const response = await api.login(username, password, mfaCode);
    if (response.mfaRequired) {
      return { mfaRequired: true, mfaMethod: response.mfaMethod };
    }
    this.saveAuth(response.accessToken, response.refreshToken, response.user);
    return { success: true, user: response.user };
  },

  /**
   * Logout
   */
  async logout() {
    try {
      await api.logoutSession();
    } catch (e) {
      console.warn('Logout API failed:', e);
    } finally {
      localStorage.clear();
      window.location.href = '/pages/login.html';
    }
  },

  /**
   * Refresh current user info from API
   */
  async refreshUser() {
    try {
      const user = await api.getCurrentUser();
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      return user;
    } catch (e) {
      console.error('Failed to refresh user:', e);
      this.logout();
      return null;
    }
  },
};

export default auth;
