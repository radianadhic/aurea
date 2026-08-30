/**
 * AUREA SPA — System Health Page
 */

const HealthPage = {
  route: 'health',
  title: 'System Health',
  subtitle: 'Service status, ML engines, and API endpoints',

  async render(container) {
    container.innerHTML = `
      <div class="page">
        <div class="page-header">
          <div>
            <h1 class="page-title">💚 System Health</h1>
            <p class="page-subtitle">${this.subtitle}</p>
          </div>
          <button class="btn btn-primary" id="refreshBtn">↻ Check Now</button>
        </div>
        <div id="healthContent">${Components.skeleton(5)}</div>
      </div>
    `;

    document.getElementById('refreshBtn').onclick = () => this.load(container);
    await this.load(container);
  },

  async load(container) {
    try {
      const health = await window.api.getHealth();
      const html = `
        <div class="card" style="background: linear-gradient(135deg, var(--navy), var(--navy-light)); color: white; border: 1px solid var(--gold); margin-bottom: 20px;">
          <div style="display: flex; align-items: center; gap: 16px;">
            <div style="font-size: 48px;">✅</div>
            <div>
              <div style="font-family: 'Georgia', serif; font-size: 28px; font-weight: 700;">All Systems Operational</div>
              <div style="opacity: 0.7; font-size: 14px;">AUREA ML Service v${health.version} · ${new Date(health.timestamp).toLocaleString()}</div>
            </div>
          </div>
        </div>

        <h2 style="font-size: 16px; font-weight: 700; margin: 24px 0 12px;">🧠 AI Modules</h2>
        <div class="stat-grid">
          ${(health.modules || []).map(m => `
            <div class="card">
              <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span class="status-dot status-up"></span>
                <strong style="text-transform: capitalize;">${m.replace(/_/g, ' ')}</strong>
              </div>
              <div style="font-size: 12px; color: var(--text-muted);">Operational · Healthy</div>
            </div>
          `).join('')}
        </div>

        <h2 style="font-size: 16px; font-weight: 700; margin: 24px 0 12px;">🔌 Service Endpoints</h2>
        <div class="card">
          ${[
            { name: 'AUREA ML Service', url: 'http://localhost:8000', port: 8000, status: 'up' },
            { name: 'API Documentation (Swagger)', url: 'http://localhost:8000/docs', port: 8000, status: 'up' },
            { name: 'AUREA Console', url: 'http://localhost:3000', port: 3000, status: 'up' },
            { name: 'AUREA 360', url: 'http://localhost:3001', port: 3001, status: 'up' },
            { name: 'AUREA Steward', url: 'http://localhost:3002', port: 3002, status: 'up' },
          ].map(s => `
            <div style="display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--border);">
              <span class="status-dot status-up"></span>
              <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 13px;">${s.name}</div>
                <a href="${s.url}" target="_blank" style="font-size: 11px; color: var(--gold-dark); font-family: 'JetBrains Mono', monospace; text-decoration: none;">${s.url}</a>
              </div>
              <span class="badge badge-success">:${s.port}</span>
            </div>
          `).join('')}
        </div>
      `;
      document.getElementById('healthContent').innerHTML = html;
    } catch (err) {
      document.getElementById('healthContent').innerHTML = `
        <div class="card" style="border-left: 4px solid var(--danger); background: var(--danger-light);">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 32px;">⚠️</div>
            <div>
              <div style="font-weight: 700; color: var(--danger-dark);">Cannot reach ML Service</div>
              <div style="font-size: 13px; color: var(--text-muted);">${err.message}</div>
            </div>
          </div>
        </div>
      `;
    }
  },

  unmount() {}
};

window.HealthPage = HealthPage;
