/**
 * AUREA SPA — Smart Customer Segmentation Page
 */

const SegmentationPage = {
  route: 'segmentation',
  title: 'Smart Segmentation',
  subtitle: 'RFM-based customer segments with CLV prediction',

  state: { summary: null, segments: [] },

  async render(container) {
    container.innerHTML = `
      <div class="page">
        <div class="page-header">
          <div>
            <h1 class="page-title">🎯 Smart Customer Segmentation</h1>
            <p class="page-subtitle">${this.subtitle}</p>
          </div>
          <button class="btn btn-primary" id="refreshBtn">↻ Regenerate</button>
        </div>

        <div class="stat-grid" id="segStats">${Components.skeleton(4)}</div>

        <h2 style="font-size: 16px; font-weight: 700; margin: 24px 0 16px;">Customer Segments</h2>
        <div class="stat-grid" id="segmentsList">${Components.skeleton(6)}</div>
      </div>
    `;

    document.getElementById('refreshBtn').onclick = async () => {
      Components.loading(true);
      try {
        await window.api.refreshSegments();
        await this.loadData();
        Components.toast('Segmentation regenerated', 'success');
      } catch (e) { Components.handleError(e, 'Refresh'); }
      finally { Components.loading(false); }
    };

    await this.loadData();
  },

  async loadData() {
    try {
      const [summary, all] = await Promise.all([
        window.api.getSegmentsSummary(),
        window.api.getAllSegments(),
      ]);
      this.state.summary = summary;
      this.state.segments = all.segments || [];
      this.render();
    } catch (err) {
      Components.handleError(err, 'Segmentation');
    }
  },

  render() {
    const s = this.state.summary?.summary || {};
    document.getElementById('segStats').innerHTML = `
      <div class="stat-card">
        <div class="stat-label">👥 Total Customers</div>
        <div class="stat-value">${s.total_customers || 0}</div>
      </div>
      <div class="stat-card success">
        <div class="stat-label">🏆 Champions</div>
        <div class="stat-value green">${s.champions || 0}</div>
        <div class="stat-sub">${Components.formatCurrency(s.total_revenue ? s.total_revenue * 0.6 : 0)} revenue</div>
      </div>
      <div class="stat-card warning">
        <div class="stat-label">⚠️ At Risk</div>
        <div class="stat-value yellow">${s.at_risk || 0}</div>
        <div class="stat-sub">need retention</div>
      </div>
      <div class="stat-card info">
        <div class="stat-label">💰 12-month CLV</div>
        <div class="stat-value gold">${Components.formatCurrency(s.total_predicted_clv_12m || 0)}</div>
      </div>
    `;

    const ICONS = { Champions: '🏆', 'Loyal Customers': '⭐', 'Potential Loyalists': '🌱',
      'Recent Customers': '👋', Promising: '📈', 'Need Attention': '⚠️',
      'About to Sleep': '😴', 'At Risk': '🚨', Hibernating: '💤', Lost: '👻' };

    document.getElementById('segmentsList').innerHTML = this.state.segments.map(seg => `
      <div class="card segment-card" data-seg="${seg.name}" style="cursor: pointer; border-left: 4px solid ${seg.color};">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
          <div style="font-size: 28px;">${ICONS[seg.name] || '📊'}</div>
          <div style="flex: 1;">
            <div style="font-weight: 700; font-size: 15px;">${seg.name}</div>
            <div style="font-size: 11px; color: var(--text-muted);">${seg.customer_count} customers (${seg.percentage}%)</div>
          </div>
        </div>
        <p style="font-size: 12px; color: var(--text-muted); line-height: 1.5; margin-bottom: 12px;">
          ${(seg.description || '').substring(0, 100)}...
        </p>
        <div style="display: flex; justify-content: space-between; font-size: 12px;">
          <div>
            <div style="color: var(--text-muted); font-size: 10px; text-transform: uppercase;">Revenue</div>
            <div style="font-weight: 700;">${Components.formatCurrency(seg.total_revenue)}</div>
          </div>
          <div>
            <div style="color: var(--text-muted); font-size: 10px; text-transform: uppercase;">Avg CLV</div>
            <div style="font-weight: 700;">${Components.formatCurrency(seg.avg_clv)}</div>
          </div>
          <div>
            <div style="color: var(--text-muted); font-size: 10px; text-transform: uppercase;">Risk</div>
            ${Components.riskLevelBadge(seg.churn_risk)}
          </div>
        </div>
      </div>
    `).join('');

    // Click to open detail
    document.querySelectorAll('.segment-card').forEach(card => {
      card.onclick = () => this.showDetail(card.dataset.seg);
    });
  },

  async showDetail(name) {
    try {
      const seg = await window.api.getSegment(name);
      const body = `
        <p style="margin-bottom: 16px; color: var(--text-muted);">${seg.description}</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
          <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
            <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Customers</div>
            <div style="font-size: 22px; font-weight: 700;">${seg.customer_count} (${seg.percentage}%)</div>
          </div>
          <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
            <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Total Revenue</div>
            <div style="font-size: 22px; font-weight: 700;">${Components.formatCurrency(seg.total_revenue)}</div>
          </div>
          <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
            <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Avg CLV (12m)</div>
            <div style="font-size: 22px; font-weight: 700;">${Components.formatCurrency(seg.avg_clv)}</div>
          </div>
          <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
            <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Churn Risk</div>
            <div style="font-size: 18px; font-weight: 700; margin-top: 4px;">${Components.riskLevelBadge(seg.churn_risk)}</div>
          </div>
        </div>
        <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">Characteristics</h4>
        <ul style="margin-bottom: 16px; padding-left: 20px; font-size: 13px;">
          ${(seg.characteristics || []).map(c => `<li style="margin-bottom: 4px;">${c}</li>`).join('')}
        </ul>
        <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">Recommended Actions</h4>
        <ul style="list-style: none; padding: 0;">
          ${(seg.recommendations || []).map(r => `
            <li style="padding: 8px 12px; background: var(--gold-pale); border-radius: 6px; margin-bottom: 4px; font-size: 13px;">
              <span style="color: var(--gold-dark); margin-right: 6px;">▸</span>${r}
            </li>
          `).join('')}
        </ul>
      `;
      Components.modal({ title: seg.name, body, size: 'md' });
    } catch (e) { Components.handleError(e, 'Segment'); }
  },

  unmount() {}
};

window.SegmentationPage = SegmentationPage;
