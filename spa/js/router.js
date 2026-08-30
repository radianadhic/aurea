/**
 * AUREA SPA — Hash-based Router
 */

class Router {
  constructor() {
    this.routes = new Map();
    this.currentPage = null;
    window.addEventListener('hashchange', () => this.handleRoute());
  }

  register(name, page) {
    this.routes.set(name, page);
  }

  start() {
    this.handleRoute();
  }

  handleRoute() {
    const hash = window.location.hash || '#/dashboard';
    const route = hash.replace('#/', '').split('/')[0] || 'dashboard';
    const page = this.routes.get(route) || this.routes.get('dashboard');

    // Unmount previous
    if (this.currentPage && this.currentPage.unmount) {
      this.currentPage.unmount();
    }

    // Update page title
    document.getElementById('pageTitle').textContent = page.title || 'Dashboard';
    document.getElementById('pageSubtitle').textContent = page.subtitle || '';

    // Update active nav
    document.querySelectorAll('.nav-item').forEach(item => {
      item.classList.toggle('active', item.dataset.route === route);
    });

    // Render page
    const content = document.getElementById('content');
    this.currentPage = page;
    page.render(content);

    // Close mobile sidebar
    if (window.innerWidth <= 968) {
      document.getElementById('sidebar').classList.remove('open');
      document.getElementById('sidebarBackdrop').classList.remove('open');
    }
  }
}

window.router = new Router();
window.router.register('dashboard', window.DashboardPage);
window.router.register('insights', window.InsightsPage);
window.router.register('segmentation', window.SegmentationPage);
window.router.register('churn', window.ChurnPage);
window.router.register('fraud', window.FraudPage);
window.router.register('customers', window.CustomersPage);
window.router.register('health', window.HealthPage);
window.router.register('settings', window.SettingsPage);
window.router.register('monitoring', window.HealthPage);   // alias
window.router.register('config', window.SettingsPage);     // alias
window.router.register('reports', window.DashboardPage);   // placeholder
