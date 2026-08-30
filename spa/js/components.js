/**
 * AUREA SPA — Common Components
 * Reusable UI building blocks
 */

const Components = {
  // ============ Toast notifications ============
  toast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };
    toast.innerHTML = `<span>${icons[type] || 'ℹ'}</span><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.classList.add('fade-out');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },

  // ============ Modal ============
  modal({ title, body, footer, size = 'md' }) {
    // Remove existing
    const existing = document.querySelector('.modal-backdrop');
    if (existing) existing.remove();

    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop open';
    backdrop.innerHTML = `
      <div class="modal" style="max-width: ${size === 'lg' ? '1100px' : size === 'sm' ? '500px' : '800px'}">
        <div class="modal-header">
          <h3 class="modal-title font-georgia" style="font-size: 20px; font-weight: 700;">${title}</h3>
          <button class="modal-close">×</button>
        </div>
        <div class="modal-body">${body}</div>
        ${footer ? `<div class="modal-footer">${footer}</div>` : ''}
      </div>
    `;
    document.body.appendChild(backdrop);

    const close = () => backdrop.remove();
    backdrop.querySelector('.modal-close').onclick = close;
    backdrop.onclick = (e) => { if (e.target === backdrop) close(); };
    return { element: backdrop, close };
  },

  // ============ Loading state ============
  loading(show) {
    document.getElementById('loadingOverlay').classList.toggle('open', show);
  },

  // ============ Formatters ============
  formatCurrency(n) {
    if (n === null || n === undefined) return 'Rp 0';
    if (Math.abs(n) >= 1e9) return `Rp ${(n/1e9).toFixed(2)}B`;
    if (Math.abs(n) >= 1e6) return `Rp ${(n/1e6).toFixed(1)}M`;
    if (Math.abs(n) >= 1e3) return `Rp ${(n/1e3).toFixed(0)}K`;
    return `Rp ${n.toFixed(0)}`;
  },
  formatNumber(n) {
    if (n === null || n === undefined) return '0';
    if (Math.abs(n) >= 1_000_000) return `${(n/1_000_000).toFixed(1)}M`;
    if (Math.abs(n) >= 1_000) return `${(n/1_000).toFixed(0)}K`;
    return (n || 0).toLocaleString('id-ID');
  },
  formatPercent(n, decimals = 1) {
    if (n === null || n === undefined) return '0%';
    return `${(n * 100).toFixed(decimals)}%`;
  },
  formatTime(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    const now = new Date();
    const diff = (now - d) / 1000;
    if (diff < 60) return 'just now';
    if (diff < 3600) return `${Math.floor(diff/60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff/3600)}h ago`;
    return d.toLocaleDateString('id-ID', { day: 'numeric', month: 'short' });
  },

  // ============ Risk level helpers ============
  riskClass(score) {
    if (score < 40) return 'risk-low';
    if (score < 60) return 'risk-medium';
    if (score < 80) return 'risk-high';
    return 'risk-critical';
  },
  severityBadge(severity) {
    return `<span class="badge badge-${severity.toLowerCase()}">${severity}</span>`;
  },
  riskLevelBadge(level) {
    const map = {
      CRITICAL: 'badge-critical',
      ALERT: 'badge-warning',
      WARNING: 'badge-warning',
      WATCH: 'badge-warning',
      INFO: 'badge-info',
      LOST: 'badge-critical',
      SAFE: 'badge-success',
    };
    return `<span class="badge ${map[level] || 'badge-info'}">${level}</span>`;
  },
  churnRiskBadge(risk) {
    if (risk < 0.2) return '<span class="badge badge-success">LOW</span>';
    if (risk < 0.45) return '<span class="badge badge-info">MEDIUM</span>';
    if (risk < 0.7) return '<span class="badge badge-warning">HIGH</span>';
    return '<span class="badge badge-critical">CRITICAL</span>';
  },

  // ============ Empty state ============
  emptyState({ icon = '📭', title = 'No data', desc = '' }) {
    return `
      <div class="empty-state">
        <div class="empty-state-icon">${icon}</div>
        <div class="empty-state-title">${title}</div>
        ${desc ? `<div class="empty-state-desc">${desc}</div>` : ''}
      </div>
    `;
  },

  // ============ Skeleton loaders ============
  skeleton(count = 3) {
    return Array(count).fill('<div class="skeleton" style="height: 60px; margin-bottom: 12px;"></div>').join('');
  },

  // ============ Error handler ============
  handleError(err, context = '') {
    console.error(`[${context}]`, err);
    this.toast(err.message || 'An error occurred', 'error', 5000);
  },
};

window.Components = Components;
