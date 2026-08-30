/**
 * Centralized API client for Steward UI.
 * Handles auth, refresh, error handling, and logging.
 */
import axios, { AxiosError, type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios';
import { useAuthStore } from '~/stores/auth';
import { useNotificationStore } from '~/stores/notification';

const TOKEN_KEY = 'accessToken';
const REFRESH_KEY = 'refreshToken';

class ApiClient {
  private instance: AxiosInstance;
  private refreshing: Promise<string> | null = null;

  constructor() {
    const config = useRuntimeConfig();

    this.instance = axios.create({
      baseURL: config.public.apiGatewayUrl,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor - add auth token
    this.instance.interceptors.request.use(
      (config) => {
        const token = this.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle errors and refresh
    this.instance.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

        // 401 - try refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const newToken = await this.refreshAccessToken();
            originalRequest.headers = { ...originalRequest.headers, Authorization: `Bearer ${newToken}` };
            return this.instance(originalRequest);
          } catch (refreshError) {
            this.logout();
            throw refreshError;
          }
        }

        // Show error notification
        if (error.response?.status !== 401) {
          const notificationStore = useNotificationStore();
          const message = this.extractErrorMessage(error);
          notificationStore.showError(message);
        }

        return Promise.reject(error);
      }
    );
  }

  private extractErrorMessage(error: AxiosError): string {
    if (error.response?.data) {
      const data = error.response.data as any;
      return data.message || data.error || error.message;
    }
    return error.message || 'Unknown error';
  }

  // Token management
  getAccessToken(): string | null {
    if (process.server) return null;
    return localStorage.getItem(TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    if (process.server) return null;
    return localStorage.getItem(REFRESH_KEY);
  }

  setTokens(accessToken: string, refreshToken?: string) {
    if (process.server) return;
    localStorage.setItem(TOKEN_KEY, accessToken);
    if (refreshToken) localStorage.setItem(REFRESH_KEY, refreshToken);
  }

  clearTokens() {
    if (process.server) return;
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
  }

  private async refreshAccessToken(): Promise<string> {
    if (this.refreshing) return this.refreshing;

    this.refreshing = (async () => {
      const refreshToken = this.getRefreshToken();
      if (!refreshToken) throw new Error('No refresh token');

      const response = await axios.post(
        `${useRuntimeConfig().public.apiGatewayUrl}/api/v1/auth/refresh`,
        { refreshToken },
        { headers: { 'Content-Type': 'application/json' } }
      );

      const { accessToken, refreshToken: newRefresh } = response.data;
      this.setTokens(accessToken, newRefresh);
      return accessToken;
    })();

    try {
      return await this.refreshing;
    } finally {
      this.refreshing = null;
    }
  }

  logout() {
    this.clearTokens();
    const authStore = useAuthStore();
    authStore.clearUser();
    if (process.client) {
      window.location.href = '/auth/login';
    }
  }

  // HTTP methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.get(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.post(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.put(url, data, config);
    return response.data;
  }

  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.patch(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.delete(url, config);
    return response.data;
  }

  // Paginated endpoints
  async getPage<T>(url: string, params?: Record<string, any>): Promise<PageResponse<T>> {
    return this.get<PageResponse<T>>(url, { params });
  }
}

// Singleton
let _client: ApiClient | null = null;

export function useApi(): ApiClient {
  if (!_client) {
    _client = new ApiClient();
  }
  return _client;
}

// Page response interface
export interface PageResponse<T> {
  content: T[];
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
  first: boolean;
  last: boolean;
  numberOfElements: number;
  empty: boolean;
}
