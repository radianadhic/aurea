/**
 * AUREA SPA — App Bootstrap
 */

(function() {
  'use strict';

  // ============ Splash → Login Transition ============
  function showLogin() {
    document.getElementById('splash').classList.add('fade-out');
    setTimeout(() => {
      document.getElementById('splash').classList.add('hidden');
      document.getElementById('login').classList.remove('hidden');
    }, 500);
  }

  function showApp() {
    document.getElementById('login').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    document.getElementById('app').classList.add('fade-in');
    window.router.start();
  }

  // ============ Login Handler ============
  function setupLogin() {
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('loginEmail').value;
      const password = document.getElementById('loginPassword').value;

      Components.loading(true);
      setTimeout(() => {
        if (email && password) {
          window.store.setUser({
            email,
            name: email.split('@')[0],
            role: 'admin',
            loginAt: new Date().toISOString(),
          });
          Components.toast('Welcome to AUREA!', 'success');
          Components.loading(false);
          showApp();
        } else {
          Components.loading(false);
          Components.toast('Please fill all fields', 'error');
        }
      }, 600);
    });
  }

  // ============ Sidebar Toggle ============
  function setupSidebar() {
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    const toggle = document.getElementById('sidebarToggle');
    const close = document.getElementById('sidebarClose');

    const closeSidebar = () => {
      sidebar.classList.remove('open');
      backdrop.classList.remove('open');
    };

    if (toggle) toggle.onclick = () => {
      sidebar.classList.toggle('open');
      backdrop.classList.toggle('open');
    };
    if (close) close.onclick = closeSidebar;
    if (backdrop) backdrop.onclick = closeSidebar;
  }

  // ============ User Menu Dropdown ============
  function setupUserMenu() {
    const userMenu = document.getElementById('userMenu');
    const dropdown = document.getElementById('userDropdown');
    const logoutBtn = document.getElementById('logoutBtn');

    if (userMenu) {
      userMenu.onclick = (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('open');
      };
    }
    document.addEventListener('click', () => dropdown.classList.remove('open'));

    if (logoutBtn) {
      logoutBtn.onclick = (e) => {
        e.preventDefault();
        window.store.setUser(null);
        location.reload();
      };
    }
  }

  // ============ Topbar Actions ============
  function setupTopbar() {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
      themeToggle.textContent = window.store.state.theme === 'dark' ? '☀️' : '🌙';
      themeToggle.onclick = () => {
        window.store.toggleTheme();
        themeToggle.textContent = window.store.state.theme === 'dark' ? '☀️' : '🌙';
        Components.toast(`Theme: ${window.store.state.theme}`, 'info', 1500);
      };
    }

    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
      refreshBtn.onclick = () => {
        window.api.clearCache();
        if (window.router.currentPage && window.router.currentPage.loadData) {
          window.router.currentPage.loadData();
        }
        Components.toast('Refreshed', 'success', 1500);
      };
    }
  }

  // ============ WebSocket Status (simulated) ============
  function setupRealtime() {
    let connected = true;
    setInterval(() => {
      connected = Math.random() > 0.05; // 95% uptime
      const dot = document.getElementById('wsStatus');
      const text = document.getElementById('wsStatusText');
      if (dot && text) {
        dot.className = connected ? 'status-dot status-up' : 'status-dot status-down';
        text.textContent = connected ? 'Live' : 'Offline';
      }
    }, 10000);
  }

  // ============ Notification Count ============
  function updateNotifCount() {
    setInterval(async () => {
      try {
        const [churn, fraud, insights] = await Promise.all([
          window.api.getChurnSummary().catch(() => null),
          window.api.getFraudSummary().catch(() => null),
          window.api.getInsightsSummary().catch(() => null),
        ]);
        const count = (churn?.summary?.by_level?.Critical || 0) +
                      (fraud?.summary?.by_priority?.P1 || 0) +
                      (insights?.by_severity?.CRITICAL || 0);
        const el = document.getElementById('notifCount');
        if (el) {
          el.textContent = count;
          el.style.display = count > 0 ? 'flex' : 'none';
        }
      } catch (e) { /* ignore */ }
    }, 15000);
  }

  // ============ Boot ============
  function boot() {
    const existingUser = window.store.loadUser();

    // Always show splash first
    setTimeout(() => {
      if (existingUser) {
        showLogin();
        // Auto-submit login form for returning user
        setTimeout(() => {
          document.getElementById('loginForm').dispatchEvent(new Event('submit'));
        }, 300);
      } else {
        showLogin();
      }
    }, 1800);

    setupLogin();
    setupSidebar();
    setupUserMenu();
    setupTopbar();
    setupRealtime();
    updateNotifCount();
  }

  // Add fade-in style
  const style = document.createElement('style');
  style.textContent = '.fade-in { animation: fadeIn 0.3s ease; } @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }';
  document.head.appendChild(style);

  // Wait for DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
