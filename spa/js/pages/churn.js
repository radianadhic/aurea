/**
 * AUREA SPA — Churn Watch List Page
 */

const ChurnPage = {
  route: 'churn',
  title: 'Churn Watch List',
  subtitle: 'Real-time monitoring of at-risk customers',

  state: { summary: null, alerts: [], levelFilter: 'ALL' },

  async render(container) {
    container.innerHTML = `
      <div class="page">
        <div class="page-header">
          <div>
            <h1 class="page-title">🚨 Churn Watch List</h1>
            <p class="page-subtitle">${this.subtitle}</p>
          </div>
          <button class="btn btn-primary" id="refreshBtn">↻ Refresh</button>
        </div>

        <div class="stat-grid" id="churnStats">${Components.skeleton(5)}</div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin: 20px 0 12px;">
          <button class="filter-chip active" data-level="ALL">All</button>
          <button class="filter-chip" data-level="Critical">🔴 Critical</button>
          <button class="filter-chip" data-level="Alert">🟠 Alert</button>
          <button class="filter-chip" data-level="Watch">🟡 Watch</button>
          <button class="filter-chip" data-level="Lost">⚫ Lost</button>
        </div>

        <div class="card" style="padding: 0; overflow: hidden;">
          <div id="churnList" style="padding: 8px;">${Components.skeleton(5)}</div>
        </div>
      </div>
    `;

    document.getElementById('refreshBtn').onclick = () => this.loadData();
    container.querySelectorAll('[data-level]').forEach(btn => {
      btn.onclick = () => {
        container.querySelectorAll('[data-level]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.state.levelFilter = btn.dataset.level;
        this.renderList();
      };
    });

    await this.loadData();
  },

  async loadData() {
    try {
      Components.loading(true);
      const [summary, alerts] = await Promise.all([
        window.api.getChurnSummary(),
        window.api.getChurnAlerts({ limit: 200 }),
      ]);
      this.state.summary = summary;
      this.state.alerts = alerts.alerts || [];
      this.renderStats();
      this.renderList();
    } catch (err) {
      Components.handleError(err, 'Churn');
    } finally {
      Components.loading(false);
    }
  },

  renderStats() {
    const s = this.state.summary?.summary || {};
    const driverCount = Object.keys(this.state.summary?.driver_breakdown || {}).length;
    document.getElementById('churnStats').innerHTML = `
      <div class="stat-card danger">
        <div class="stat-label">🔴 Critical</div>
        <div class="stat-value red">${s.by_level?.Critical || 0}</div>
        <div class="stat-sub">URGENT</div>
      </div>
      <div class="stat-card warning">
        <div class="stat-label">🟠 Alert</div>
        <div class="stat-value yellow">${s.by_level?.Alert || 0}</div>
        <div class="stat-sub">action this week</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">🟡 Watch</div>
        <div class="stat-value">${s.by_level?.Watch || 0}</div>
        <div class="stat-sub">monitor</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">💰 CLV at Risk</div>
        <div class="stat-value gold">${Components.formatCurrency(s.total_clv_at_risk || 0)}</div>
      </div>
      <div class="stat-card success">
        <div class="stat-label">✅ Recovery (30d)</div>
        <div class="stat-value green">${Components.formatCurrency(s.recovery_this_month || 0)}</div>
        <div class="stat-sub">${(s.intervention_success_rate * 100 || 0).toFixed(0)}% success</div>
      </div>
    `;
  },

  renderList() {
    const filtered = this.state.alerts.filter(a =>
      this.state.levelFilter === 'ALL' || a.level === this.state.levelFilter
    );

    const list = document.getElementById('churnList');
    if (filtered.length === 0) {
      list.innerHTML = Components.emptyState({ icon: '✨', title: 'No alerts', desc: 'All clear!' });
      return;
    }

    list.innerHTML = filtered.slice(0, 50).map(a => `
      <div class="churn-row" data-id="${a.id}" style="padding: 14px; border-bottom: 1px solid var(--border); cursor: pointer; transition: background 0.15s;"
           onmouseover="this.style.background='var(--gray-50)'" onmouseout="this.style.background=''">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 100px;">
            <div style="font-weight: 700; font-size: 18px; font-family: 'Georgia', serif;">${a.risk_score}</div>
            <div class="risk-meter"><div class="risk-meter-fill ${Components.riskClass(a.risk_score)}" style="width: ${a.risk_score}%;"></div></div>
          </div>
          <div style="flex: 1;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
              ${Components.riskLevelBadge(a.level)}
              <span style="font-weight: 600; font-size: 14px;">${a.customer_name}</span>
              <span style="font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">${a.customer_id}</span>
            </div>
            <div style="font-size: 12px; color: var(--text-muted);">
              ${(a.drivers || []).slice(0, 2).map(d => `<span class="badge badge-gold" style="margin-right: 4px;">${d.driver}</span>`).join('')}
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">CLV at risk</div>
            <div style="font-weight: 700; color: var(--danger);">${Components.formatCurrency(a.clv_at_risk)}</div>
            <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">${a.days_since_purchase}d inactive</div>
          </div>
        </div>
      </div>
    `).join('');

    list.querySelectorAll('.churn-row').forEach(row => {
      row.onclick = () => this.showDetail(row.dataset.id);
    });
  },

  async showDetail(id) {
    const alert = this.state.alerts.find(a => a.id === id);
    if (!alert) return;
    const body = `
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 16px;">
        <div style="background: var(--danger-light); padding: 12px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--danger-dark); text-transform: uppercase;">Risk Score</div>
          <div style="font-size: 24px; font-weight: 700; color: var(--danger-dark);">${alert.risk_score}</div>
        </div>
        <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Churn Prob.</div>
          <div style="font-size: 24px; font-weight: 700;">${(alert.churn_probability * 100).toFixed(0)}%</div>
        </div>
        <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">CLV at Risk</div>
          <div style="font-size: 20px; font-weight: 700;">${Components.formatCurrency(alert.clv_at_risk)}</div>
        </div>
      </div>
      <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin: 16px 0 8px;">⚠️ Churn Drivers</h4>
      <div style="margin-bottom: 16px;">
        ${(alert.drivers || []).map(d => `
          <div style="background: var(--danger-light); padding: 10px 12px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid var(--danger);">
            <div style="font-weight: 600; font-size: 13px; color: var(--danger-dark);">${d.driver} <span style="font-weight: 400; color: var(--text-muted);">· severity ${d.severity}/10</span></div>
            <div style="font-size: 12px; color: var(--text-muted);">${d.description}</div>
          </div>
        `).join('')}
      </div>
      <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin: 16px 0 8px;">💡 Recommended Actions</h4>
      <ul style="list-style: none; padding: 0;">
        ${(alert.recommended_actions || []).map(r => `
          <li style="padding: 8px 12px; background: var(--gold-pale); border-radius: 6px; margin-bottom: 4px; font-size: 13px;">
            <span style="color: var(--gold-dark); margin-right: 6px;">▸</span>${r}
          </li>
        `).join('')}
      </ul>
    `;
    const footer = `
      <button class="btn btn-secondary" data-action="close">Close</button>
      <button class="btn btn-primary" data-action="intervene">📞 Create Intervention</button>
    `;
    const modal = Components.modal({ title: alert.customer_name, body, size: 'lg', footer });
    modal.element.querySelector('[data-action="close"]').onclick = () => modal.close();
    modal.element.querySelector('[data-action="intervene"]').onclick = () => this.createIntervention(alert);
  },

  async createIntervention(alert) {
    const message = prompt('Intervention message:', 'Personal outreach to retain this customer.');
    if (!message) return;
    try {
      await window.api.createChurnIntervention(alert.id, 'Phone Call', message, 'Admin');
      Components.toast('✓ Intervention scheduled', 'success');
      await this.loadData();
    } catch (e) { Components.handleError(e, 'Intervention'); }
  },

  unmount() {}
};

window.ChurnPage = ChurnPage;
