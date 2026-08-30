/**
 * API client for MDM Admin Dashboard.
 * Handles HTTP requests with auth, error handling, and CSRF.
 */

const API_BASE_URL =
  import.meta.env.VITE_API_GATEWAY_URL || 'http://localhost:8080';
const AUTH_SERVICE_URL =
  import.meta.env.VITE_AUTH_SERVICE_URL || 'http://localhost:8081';

class ApiClient {
  constructor() {
    this.accessToken = localStorage.getItem('accessToken');
    this.refreshToken = localStorage.getItem('refreshToken');
  }

  /**
   * Get auth header for requests
   */
  getAuthHeader() {
    return this.accessToken ? { Authorization: `Bearer ${this.accessToken}` } : {};
  }

  /**
   * Generic request method
   */
  async request(url, options = {}) {
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeader(),
        ...(options.headers || {}),
      },
    };

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }

    const response = await fetch(url, config);

    // Handle 401 (Unauthorized) - try to refresh token
    if (response.status === 401 && this.refreshToken) {
      const refreshed = await this.tryRefresh();
      if (refreshed) {
        // Retry original request
        config.headers = {
          ...config.headers,
          ...this.getAuthHeader(),
        };
        return fetch(url, config);
      } else {
        // Refresh failed - logout
        this.logout();
        throw new Error('Session expired');
      }
    }

    return response;
  }

  /**
   * GET request
   */
  async get(url, options = {}) {
    const response = await this.request(url, { ...options, method: 'GET' });
    return this.handleResponse(response);
  }

  /**
   * POST request
   */
  async post(url, body, options = {}) {
    const response = await this.request(url, {
      ...options,
      method: 'POST',
      body,
    });
    return this.handleResponse(response);
  }

  /**
   * PUT request
   */
  async put(url, body, options = {}) {
    const response = await this.request(url, {
      ...options,
      method: 'PUT',
      body,
    });
    return this.handleResponse(response);
  }

  /**
   * PATCH request
   */
  async patch(url, body, options = {}) {
    const response = await this.request(url, {
      ...options,
      method: 'PATCH',
      body,
    });
    return this.handleResponse(response);
  }

  /**
   * DELETE request
   */
  async delete(url, options = {}) {
    const response = await this.request(url, { ...options, method: 'DELETE' });
    return this.handleResponse(response);
  }

  /**
   * Handle response - check status, parse JSON
   */
  async handleResponse(response) {
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      const err = new Error(error.message || `HTTP ${response.status}`);
      err.status = response.status;
      err.code = error.code;
      err.details = error;
      throw err;
    }

    // 204 No Content
    if (response.status === 204) return null;

    return response.json();
  }

  /**
   * Try to refresh access token
   */
  async tryRefresh() {
    try {
      const response = await fetch(`${AUTH_SERVICE_URL}/api/v1/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refreshToken: this.refreshToken }),
      });

      if (!response.ok) return false;

      const data = await response.json();
      this.setTokens(data.accessToken, data.refreshToken);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Set tokens and persist
   */
  setTokens(accessToken, refreshToken) {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('accessToken', accessToken);
    if (refreshToken) localStorage.setItem('refreshToken', refreshToken);
  }

  /**
   * Clear tokens and logout
   */
  logout() {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    window.location.href = '/pages/login.html';
  }

  // ============================================================
  // AUTH
  // ============================================================
  async login(username, password, mfaCode = null) {
    const response = await fetch(`${AUTH_SERVICE_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, mfaCode }),
    });
    return this.handleResponse(response);
  }

  async logoutSession() {
    try {
      await this.post(`${AUTH_SERVICE_URL}/api/v1/auth/logout`);
    } finally {
      this.logout();
    }
  }

  async getCurrentUser() {
    return this.get(`${AUTH_SERVICE_URL}/api/v1/auth/me`);
  }

  // ============================================================
  // CUSTOMERS
  // ============================================================
  async searchCustomers(query, page = 0, size = 20) {
    return this.get(
      `${API_BASE_URL}/api/v1/customers/search?q=${encodeURIComponent(query)}&page=${page}&size=${size}`
    );
  }

  async getCustomer(id) {
    return this.get(`${API_BASE_URL}/api/v1/customers/${id}`);
  }

  async getCustomerByCif(cifNumber) {
    return this.get(`${API_BASE_URL}/api/v1/customers/cif/${cifNumber}`);
  }

  // ============================================================
  // MONITORING
  // ============================================================
  async getServicesHealth() {
    return this.get(`${API_BASE_URL}/actuator/health/services`);
  }

  async getMetrics() {
    return this.get(`${API_BASE_URL}/actuator/metrics`);
  }

  // ============================================================
  // REPORTS
  // ============================================================
  async getReports(page = 0, size = 20) {
    return this.get(
      `${API_BASE_URL}/api/v1/reports?page=${page}&size=${size}`
    );
  }

  async generateReport(reportId, parameters) {
    return this.post(`${API_BASE_URL}/api/v1/reports/${reportId}/generate`, parameters);
  }
}

export const api = new ApiClient();
export default api;
