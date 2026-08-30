/**
 * AUREA SPA — API Client
 * Pure vanilla JavaScript fetch wrapper
 */

const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:8000'
  : '/api';

class AureaAPI {
  constructor(baseURL = API_BASE) {
    this.baseURL = baseURL;
    this.cache = new Map();
    this.cacheTimeout = 30000; // 30s
  }

  async _request(path, options = {}) {
    const url = `${this.baseURL}${path}`;
    const cacheKey = options.method === 'GET' ? url : null;

    // Check cache
    if (cacheKey && this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.time < this.cacheTimeout) {
        return cached.data;
      }
      this.cache.delete(cacheKey);
    }

    try {
      const res = await fetch(url, {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`API ${res.status}: ${errText}`);
      }

      const data = await res.json();

      // Cache successful GET
      if (cacheKey) {
        this.cache.set(cacheKey, { data, time: Date.now() });
      }

      return data;
    } catch (err) {
      console.error(`[AUREA API] ${path}:`, err);
      throw err;
    }
  }

  clearCache() { this.cache.clear(); }

  // ============ Insights ============
  async getInsightsSummary() {
    return this._request('/insights/summary');
  }
  async getInsights({ severity, category, type, limit = 100 } = {}) {
    const params = new URLSearchParams();
    if (severity) params.append('severity', severity);
    if (category) params.append('category', category);
    if (type) params.append('insight_type', type);
    params.append('limit', limit);
    return this._request(`/insights?${params}`);
  }
  async getCriticalInsights() { return this._request('/insights/critical'); }
  async getInsightById(id) { return this._request(`/insights/${id}`); }
  async refreshInsights() {
    return this._request('/insights/refresh', { method: 'POST' });
  }

  // ============ Segmentation ============
  async getSegmentsSummary() { return this._request('/segments/summary'); }
  async getAllSegments() { return this._request('/segments'); }
  async getSegment(name) { return this._request(`/segments/${encodeURIComponent(name)}`); }
  async getSegmentCustomers(name, limit = 50) {
    return this._request(`/segments/${encodeURIComponent(name)}/customers?limit=${limit}`);
  }
  async getCustomers({ segment, minClv, minChurn, limit } = {}) {
    const params = new URLSearchParams();
    if (segment) params.append('segment', segment);
    if (minClv !== undefined) params.append('min_clv', minClv);
    if (minChurn !== undefined) params.append('min_churn', minChurn);
    if (limit) params.append('limit', limit);
    return this._request(`/customers?${params}`);
  }
  async getCustomer(id) { return this._request(`/customers/${id}`); }
  async refreshSegments(n = 200, seed = 42) {
    return this._request(`/segments/refresh?n=${n}&seed=${seed}`, { method: 'POST' });
  }

  // ============ Churn ============
  async getChurnSummary() { return this._request('/churn/summary'); }
  async getChurnDashboard() { return this._request('/churn'); }
  async getChurnAlerts({ level, status, minRisk, minClv, limit } = {}) {
    const params = new URLSearchParams();
    if (level) params.append('level', level);
    if (status) params.append('status', status);
    if (minRisk !== undefined) params.append('min_risk', minRisk);
    if (minClv !== undefined) params.append('min_clv', minClv);
    if (limit) params.append('limit', limit);
    return this._request(`/churn/alerts?${params}`);
  }
  async getChurnAlert(id) { return this._request(`/churn/alerts/${id}`); }
  async acknowledgeChurn(id, user = 'admin') {
    return this._request(`/churn/alerts/${id}/acknowledge?user=${encodeURIComponent(user)}`, { method: 'POST' });
  }
  async resolveChurn(id, outcome = 'Customer retained', user = 'admin') {
    return this._request(`/churn/alerts/${id}/resolve?outcome=${encodeURIComponent(outcome)}&user=${encodeURIComponent(user)}`, { method: 'POST' });
  }
  async createChurnIntervention(id, type, message, assignedTo = 'Retention Team') {
    const params = new URLSearchParams({
      intervention_type: type,
      message,
      assigned_to: assignedTo,
    });
    return this._request(`/churn/alerts/${id}/intervene?${params}`, { method: 'POST' });
  }
  async refreshChurn(n = 200, seed = 42) {
    return this._request(`/churn/refresh?n=${n}&seed=${seed}`, { method: 'POST' });
  }

  // ============ Fraud ============
  async getFraudSummary() { return this._request('/fraud/summary'); }
  async getFraudDashboard() { return this._request('/fraud'); }
  async getFraudAlerts({ decision, pattern, priority, minRisk, minAmount, limit } = {}) {
    const params = new URLSearchParams();
    if (decision) params.append('decision', decision);
    if (pattern) params.append('pattern', pattern);
    if (priority) params.append('priority', priority);
    if (minRisk !== undefined) params.append('min_risk', minRisk);
    if (minAmount !== undefined) params.append('min_amount', minAmount);
    if (limit) params.append('limit', limit);
    return this._request(`/fraud/alerts?${params}`);
  }
  async getFraudAlert(id) { return this._request(`/fraud/alerts/${id}`); }
  async getFraudCases({ status, limit } = {}) {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (limit) params.append('limit', limit);
    return this._request(`/fraud/cases?${params}`);
  }
  async approveFraud(id, user = 'admin') {
    return this._request(`/fraud/alerts/${id}/approve?user=${encodeURIComponent(user)}`, { method: 'POST' });
  }
  async blockFraud(id, user = 'admin') {
    return this._request(`/fraud/alerts/${id}/block?user=${encodeURIComponent(user)}`, { method: 'POST' });
  }
  async refreshFraud(n = 500, seed = 42) {
    return this._request(`/fraud/refresh?n_tx=${n}&seed=${seed}`, { method: 'POST' });
  }

  // ============ Health ============
  async getHealth() { return this._request('/health'); }
  async getUnifiedDashboard() { return this._request('/dashboard'); }
}

// Global instance
window.api = new AureaAPI();
