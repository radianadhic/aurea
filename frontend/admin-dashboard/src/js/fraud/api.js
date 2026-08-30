/**
 * AUREA Real-time Fraud Detection API Client
 */

const FRAUD_API = import.meta.env.VITE_INSIGHTS_API || 'http://localhost:8000';

class FraudAPI {
  constructor(baseURL = FRAUD_API) {
    this.baseURL = baseURL;
  }

  async _fetch(path, options = {}) {
    const res = await fetch(`${this.baseURL}${path}`, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Fraud API ${res.status}: ${err}`);
    }
    return res.json();
  }

  async getSummary() { return this._fetch('/fraud/summary'); }
  async getDashboard() { return this._fetch('/fraud'); }
  async getAlerts({ decision, pattern, priority, minRisk, minAmount, limit } = {}) {
    const params = new URLSearchParams();
    if (decision) params.append('decision', decision);
    if (pattern) params.append('pattern', pattern);
    if (priority) params.append('priority', priority);
    if (minRisk !== undefined) params.append('min_risk', minRisk);
    if (minAmount !== undefined) params.append('min_amount', minAmount);
    if (limit) params.append('limit', limit);
    return this._fetch(`/fraud/alerts?${params}`);
  }
  async getAlert(id) { return this._fetch(`/fraud/alerts/${id}`); }
  async approve(id, user = 'current_user') {
    return this._fetch(`/fraud/alerts/${id}/approve?user=${encodeURIComponent(user)}`, { method: 'POST' });
  }
  async block(id, user = 'current_user') {
    return this._fetch(`/fraud/alerts/${id}/block?user=${encodeURIComponent(user)}`, { method: 'POST' });
  }
  async getCases({ status, limit } = {}) {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (limit) params.append('limit', limit);
    return this._fetch(`/fraud/cases?${params}`);
  }
  async refresh(n_tx = 500, seed = 42) {
    return this._fetch(`/fraud/refresh?n_tx=${n_tx}&seed=${seed}`, { method: 'POST' });
  }
}

export const fraudAPI = new FraudAPI();
