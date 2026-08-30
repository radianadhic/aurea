/**
 * AUREA Churn Watch List API Client
 * Real-time churn risk monitoring & intervention management
 */

const CHURN_API = import.meta.env.VITE_INSIGHTS_API || 'http://localhost:8000';

class ChurnAPI {
  constructor(baseURL = CHURN_API) {
    this.baseURL = baseURL;
  }

  async _fetch(path, options = {}) {
    const res = await fetch(`${this.baseURL}${path}`, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Churn API ${res.status}: ${err}`);
    }
    return res.json();
  }

  async getSummary() {
    return this._fetch('/churn/summary');
  }

  async getDashboard() {
    return this._fetch('/churn');
  }

  async getAlerts({ level, status, minRisk, minClv, limit } = {}) {
    const params = new URLSearchParams();
    if (level) params.append('level', level);
    if (status) params.append('status', status);
    if (minRisk !== undefined) params.append('min_risk', minRisk);
    if (minClv !== undefined) params.append('min_clv', minClv);
    if (limit) params.append('limit', limit);
    return this._fetch(`/churn/alerts?${params}`);
  }

  async getAlert(id) {
    return this._fetch(`/churn/alerts/${id}`);
  }

  async acknowledge(id, user = 'current_user') {
    return this._fetch(`/churn/alerts/${id}/acknowledge?user=${encodeURIComponent(user)}`, { method: 'POST' });
  }

  async resolve(id, outcome = 'Customer retained', user = 'current_user') {
    return this._fetch(`/churn/alerts/${id}/resolve?outcome=${encodeURIComponent(outcome)}&user=${encodeURIComponent(user)}`, { method: 'POST' });
  }

  async intervene(id, interventionType, message, assignedTo = 'Retention Team') {
    const params = new URLSearchParams({
      intervention_type: interventionType,
      message,
      assigned_to: assignedTo,
    });
    return this._fetch(`/churn/alerts/${id}/intervene?${params}`, { method: 'POST' });
  }

  async getInterventions({ status, customerId, limit } = {}) {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (customerId) params.append('customer_id', customerId);
    if (limit) params.append('limit', limit);
    return this._fetch(`/churn/interventions?${params}`);
  }

  async refresh(n = 200, seed = 42) {
    return this._fetch(`/churn/refresh?n=${n}&seed=${seed}`, { method: 'POST' });
  }
}

export const churnAPI = new ChurnAPI();
