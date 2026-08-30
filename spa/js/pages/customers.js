/**
 * AUREA SPA — Customers Page
 */

const CustomersPage = {
  route: 'customers',
  title: 'Customers',
  subtitle: 'Browse and search all segmented customers',

  state: { customers: [], search: '', segment: '' },

  async render(container) {
    container.innerHTML = `
      <div class="page">
        <div class="page-header">
          <div>
            <h1 class="page-title">👥 Customers</h1>
            <p class="page-subtitle">${this.subtitle}</p>
          </div>
        </div>

        <div style="display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap;">
          <input class="input" id="searchInput" placeholder="Search by name or ID..." style="max-width: 300px;" />
          <select class="select" id="segmentSelect" style="max-width: 200px;">
            <option value="">All segments</option>
          </select>
          <select class="select" id="sortSelect" style="max-width: 200px;">
            <option value="clv_12m">Sort by CLV (high → low)</option>
            <option value="churn_probability">Sort by Churn (high → low)</option>
            <option value="recency_days">Sort by Recency (recent first)</option>
          </select>
        </div>

        <div class="card" style="padding: 0; overflow: hidden;">
          <div id="customersList" style="padding: 8px;">${Components.skeleton(8)}</div>
        </div>
      </div>
    `;

    document.getElementById('searchInput').oninput = (e) => { this.state.search = e.target.value.toLowerCase(); this.renderList(); };
    document.getElementById('segmentSelect').onchange = (e) => { this.state.segment = e.target.value; this.renderList(); };
    document.getElementById('sortSelect').onchange = (e) => { this.state.sort = e.target.value; this.renderList(); };

    await this.loadData();
  },

  async loadData() {
    try {
      const res = await window.api.getCustomers({ limit: 200 });
      this.state.customers = res.customers || [];
      // Populate segment filter
      const segments = [...new Set(this.state.customers.map(c => c.segment))].sort();
      const sel = document.getElementById('segmentSelect');
      sel.innerHTML = '<option value="">All segments</option>' + segments.map(s => `<option>${s}</option>`).join('');
      this.renderList();
    } catch (e) { Components.handleError(e, 'Customers'); }
  },

  renderList() {
    let list = [...this.state.customers];
    if (this.state.search) {
      list = list.filter(c => c.customer_name.toLowerCase().includes(this.state.search) || c.customer_id.toLowerCase().includes(this.state.search));
    }
    if (this.state.segment) list = list.filter(c => c.segment === this.state.segment);
    const sortBy = this.state.sort || 'clv_12m';
    list.sort((a, b) => sortBy === 'recency_days' ? a[sortBy] - b[sortBy] : b[sortBy] - a[sortBy]);

    const container = document.getElementById('customersList');
    if (list.length === 0) {
      container.innerHTML = Components.emptyState({ icon: '🔍', title: 'No customers found' });
      return;
    }

    container.innerHTML = `
      <div style="overflow-x: auto;">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Segment</th>
              <th>RFM</th>
              <th>CLV (12m)</th>
              <th>Churn</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${list.slice(0, 100).map(c => `
              <tr data-id="${c.customer_id}">
                <td style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-muted);">${c.customer_id}</td>
                <td><strong>${c.customer_name}</strong></td>
                <td><span class="badge badge-gold">${c.segment}</span></td>
                <td><span style="font-family: 'JetBrains Mono', monospace; padding: 2px 8px; background: var(--navy); color: var(--gold); border-radius: 4px; font-size: 11px; font-weight: 600;">${c.rfm_score}</span></td>
                <td style="font-weight: 600;">${Components.formatCurrency(c.clv_12m)}</td>
                <td>${Components.churnRiskBadge(c.churn_probability)}</td>
                <td style="font-size: 11px; color: var(--text-muted);">${c.next_best_action?.substring(0, 40)}...</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;

    container.querySelectorAll('tbody tr').forEach(row => {
      row.onclick = () => this.showDetail(row.dataset.id);
    });
  },

  async showDetail(id) {
    try {
      const c = await window.api.getCustomer(id);
      const body = `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
          <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
            <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Segment</div>
            <div style="font-size: 16px; font-weight: 700;">${c.segment}</div>
          </div>
          <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
            <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">RFM Score</div>
            <div style="font-size: 16px; font-weight: 700; font-family: 'JetBrains Mono', monospace;">${c.rfm_score}</div>
          </div>
          <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
            <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">CLV (12m)</div>
            <div style="font-size: 16px; font-weight: 700; color: var(--success);">${Components.formatCurrency(c.clv_12m)}</div>
          </div>
          <div style="background: var(--gray-50); padding: 12px; border-radius: 8px;">
            <div style="font-size: 10px; color: var(--text-muted); text-transform: uppercase;">Churn Risk</div>
            <div style="margin-top: 4px;">${Components.churnRiskBadge(c.churn_probability)} ${(c.churn_probability * 100).toFixed(0)}%</div>
          </div>
        </div>
        <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">📊 Profile</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 16px; font-size: 13px;">
          <div>Recency: <strong>${c.recency_days}d</strong></div>
          <div>Frequency: <strong>${c.frequency} orders</strong></div>
          <div>Monetary: <strong>${Components.formatCurrency(c.monetary)}</strong></div>
        </div>
        <h4 style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">💡 Next Best Action</h4>
        <div style="padding: 12px; background: var(--gold-pale); border-radius: 6px; font-size: 13px;">
          <span style="color: var(--gold-dark); margin-right: 6px;">▸</span>${c.next_best_action}
        </div>
      `;
      Components.modal({ title: c.customer_name, body });
    } catch (e) { Components.handleError(e, 'Customer'); }
  },

  unmount() {}
};

window.CustomersPage = CustomersPage;
