/**
 * Main entry point for MDM Admin Dashboard.
 * Initializes Alpine.js, HTMX, and the app.
 */
import Alpine from 'alpinejs';
import persist from '@alpinejs/persist';
import focus from '@alpinejs/focus';
import htmx from 'htmx.org';

import auth from './auth.js';
import api from './api.js';
import ws from './websocket.js';
import utils from './utils.js';

// Register Alpine plugins
Alpine.plugin(persist);
Alpine.plugin(focus);

// Make HTMX available globally
window.htmx = htmx;

// Make Alpine available globally
window.Alpine = Alpine;

// ============================================================
// ALPINE STORES
// ============================================================

// App store - sidebar, navigation, etc.
Alpine.store('app', {
  sidebarOpen: false,
  desktop: window.innerWidth >= 1024,
  pageTitle: 'Dashboard',
  breadcrumb: 'Home',

  init() {
    window.addEventListener('resize', () => {
      this.desktop = window.innerWidth >= 1024;
    });
  },

  toggleSidebar() {
    this.sidebarOpen = !this.sidebarOpen;
  },

  setPage(title, breadcrumb) {
    this.pageTitle = title;
    this.breadcrumb = breadcrumb;
  },
});

// Toast notifications
Alpine.store('toast', {
  items: [],

  show(message, type = 'info', duration = 3000) {
    const id = Date.now() + Math.random();
    this.items.push({ id, message, type });
    setTimeout(() => this.remove(id), duration);
  },

  remove(id) {
    this.items = this.items.filter((i) => i.id !== id);
  },
});

// ============================================================
// ALPINE COMPONENTS
// ============================================================

// Main app data
Alpine.data('appData', () => ({
  initialized: false,
  authenticated: false,
  user: {
    id: null,
    username: '',
    fullName: '',
    email: '',
    branchId: '',
    roles: [],
    initials: '?',
  },
  ws: {
    connected: false,
  },

  async init() {
    // Wait for Alpine to be fully ready
    await new Promise((r) => setTimeout(r, 100));

    // Check if on login page
    if (window.location.pathname.includes('/login')) {
      this.initialized = true;
      this.authenticated = !!auth.getAccessToken();
      if (this.authenticated) {
        // Already logged in - redirect to dashboard
        window.location.href = '/pages/dashboard.html';
      }
      return;
    }

    // Check authentication
    if (!auth.isAuthenticated()) {
      window.location.href = '/pages/login.html';
      return;
    }

    this.user = auth.getUser() || this.user;
    this.user.initials = utils.getInitials(this.user.fullName);
    this.authenticated = true;
    this.initialized = true;

    // Connect WebSocket
    try {
      ws.connect();
      if (ws.client && ws.client.onConnect) {
        ws.client.onConnect = () => {
          this.ws.connected = true;
        };
      }
    } catch (e) {
      console.warn('WebSocket connection failed:', e);
    }

    // Listen for connection status
    window.addEventListener('ws:connected', () => {
      this.ws.connected = true;
    });
    window.addEventListener('ws:disconnected', () => {
      this.ws.connected = false;
    });

    // Toast events
    window.addEventListener('toast:show', (e) => {
      this.$store.toast.show(e.detail.message, e.detail.type, e.detail.duration);
    });

    // Listen for WebSocket events (real-time updates)
    this.subscribeToRealtime();
  },

  async logout() {
    await auth.logout();
  },

  subscribeToRealtime() {
    // Subscribe to customer events
    ws.subscribe('/topic/customers', (data) => {
      console.log('Customer event:', data);
      // Refresh customer list if on that page
      window.dispatchEvent(new CustomEvent('customer:updated', { detail: data }));
    });

    // Subscribe to audit events
    ws.subscribe('/topic/audit', (data) => {
      console.log('Audit event:', data);
      window.dispatchEvent(new CustomEvent('audit:new', { detail: data }));
    });

    // Subscribe to alerts
    ws.subscribe('/topic/alerts', (data) => {
      console.log('Alert:', data);
      utils.toast(`Alert: ${data.message || 'New alert'}`, 'warning', 5000);
    });
  },
}));

// Login page component
Alpine.data('loginForm', () => ({
  username: '',
  password: '',
  mfaCode: '',
  mfaRequired: false,
  mfaMethod: null,
  loading: false,
  error: null,

  async submit() {
    this.loading = true;
    this.error = null;
    try {
      const result = await auth.login(this.username, this.password, this.mfaCode);
      if (result.mfaRequired) {
        this.mfaRequired = true;
        this.mfaMethod = result.mfaMethod;
        utils.toast('MFA code required', 'info');
      } else {
        utils.toast('Login successful', 'success');
        setTimeout(() => {
          window.location.href = '/pages/dashboard.html';
        }, 500);
      }
    } catch (err) {
      this.error = err.message || 'Login failed';
      utils.toast(this.error, 'error');
    } finally {
      this.loading = false;
    }
  },
}));

// Stat card component
Alpine.data('statCard', (config) => ({
  value: config.value || 0,
  label: config.label || '',
  trend: config.trend || null,
  trendValue: config.trendValue || null,
  icon: config.icon || null,
  color: config.color || 'primary',
  loading: false,

  init() {
    if (config.endpoint) this.load();
  },

  async load() {
    this.loading = true;
    try {
      const data = await api.get(config.endpoint);
      this.value = data.value;
      this.trend = data.trend;
      this.trendValue = data.trendValue;
    } catch (e) {
      console.error('Failed to load stat:', e);
    } finally {
      this.loading = false;
    }
  },
}));

// Data table component
Alpine.data('dataTable', (config) => ({
  data: [],
  loading: false,
  page: 0,
  size: config.size || 20,
  totalElements: 0,
  totalPages: 0,
  sortField: config.sortField || 'id',
  sortDirection: config.sortDirection || 'ASC',
  search: '',
  filters: config.filters || {},

  async load() {
    this.loading = true;
    try {
      const params = new URLSearchParams({
        page: this.page,
        size: this.size,
        sort: this.sortField,
        direction: this.sortDirection,
        ...(this.search ? { q: this.search } : {}),
        ...this.filters,
      });
      const response = await api.get(`${config.endpoint}?${params}`);
      this.data = response.content || [];
      this.totalElements = response.totalElements || 0;
      this.totalPages = response.totalPages || 0;
    } catch (e) {
      console.error('Failed to load data:', e);
      utils.toast('Failed to load data', 'error');
    } finally {
      this.loading = false;
    }
  },

  sortBy(field) {
    if (this.sortField === field) {
      this.sortDirection = this.sortDirection === 'ASC' ? 'DESC' : 'ASC';
    } else {
      this.sortField = field;
      this.sortDirection = 'ASC';
    }
    this.page = 0;
    this.load();
  },

  nextPage() {
    if (this.page < this.totalPages - 1) {
      this.page++;
      this.load();
    }
  },

  prevPage() {
    if (this.page > 0) {
      this.page--;
      this.load();
    }
  },

  onSearch() {
    this.page = 0;
    this.load();
  },
}));

// Start Alpine
Alpine.start();

console.log('MDM Admin Dashboard initialized');
console.log('Build:', import.meta.env.MODE);
console.log('API:', import.meta.env.VITE_API_GATEWAY_URL);
