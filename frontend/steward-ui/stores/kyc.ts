/**
 * KYC (Know Your Customer) store.
 * Manages KYC review queue, approvals, document verification.
 */
import { defineStore } from 'pinia';
import { useApi, type PageResponse } from '~/composables/useApi';
import type { KycStatus } from '~/types/customer';

export interface KycCase {
  id: string;
  cifNumber: string;
  customerName: string;
  kycStatus: KycStatus;
  kycLevel: 'STANDARD' | 'ENHANCED' | 'SIMPLIFIED';
  riskScore: number;
  pepStatus: boolean;
  sanctionsStatus: 'CLEAR' | 'MATCH' | 'POTENTIAL_MATCH' | 'PENDING';
  documentCompleteness: number;
  daysSinceLastUpdate: number;
  assignedTo?: string;
  assignedToId?: string;
  submittedAt: string;
  reviewDeadline?: string;
  documents: KycDocument[];
  flags: string[];
  customerId: string;
}

export interface KycDocument {
  id: string;
  type: 'KTP' | 'NPWP' | 'PASSPORT' | 'SELFIE' | 'SIGNATURE' | 'PROOF_OF_ADDRESS' | 'OTHER';
  fileName: string;
  fileSize: number;
  uploadedAt: string;
  verified: boolean;
  verifiedBy?: string;
  expiryDate?: string;
  url: string;
}

interface KycState {
  cases: KycCase[];
  currentCase: KycCase | null;
  loading: boolean;
  totalElements: number;
  currentPage: number;
  pageSize: number;
  filters: {
    kycStatus?: KycStatus;
    kycLevel?: string;
    riskLevel?: string;
    assignedToMe?: boolean;
    pepOnly?: boolean;
    sanctionsOnly?: boolean;
  };
  stats: {
    pending: number;
    inReview: number;
    approved: number;
    rejected: number;
    expiring: number;
  };
}

export const useKycStore = defineStore('kyc', {
  state: (): KycState => ({
    cases: [],
    currentCase: null,
    loading: false,
    totalElements: 0,
    currentPage: 0,
    pageSize: 20,
    filters: {
      kycStatus: undefined,
      kycLevel: undefined,
      riskLevel: undefined,
      assignedToMe: false,
      pepOnly: false,
      sanctionsOnly: false,
    },
    stats: {
      pending: 0,
      inReview: 0,
      approved: 0,
      rejected: 0,
      expiring: 0,
    },
  }),

  actions: {
    async fetchCases() {
      this.loading = true;
      try {
        const api = useApi();
        const response: PageResponse<KycCase> = await api.getPage<KycCase>(
          '/api/v1/kyc/cases',
          {
            page: this.currentPage,
            size: this.pageSize,
            ...this.cleanFilters(),
          }
        );
        this.cases = response.content;
        this.totalElements = response.totalElements;
      } catch (e) {
        console.error('Failed to fetch KYC cases:', e);
      } finally {
        this.loading = false;
      }
    },

    async fetchCase(id: string): Promise<KycCase> {
      const api = useApi();
      const kycCase = await api.get<KycCase>(`/api/v1/kyc/cases/${id}`);
      this.currentCase = kycCase;
      return kycCase;
    },

    async approve(caseId: string, decision: { notes?: string; kycLevel?: string; validUntil?: string }) {
      const api = useApi();
      const result = await api.post(`/api/v1/kyc/cases/${caseId}/approve`, decision);
      await this.fetchCases();
      return result;
    },

    async reject(caseId: string, reason: string, notes?: string) {
      const api = useApi();
      const result = await api.post(`/api/v1/kyc/cases/${caseId}/reject`, { reason, notes });
      await this.fetchCases();
      return result;
    },

    async assignToMe(caseId: string) {
      const api = useApi();
      await api.post(`/api/v1/kyc/cases/${caseId}/assign`, { assignToMe: true });
      await this.fetchCases();
    },

    async fetchStats() {
      const api = useApi();
      const stats = await api.get<typeof this.stats>('/api/v1/kyc/stats');
      this.stats = stats;
    },

    cleanFilters(): Record<string, any> {
      const cleaned: Record<string, any> = {};
      Object.entries(this.filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '' && value !== false) {
          cleaned[key] = value;
        }
      });
      return cleaned;
    },
  },
});
