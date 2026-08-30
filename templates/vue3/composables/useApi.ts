/**
 * useApi composable - HTTP client template.
 * Copy this file to your project's composables folder.
 */
import axios, { AxiosError, type AxiosInstance, type AxiosRequestConfig } from 'axios';

const TOKEN_KEY = 'accessToken';
const REFRESH_KEY = 'refreshToken';

interface ApiClientOptions {
  baseURL?: string;
  onUnauthorized?: () => void;
  onError?: (error: AxiosError) => void;
}

export function createApiClient(options: ApiClientOptions = {}) {
  const baseURL = options.baseURL || (typeof window !== 'undefined'
    ? (window as any).NUXT_API_GATEWAY_URL
    : process.env.NUXT_API_GATEWAY_URL) || 'http://localhost:8080';

  const instance = axios.create({
    baseURL,
    timeout: 30000,
    headers: { 'Content-Type': 'application/json' },
  });

  let refreshing: Promise<string> | null = null;

  // Request interceptor - add auth
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  // Response interceptor - handle 401, errors
  instance.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
      const original = error.config as AxiosRequestConfig & { _retry?: boolean };

      if (error.response?.status === 401 && !original._retry) {
        original._retry = true;
        try {
          const newToken = await refreshToken();
          original.headers = { ...original.headers, Authorization: `Bearer ${newToken}` };
          return instance(original);
        } catch (e) {
          options.onUnauthorized?.();
          throw e;
        }
      }

      options.onError?.(error);
      throw error;
    }
  );

  async function refreshToken(): Promise<string> {
    if (refreshing) return refreshing;
    refreshing = (async () => {
      const refreshToken = localStorage.getItem(REFRESH_KEY);
      if (!refreshToken) throw new Error('No refresh token');
      const response = await axios.post(`${baseURL}/api/v1/auth/refresh`, { refreshToken });
      const { accessToken, refreshToken: newRefresh } = response.data;
      localStorage.setItem(TOKEN_KEY, accessToken);
      if (newRefresh) localStorage.setItem(REFRESH_KEY, newRefresh);
      return accessToken;
    })();
    try {
      return await refreshing;
    } finally {
      refreshing = null;
    }
  }

  return {
    instance,
    get: <T>(url: string, config?: AxiosRequestConfig) =>
      instance.get<T>(url, config).then((r) => r.data),
    post: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
      instance.post<T>(url, data, config).then((r) => r.data),
    put: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
      instance.put<T>(url, data, config).then((r) => r.data),
    patch: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
      instance.patch<T>(url, data, config).then((r) => r.data),
    delete: <T>(url: string, config?: AxiosRequestConfig) =>
      instance.delete<T>(url, config).then((r) => r.data),
    setTokens: (access: string, refresh?: string) => {
      localStorage.setItem(TOKEN_KEY, access);
      if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
    },
    clearTokens: () => {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(REFRESH_KEY);
    },
  };
}

let _client: ReturnType<typeof createApiClient> | null = null;

export function useApi() {
  if (!_client) {
    _client = createApiClient();
  }
  return _client;
}

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
