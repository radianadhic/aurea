/**
 * AUREA SPA — Real-time Fraud Detection Page
 */

const FraudPage = {
  route: 'fraud',
  title: 'Fraud Detection',
  subtitle: 'Multi-layer transaction scoring & risk management',

  state: { summary: null, alerts: [], decisionFilter: 'ALL' },

  async render(container) {
    container.innerHTML = `
      <div class="page">
        <div class="page-header">
          <div>
            <h1 class="page-title">🛡️ Real-time Fraud Detection</h1>
            <p class="page-subtitle">${this.subtitle}</p>
          </div>
          <button class="btn btn-primary" id="refreshBtn">↻ Simulate</button>
        </div>

        <div class="stat-grid" id="fraudStats">${Components.skeleton(5)}</div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin: 20px 0 12px;">
          <button class="filter-chip active" data-decision="ALL">All</button>
          <button class="filter-chip" data-decision="Blocked">🔴 Blocked</button>
          <button class="filter-chip" data-decision="Manual Review">🟡 Review</button>
          <button class="filter-chip" data-decision="Approved">🟢 Approved</button>
        </div>

        <div class="card" style="padding: 0; overflow: hidden;">
          <div id="fraudList" style="padding: 8px;">${Components.skeleton(5)}</div>
        </div>
      </div>
    `;

    document.getElementById('refreshBtn').onclick = async () => {
      Components.loading(true);
      try {
        await window.api.refreshFraud();
        await this.loadData();
        Components.toast('Fraud simulation regenerated', 'success');
      } catch (e) { Components.handleError(e, 'Refresh'); }
      finally { Components.loading(false); }
    };

    container.querySelectorAll('[data-decision]').forEach(btn => {
      btn.onclick = () => {
        container.querySelectorAll('[data-decision]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.state.decisionFilter = btn.dataset.decision;
        this.renderList();
      };
    });

    await this.loadData();
  },

  async loadData() {
    try {
      Components.loading(true);
      const [summary, alerts] = await Promise.all([
        window.api.getFraudSummary(),
        window.api.getFraudAlerts({ limit: 100 }),
      ]);
      this.state.summary = summary;
      this.state.alerts = alerts.alerts || [];
      this.renderStats();
      this.renderList();
    } catch (err) {
      Components.handleError(err, 'Fraud');
    } finally {
      Components.loading(false);
    }
  },

  renderStats() {
    const s = this.state.summary?.summary || {};
    document.getElementById('fraudStats').innerHTML = `
      <div class="stat-card info">
        <div class="stat-label">📊 Scanned</div>
        <div class="stat-value">${s.total_scanned || 0}</div>
        <div class="stat-sub">transactions</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-label">🚨 Flagged</div>
        <div class="stat-value red">${s.total_flagged || 0}</div>
        <div class="stat-sub">${(s.fraud_rate_pct || 0).toFixed(1)}% rate</div>
      </div>
      <div class="stat-card success">
        <div class="stat-label">✓ Approved</div>
        <div class="stat-value green">${s.approved || 0}</div>
      </div>
      <div class="stat-card warning">
        <div class="stat-label">⏸ Review</div>
        <div class="stat-value yellow">${s.manual_review || 0}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">💰 At Risk</div>
        <div class="stat-value gold">${Components.formatCurrency(s.total_amount_at_risk || 0)}</div>
      </div>
    `;
  },

  renderList() {
    const filtered = this.state.alerts.filter(a =>
      this.state.decisionFilter === 'ALL' || a.decision === this.state.decisionFilter
    );
    const list = document.getElementById('fraudList');

    if (filtered.length === 0) {
      list.innerHTML = Components.emptyState({ icon: '✅', title: 'No flagged transactions', desc: 'All clear.' });
      return;
    }

    list.innerHTML = filtered.slice(0, 50).map(a => {
      const decClass = a.decision === 'Approved' ? 'badge-success' :
                       a.decision === 'Blocked' ? 'badge-critical' : 'badge-warning';
      return `
      <div class="fraud-row" data-id="${a.id}" style="padding: 14px; border-bottom: 1px solid var(--border); cursor: pointer; transition: background 0.15s;"
           onmouseover="this.style.background='var(--gray-50)'" onmouseout="this.style.background=''">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 80px;">
            <div style="font-weight: 700; font-size: 16px; font-family: 'Georgia', serif;">${a.risk_score.toFixed(0)}</div>
            <div class="risk-meter"><div class="risk-meter-fill ${Components.riskClass(a.risk_score)}" style="width: ${a.risk_score}%;"></div></div>
          </div>
          <div style="flex: 1;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
              <span class="badge ${decClass}">${a.decision}</span>
              <span class="badge badge-gold">${a.priority}</span>
              <span style="font-weight: 600; font-size: 13px;">${a.customer_id}</span>
              <span style="font-size: 11px; color: var(--text-muted);">·</span>
              <span style="font-size: 12px; color: var(--text-muted);">${a.pattern}</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">
              ${a.signals.length} signals · ${a.channel} · ${a.location}
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-weight: 700; color: var(--danger);">${Components.formatCurrency(a.amount)}</div>
          </div>
        </div>
      </div>
    `;
    }).join('');

    list.querySelectorAll('.fraud-row').forEach(row => {
      row.onclick = () => this.showDetail(row.dataset.id);
    });
  },

  showDetail(id) {
    const a = this.state.alerts.find(x => x.id === id);
    if (!a) return;
    const sorted = [...(a.signals || [])].sort((x, y) => (y.score * y.weight) - (x.score * x.weight));
    const body = `
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px; margin-bottom: 16px;">
        <div style="background: var(--danger-light); padding: 10px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--danger-dark); text-transform: uppercase;">Risk</div>
          <div style="font-size: 22px; font-weight: 700; color: var(--danger-dark);">${a.risk_score.toFixed(0)}</div>
        </div>
        <div style="background: var(--gray-50); padding: 10px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Amount</div>
          <div style="font-size: 18px; font-weight: 700;">${Components.formatCurrency(a.amount)}</div>
        </div>
        <div style="background: var(--gray-50); padding: 10px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Channel</div>
          <div style="font-size: 14px; font-weight: 600;">${a.channel}</div>
        </div>
        <div style="background: var(--gray-50); padding: 10px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Location</div>
          <div style="font-size: 14px; font-weight: 600;">${a.location}</div>
        </div>
      </div>
      <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin: 16px 0 8px;">🎯 ${a.signals.length} Risk Signals</h4>
      <div style="max-height: 300px; overflow-y: auto;">
        ${sorted.map(s => `
          <div style="display: flex; align-items: center; gap: 8px; padding: 8px 10px; background: var(--danger-light); border-radius: 6px; margin-bottom: 4px; border-left: 3px solid var(--danger);">
            <div style="text-align: center; min-width: 36px;">
              <div style="font-size: 18px; font-weight: 700; color: var(--danger-dark);">${s.score}</div>
              <div style="font-size: 8px; color: var(--text-muted); text-transform: uppercase;">score</div>
            </div>
            <div style="flex: 1;">
              <div style="font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase;">[${s.layer}]</div>
              <div style="font-weight: 600; font-size: 12px;">${s.rule}</div>
              <div style="font-size: 11px; color: var(--text-muted);">${s.description}</div>
            </div>
          </div>
        `).join('')}
      </div>
      <div style="margin-top: 16px; padding: 12px; background: var(--warning-light); border-left: 3px solid var(--warning); border-radius: 6px;">
        <div style="font-size: 11px; color: var(--warning-dark); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px;">⚡ Recommended Action</div>
        <div style="font-size: 13px; color: var(--warning-dark);">${a.recommended_action}</div>
      </div>
    `;
    const footer = `
      <button class="btn btn-secondary" data-action="close">Close</button>
      <button class="btn btn-secondary" data-action="approve" style="background: var(--success); color: white; border-color: var(--success);">✓ Approve</button>
      <button class="btn" data-action="block" style="background: var(--danger); color: white;">🚫 Block</button>
    `;
    const modal = Components.modal({ title: `${a.id} — ${a.pattern}`, body, size: 'lg', footer });
    modal.element.querySelector('[data-action="close"]').onclick = () => modal.close();
    modal.element.querySelector('[data-action="approve"]').onclick = async () => {
      try { await window.api.approveFraud(a.id); Components.toast('✓ Approved', 'success'); modal.close(); this.loadData(); }
      catch (e) { Components.handleError(e); }
    };
    modal.element.querySelector('[data-action="block"]').onclick = async () => {
      if (!confirm('Block this transaction?')) return;
      try { await window.api.blockFraud(a.id); Components.toast('🚫 Blocked', 'success'); modal.close(); this.loadData(); }
      catch (e) { Components.handleError(e); }
    };
  },

  unmount() {}
};

window.FraudPage = FraudPage;
