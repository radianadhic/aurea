/**
 * AUREA SPA — Dashboard Page
 * Overview of all AI engines + system health
 */

const DashboardPage = {
  route: 'dashboard',
  title: 'Dashboard',
  subtitle: 'Real-time overview of AUREA platform',

  async render(container) {
    container.innerHTML = `
      <div class="page">
        <div class="page-header">
          <div>
            <h1 class="page-title">Welcome back, Admin 👋</h1>
            <p class="page-subtitle">Here's what's happening across AUREA right now</p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary" id="refreshAllBtn">↻ Refresh All</button>
            <button class="btn btn-primary" id="exportBtn">📥 Export Report</button>
          </div>
        </div>

        <!-- Top stats -->
        <div class="stat-grid" id="topStats">
          ${Components.skeleton(4)}
        </div>

        <!-- AI Modules Overview -->
        <h2 style="font-size: 16px; font-weight: 700; margin: 32px 0 16px; color: var(--text);">
          🧠 AI Intelligence Engines
        </h2>
        <div class="stat-grid" id="aiStats">
          ${Components.skeleton(4)}
        </div>

        <!-- Two-column section: Recent Activity + System Health -->
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 16px; margin-top: 24px;" class="dashboard-grid">
          <div class="card">
            <div class="card-header">
              <div>
                <h3 class="card-title">🚨 Top Critical Alerts</h3>
                <p class="card-subtitle">From insights, churn, and fraud engines</p>
              </div>
              <a href="#/insights" class="filter-chip">View All</a>
            </div>
            <div id="recentAlerts">${Components.skeleton(5)}</div>
          </div>

          <div class="card">
            <div class="card-header">
              <h3 class="card-title">💚 System Health</h3>
            </div>
            <div id="systemHealth">${Components.skeleton(4)}</div>
          </div>
        </div>

        <!-- Quick actions -->
        <h2 style="font-size: 16px; font-weight: 700; margin: 32px 0 16px; color: var(--text);">
          ⚡ Quick Actions
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px;">
          <a href="#/insights" class="card" style="text-align: center; text-decoration: none;">
            <div style="font-size: 32px; margin-bottom: 8px;">🧠</div>
            <div style="font-weight: 600;">View Insights</div>
            <div style="font-size: 12px; color: var(--text-muted);">Anomaly detection</div>
          </a>
          <a href="#/segmentation" class="card" style="text-align: center; text-decoration: none;">
            <div style="font-size: 32px; margin-bottom: 8px;">🎯</div>
            <div style="font-weight: 600;">Segments</div>
            <div style="font-size: 12px; color: var(--text-muted);">RFM analysis</div>
          </a>
          <a href="#/churn" class="card" style="text-align: center; text-decoration: none;">
            <div style="font-size: 32px; margin-bottom: 8px;">🚨</div>
            <div style="font-weight: 600;">Churn Watch</div>
            <div style="font-size: 12px; color: var(--text-muted);">At-risk customers</div>
          </a>
          <a href="#/fraud" class="card" style="text-align: center; text-decoration: none;">
            <div style="font-size: 32px; margin-bottom: 8px;">🛡️</div>
            <div style="font-weight: 600;">Fraud Detection</div>
            <div style="font-size: 12px; color: var(--text-muted);">Real-time scoring</div>
          </a>
        </div>
      </div>
    `;

    // Setup button handlers
    document.getElementById('refreshAllBtn').onclick = () => this.render(container);
    document.getElementById('exportBtn').onclick = () => Components.toast('Report exported!', 'success');

    // Mobile responsive grid
    const style = document.createElement('style');
    style.textContent = `@media (max-width: 968px) { .dashboard-grid { grid-template-columns: 1fr !important; } }`;
    document.head.appendChild(style);

    // Load data in parallel
    await this.loadData();
  },

  async loadData() {
    try {
      const [insights, seg, churn, fraud, health] = await Promise.all([
        window.api.getInsightsSummary().catch(() => null),
        window.api.getSegmentsSummary().catch(() => null),
        window.api.getChurnSummary().catch(() => null),
        window.api.getFraudSummary().catch(() => null),
        window.api.getHealth().catch(() => null),
      ]);

      this.renderTopStats(insights, seg, churn, fraud);
      this.renderAIStats(insights, seg, churn, fraud);
      this.renderRecentAlerts(insights, churn, fraud);
      this.renderSystemHealth(health);
    } catch (err) {
      Components.handleError(err, 'Dashboard');
    }
  },

  renderTopStats(insights, seg, churn, fraud) {
    const totalAlerts = (insights?.total_insights || 0) + (churn?.summary?.total_alerts || 0) + (fraud?.summary?.total_flagged || 0);
    const totalCustomers = seg?.summary?.total_customers || 0;
    const totalCLV = (seg?.summary?.total_predicted_clv_12m || 0) + (churn?.summary?.total_clv_at_risk || 0);
    const totalAtRisk = (fraud?.summary?.total_amount_at_risk || 0);

    document.getElementById('topStats').innerHTML = `
      <div class="stat-card danger">
        <div class="stat-label">🚨 Total Alerts</div>
        <div class="stat-value red">${totalAlerts}</div>
        <div class="stat-sub">Across 3 AI engines</div>
      </div>
      <div class="stat-card info">
        <div class="stat-label">👥 Customers</div>
        <div class="stat-value">${Components.formatNumber(totalCustomers)}</div>
        <div class="stat-sub">Active in segmentation</div>
      </div>
      <div class="stat-card success">
        <div class="stat-label">💰 Total CLV</div>
        <div class="stat-value green">${Components.formatCurrency(totalCLV)}</div>
        <div class="stat-sub">12-month projected</div>
      </div>
      <div class="stat-card warning">
        <div class="stat-label">⚠️ At Risk (Fraud)</div>
        <div class="stat-value yellow">${Components.formatCurrency(totalAtRisk)}</div>
        <div class="stat-sub">Pending review</div>
      </div>
    `;
  },

  renderAIStats(insights, seg, churn, fraud) {
    document.getElementById('aiStats').innerHTML = `
      <div class="card" style="border-left: 4px solid var(--gold);">
        <div style="font-size: 11px; color: var(--gold-dark); font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">🧠 Auto-Insights</div>
        <div style="font-size: 28px; font-weight: 700; font-family: 'Georgia', serif;">${insights?.total_insights || 0}</div>
        <div style="font-size: 12px; color: var(--text-muted);">
          ${insights?.by_severity?.CRITICAL || 0} critical · ${insights?.by_severity?.WARNING || 0} warning
        </div>
      </div>
      <div class="card" style="border-left: 4px solid var(--info);">
        <div style="font-size: 11px; color: var(--info); font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">🎯 Segmentation</div>
        <div style="font-size: 28px; font-weight: 700; font-family: 'Georgia', serif;">${seg?.summary?.segment_count || 0}</div>
        <div style="font-size: 12px; color: var(--text-muted);">
          ${seg?.summary?.champions || 0} champions · ${seg?.summary?.at_risk || 0} at risk
        </div>
      </div>
      <div class="card" style="border-left: 4px solid var(--warning);">
        <div style="font-size: 11px; color: var(--warning); font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">🚨 Churn Watch</div>
        <div style="font-size: 28px; font-weight: 700; font-family: 'Georgia', serif;">${churn?.summary?.total_alerts || 0}</div>
        <div style="font-size: 12px; color: var(--text-muted);">
          ${churn?.summary?.by_level?.Critical || 0} critical · ${Components.formatCurrency(churn?.summary?.total_clv_at_risk || 0)}
        </div>
      </div>
      <div class="card" style="border-left: 4px solid var(--danger);">
        <div style="font-size: 11px; color: var(--danger); font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">🛡️ Fraud Detection</div>
        <div style="font-size: 28px; font-weight: 700; font-family: 'Georgia', serif;">${fraud?.summary?.total_flagged || 0}</div>
        <div style="font-size: 12px; color: var(--text-muted);">
          ${fraud?.summary?.fraud_rate_pct || 0}% rate · ${Components.formatCurrency(fraud?.summary?.total_amount_at_risk || 0)}
        </div>
      </div>
    `;
  },

  renderRecentAlerts(insights, churn, fraud) {
    const all = [];
    if (insights?.top_critical) {
      insights.top_critical.forEach(i => all.push({
        type: 'insight',
        title: i.title,
        desc: i.metric,
        severity: 'CRITICAL',
        score: i.deviation_pct,
        time: 'recent',
      }));
    }
    if (churn?.top_at_risk) {
      churn.top_at_risk.forEach(c => all.push({
        type: 'churn',
        title: c.name,
        desc: `CLV at risk: ${Components.formatCurrency(c.clv_at_risk)}`,
        severity: c.level,
        score: c.churn_probability * 100,
        time: c.days_since_purchase + 'd inactive',
      }));
    }
    if (fraud?.top_risky_customers) {
      fraud.top_risky_customers.forEach(c => all.push({
        type: 'fraud',
        title: c.customer_id,
        desc: `${c.alert_count} alerts · ${Components.formatCurrency(c.total_at_risk)}`,
        severity: 'CRITICAL',
        score: c.max_risk,
        time: 'live',
      }));
    }

    if (all.length === 0) {
      document.getElementById('recentAlerts').innerHTML = Components.emptyState({
        icon: '✨', title: 'All clear!', desc: 'No critical alerts at the moment.'
      });
      return;
    }

    document.getElementById('recentAlerts').innerHTML = all.slice(0, 6).map(a => `
      <div style="display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--border);">
        <div style="font-size: 20px;">${
          a.type === 'insight' ? '🧠' : a.type === 'churn' ? '🚨' : '🛡️'
        }</div>
        <div style="flex: 1; min-width: 0;">
          <div style="font-weight: 600; font-size: 13px; color: var(--text);">${a.title}</div>
          <div style="font-size: 12px; color: var(--text-muted);">${a.desc}</div>
        </div>
        <div style="text-align: right;">
          ${Components.severityBadge(a.severity)}
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">${a.time}</div>
        </div>
      </div>
    `).join('');
  },

  renderSystemHealth(health) {
    if (!health) {
      document.getElementById('systemHealth').innerHTML = Components.emptyState({
        icon: '⚠️', title: 'Cannot reach ML service', desc: 'Check connection to port 8000'
      });
      return;
    }
    const modules = health.modules || [];
    document.getElementById('systemHealth').innerHTML = `
      <div style="display: flex; align-items: center; gap: 8px; padding: 8px 0;">
        <span class="status-dot status-up"></span>
        <span style="font-size: 13px;">ML Service</span>
        <span style="margin-left: auto; font-size: 11px; color: var(--success); font-family: 'JetBrains Mono', monospace;">v${health.version || '4.0'}</span>
      </div>
      <div style="display: flex; align-items: center; gap: 8px; padding: 8px 0;">
        <span class="status-dot status-up"></span>
        <span style="font-size: 13px;">API Endpoints</span>
        <span style="margin-left: auto; font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">50+ ready</span>
      </div>
      <div style="padding: 8px 0;">
        <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">AI Modules</div>
        ${modules.map(m => `
          <div style="display: flex; align-items: center; gap: 8px; padding: 4px 0; font-size: 12px;">
            <span style="color: var(--success);">●</span>
            <span>${m}</span>
          </div>
        `).join('')}
      </div>
    `;
  },

  unmount() {}
};

window.DashboardPage = DashboardPage;
