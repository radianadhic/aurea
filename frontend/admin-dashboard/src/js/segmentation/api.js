/**
 * AUREA Customer Segmentation API Client
 * Connects to the AUREA ML Service for RFM-based segmentation
 */

const SEGMENTATION_API = import.meta.env.VITE_INSIGHTS_API || 'http://localhost:8000';

class SegmentationAPI {
  constructor(baseURL = SEGMENTATION_API) {
    this.baseURL = baseURL;
  }

  async _fetch(path, options = {}) {
    const res = await fetch(`${this.baseURL}${path}`, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Segmentation API ${res.status}: ${err}`);
    }
    return res.json();
  }

  async getSummary() {
    return this._fetch('/segments/summary');
  }

  async getAllSegments() {
    return this._fetch('/segments');
  }

  async getSegment(name) {
    return this._fetch(`/segments/${encodeURIComponent(name)}`);
  }

  async getSegmentCustomers(name, limit = 50) {
    return this._fetch(`/segments/${encodeURIComponent(name)}/customers?limit=${limit}`);
  }

  async getCustomers({ segment, minClv, minChurn, limit } = {}) {
    const params = new URLSearchParams();
    if (segment) params.append('segment', segment);
    if (minClv !== undefined) params.append('min_clv', minClv);
    if (minChurn !== undefined) params.append('min_churn', minChurn);
    if (limit) params.append('limit', limit);
    return this._fetch(`/customers?${params}`);
  }

  async getCustomer(id) {
    return this._fetch(`/customers/${id}`);
  }

  async getDashboard() {
    return this._fetch('/dashboard');
  }

  async refresh(n = 200, seed = 42) {
    return this._fetch(`/segments/refresh?n=${n}&seed=${seed}`, { method: 'POST' });
  }
}

export const segmentationAPI = new SegmentationAPI();
