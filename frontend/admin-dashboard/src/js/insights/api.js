/**
 * AUREA Auto-Insights API Client
 * Connects to the AUREA ML Service for auto-generated insights
 */

const INSIGHTS_API = import.meta.env.VITE_INSIGHTS_API || 'http://localhost:8000';

class InsightsAPI {
  constructor(baseURL = INSIGHTS_API) {
    this.baseURL = baseURL;
  }

  async _fetch(path, options = {}) {
    const res = await fetch(`${this.baseURL}${path}`, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Insights API ${res.status}: ${err}`);
    }
    return res.json();
  }

  async getSummary() {
    return this._fetch('/insights/summary');
  }

  async getAll({ severity, category, type, limit = 100 } = {}) {
    const params = new URLSearchParams();
    if (severity) params.append('severity', severity);
    if (category) params.append('category', category);
    if (type) params.append('insight_type', type);
    params.append('limit', limit);
    return this._fetch(`/insights?${params}`);
  }

  async getCritical() {
    return this._fetch('/insights/critical');
  }

  async getByCategory(category) {
    return this._fetch(`/insights/category/${category}`);
  }

  async getById(id) {
    return this._fetch(`/insights/${id}`);
  }

  async refresh() {
    return this._fetch('/insights/refresh', { method: 'POST' });
  }
}

export const insightsAPI = new InsightsAPI();
