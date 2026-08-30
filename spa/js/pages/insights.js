/**
 * AUREA SPA — Auto-Insights Page
 */

const InsightsPage = {
  route: 'insights',
  title: 'Auto-Insights',
  subtitle: 'AI-detected anomalies with natural-language narratives',

  state: {
    severity: 'ALL',
    category: 'ALL',
    insights: [],
    summary: null,
  },

  async render(container) {
    container.innerHTML = `
      <div class="page">
        <div class="page-header">
          <div>
            <h1 class="page-title">🧠 Auto-Insights</h1>
            <p class="page-subtitle">${this.subtitle}</p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary" id="refreshBtn">↻ Refresh</button>
            <button class="btn btn-primary" id="exportBtn">📥 Export</button>
          </div>
        </div>

        <!-- Stats -->
        <div class="stat-grid" id="insightsStats">${Components.skeleton(4)}</div>

        <!-- Filters -->
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; align-items: center;">
          <span style="font-size: 12px; color: var(--text-muted); font-weight: 600;">SEVERITY:</span>
          <button class="filter-chip active" data-severity="ALL">All</button>
          <button class="filter-chip" data-severity="CRITICAL">🔴 Critical</button>
          <button class="filter-chip" data-severity="WARNING">🟠 Warning</button>
          <button class="filter-chip" data-severity="INFO">🔵 Info</button>
          <span style="font-size: 12px; color: var(--text-muted); font-weight: 600; margin-left: 16px;">CATEGORY:</span>
          <button class="filter-chip active" data-category="ALL">All</button>
          <button class="filter-chip" data-category="Customer">Customer</button>
          <button class="filter-chip" data-category="Transaction">Transaction</button>
          <button class="filter-chip" data-category="System">System</button>
          <button class="filter-chip" data-category="KYC">KYC</button>
          <button class="filter-chip" data-category="Matching">Matching</button>
        </div>

        <!-- Insights list -->
        <div class="card" style="padding: 0; overflow: hidden;">
          <div id="insightsList" style="padding: 16px;">
            ${Components.skeleton(5)}
          </div>
        </div>
      </div>
    `;

    document.getElementById('refreshBtn').onclick = () => this.loadData();
    document.getElementById('exportBtn').onclick = () => Components.toast('Insights exported to CSV', 'success');

    // Filter handlers
    container.querySelectorAll('[data-severity]').forEach(btn => {
      btn.onclick = () => {
        container.querySelectorAll('[data-severity]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.state.severity = btn.dataset.severity;
        this.renderList();
      };
    });
    container.querySelectorAll('[data-category]').forEach(btn => {
      btn.onclick = () => {
        container.querySelectorAll('[data-category]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.state.category = btn.dataset.category;
        this.renderList();
      };
    });

    await this.loadData();
  },

  async loadData() {
    try {
      Components.loading(true);
      const [summary, insights] = await Promise.all([
        window.api.getInsightsSummary(),
        window.api.getInsights({ limit: 200 }),
      ]);
      this.state.summary = summary;
      this.state.insights = insights;
      this.renderStats();
      this.renderList();
    } catch (err) {
      Components.handleError(err, 'Insights');
    } finally {
      Components.loading(false);
    }
  },

  renderStats() {
    const s = this.state.summary;
    if (!s) return;
    document.getElementById('insightsStats').innerHTML = `
      <div class="stat-card">
        <div class="stat-label">Total Insights</div>
        <div class="stat-value">${s.total_insights || 0}</div>
        <div class="stat-sub">auto-generated</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-label">🔴 Critical</div>
        <div class="stat-value red">${s.by_severity?.CRITICAL || 0}</div>
        <div class="stat-sub">requires action</div>
      </div>
      <div class="stat-card warning">
        <div class="stat-label">🟠 Warning</div>
        <div class="stat-value yellow">${s.by_severity?.WARNING || 0}</div>
        <div class="stat-sub">monitor</div>
      </div>
      <div class="stat-card info">
        <div class="stat-label">🔵 Info</div>
        <div class="stat-value">${s.by_severity?.INFO || 0}</div>
        <div class="stat-sub">informational</div>
      </div>
    `;
  },

  renderList() {
    const filtered = this.state.insights.filter(i => {
      const sevMatch = this.state.severity === 'ALL' || i.severity === this.state.severity;
      const catMatch = this.state.category === 'ALL' || i.category === this.state.category;
      return sevMatch && catMatch;
    });

    const list = document.getElementById('insightsList');
    if (filtered.length === 0) {
      list.innerHTML = Components.emptyState({
        icon: '🔍', title: 'No insights match', desc: 'Try adjusting your filters.'
      });
      return;
    }

    list.innerHTML = filtered.map(i => `
      <div class="insight-row" data-id="${i.id}" style="
        padding: 16px;
        border-bottom: 1px solid var(--border);
        cursor: pointer;
        transition: background 0.15s;
      " onmouseover="this.style.background='var(--gray-50)'" onmouseout="this.style.background=''">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
          <div style="flex-shrink: 0; padding-top: 4px;">
            ${Components.severityBadge(i.severity)}
          </div>
          <div style="flex: 1; min-width: 0;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
              <span class="badge badge-gold">${i.category}</span>
              <span style="font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">${i.metric}</span>
            </div>
            <div style="font-weight: 600; font-size: 14px; color: var(--text); margin-bottom: 4px;">${i.title}</div>
            <div style="font-size: 13px; color: var(--text-muted);">${i.description}</div>
            <div style="display: flex; gap: 16px; margin-top: 8px; font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">
              <span>Deviation: <strong style="color: var(--text);">${i.deviation_pct > 0 ? '+' : ''}${i.deviation_pct.toFixed(1)}%</strong></span>
              <span>Confidence: <strong style="color: var(--text);">${(i.confidence * 100).toFixed(0)}%</strong></span>
              <span>${Components.formatTime(i.detected_at)}</span>
            </div>
          </div>
        </div>
      </div>
    `).join('');

    // Click handlers
    list.querySelectorAll('.insight-row').forEach(row => {
      row.onclick = () => this.showDetail(row.dataset.id);
    });
  },

  async showDetail(id) {
    const insight = this.state.insights.find(i => i.id === id);
    if (!insight) return;

    const body = `
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 20px;">
        <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Current</div>
          <div style="font-size: 20px; font-weight: 700; font-family: 'Georgia', serif;">${Components.formatNumber(insight.current_value)}</div>
        </div>
        <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Expected</div>
          <div style="font-size: 20px; font-weight: 700; font-family: 'Georgia', serif;">${Components.formatNumber(insight.expected_value)}</div>
        </div>
        <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
          <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Deviation</div>
          <div style="font-size: 20px; font-weight: 700; font-family: 'Georgia', serif; color: ${insight.deviation_pct > 0 ? 'var(--success)' : 'var(--danger)'};">
            ${insight.deviation_pct > 0 ? '+' : ''}${insight.deviation_pct.toFixed(1)}%
          </div>
        </div>
      </div>

      ${insight.chart_data ? `
        <div style="margin-bottom: 20px;">
          <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">📈 30-Day Trend</h4>
          <div style="height: 200px; background: var(--gray-50); border-radius: 8px; padding: 12px;">
            <canvas id="insightChart"></canvas>
          </div>
        </div>
      ` : ''}

      <div style="margin-bottom: 20px;">
        <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">💡 Recommended Actions</h4>
        <ul style="list-style: none; padding: 0;">
          ${(insight.recommendations || []).map(r => `
            <li style="padding: 8px 12px; background: var(--gold-pale); border-radius: 6px; margin-bottom: 4px; font-size: 13px;">
              <span style="color: var(--gold-dark); margin-right: 6px;">▸</span>${r}
            </li>
          `).join('') || '<li style="color: var(--text-muted);">No recommendations</li>'}
        </ul>
      </div>
    `;

    const modal = Components.modal({
      title: insight.title,
      body,
      size: 'lg',
    });

    // Render chart with Chart.js
    if (insight.chart_data) {
      // Load Chart.js dynamically
      if (!window.Chart) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
        script.onload = () => renderInsightChart(insight.chart_data);
        document.head.appendChild(script);
      } else {
        setTimeout(() => renderInsightChart(insight.chart_data), 50);
      }
    }
  },

  unmount() {}
};

function renderInsightChart(chartData) {
  const ctx = document.getElementById('insightChart');
  if (!ctx) return;
  const labels = chartData.labels || [];
  const values = chartData.values || [];
  const expected = chartData.expected || [];
  const anomalyIdx = new Set(chartData.anomaly_indices || []);
  const pointColors = values.map((_, i) => anomalyIdx.has(i) ? '#DC2626' : '#D4AF37');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Actual',
          data: values,
          borderColor: '#D4AF37',
          backgroundColor: 'rgba(212, 175, 55, 0.1)',
          borderWidth: 2,
          pointBackgroundColor: pointColors,
          pointRadius: 4,
          tension: 0.3,
          fill: true,
        },
        {
          label: 'Expected',
          data: expected,
          borderColor: '#0A1929',
          borderDash: [5, 5],
          borderWidth: 1.5,
          pointRadius: 0,
          fill: false,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom' } },
      scales: {
        y: { grid: { color: 'rgba(0,0,0,0.05)' } },
        x: { grid: { display: false } }
      }
    }
  });
}

window.InsightsPage = InsightsPage;
