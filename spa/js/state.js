/**
 * AUREA SPA — State Management
 * Simple pub/sub pattern
 */

class StateManager {
  constructor() {
    this.state = {
      user: null,
      authenticated: false,
      currentRoute: null,
      theme: localStorage.getItem('aurea-theme') || 'light',
      notifications: [],
      sidebarOpen: window.innerWidth > 968,
    };
    this.listeners = new Map();
  }

  get(key) {
    return key ? this.state[key] : this.state;
  }

  set(key, value) {
    const oldValue = this.state[key];
    this.state[key] = value;
    this.emit(key, value, oldValue);
    this.emit('*', this.state, null);
  }

  subscribe(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
    return () => {
      const arr = this.listeners.get(event);
      const idx = arr.indexOf(callback);
      if (idx > -1) arr.splice(idx, 1);
    };
  }

  emit(event, data, oldData) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(cb => {
        try { cb(data, oldData); } catch (e) { console.error(e); }
      });
    }
  }

  // Convenience methods
  setUser(user) {
    this.set('user', user);
    this.set('authenticated', !!user);
    if (user) {
      localStorage.setItem('aurea-user', JSON.stringify(user));
    } else {
      localStorage.removeItem('aurea-user');
    }
  }

  loadUser() {
    const stored = localStorage.getItem('aurea-user');
    if (stored) {
      try {
        const user = JSON.parse(stored);
        this.setUser(user);
        return user;
      } catch (e) {
        localStorage.removeItem('aurea-user');
      }
    }
    return null;
  }

  setTheme(theme) {
    this.set('theme', theme);
    localStorage.setItem('aurea-theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
  }

  toggleTheme() {
    this.setTheme(this.state.theme === 'light' ? 'dark' : 'light');
  }

  toggleSidebar() {
    this.set('sidebarOpen', !this.state.sidebarOpen);
  }
}

window.store = new StateManager();
window.store.setTheme(window.store.state.theme);
