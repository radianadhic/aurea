/**
 * Audit trail store.
 * Manages activity logs, audit queries, compliance reporting.
 */
import { defineStore } from 'pinia';
import { useApi, type PageResponse } from '~/composables/useApi';

export type AuditAction =
  | 'CUSTOMER_CREATE' | 'CUSTOMER_UPDATE' | 'CUSTOMER_DELETE' | 'CUSTOMER_VIEW'
  | 'KYC_APPROVE' | 'KYC_REJECT' | 'KYC_REVIEW'
  | 'MATCH_AUTO' | 'MATCH_MERGE' | 'MATCH_REJECT' | 'MATCH_ESCALATE'
  | 'BLACKLIST_ADD' | 'BLACKLIST_REMOVE'
  | 'CONFIG_CHANGE' | 'RULE_CHANGE' | 'PERMISSION_CHANGE'
  | 'LOGIN' | 'LOGOUT' | 'LOGIN_FAILED';

export interface AuditEntry {
  id: string;
  timestamp: string;
  userId: string;
  username: string;
  userFullName?: string;
  userRole?: string;
  action: AuditAction;
  entity: string;
  entityId: string;
  ipAddress: string;
  userAgent: string;
  changes?: AuditChange[];
  metadata?: Record<string, any>;
  result: 'SUCCESS' | 'FAILURE';
  errorMessage?: string;
  sessionId?: string;
}

export interface AuditChange {
  field: string;
  oldValue: any;
  newValue: any;
}

interface AuditState {
  entries: AuditEntry[];
  currentEntry: AuditEntry | null;
  loading: boolean;
  totalElements: number;
  currentPage: number;
  pageSize: number;
  filters: {
    userId?: string;
    username?: string;
    action?: AuditAction;
    entity?: string;
    entityId?: string;
    result?: string;
    fromDate?: string;
    toDate?: string;
  };
}

export const useAuditStore = defineStore('audit', {
  state: (): AuditState => ({
    entries: [],
    currentEntry: null,
    loading: false,
    totalElements: 0,
    currentPage: 0,
    pageSize: 50,
    filters: {
      userId: undefined,
      username: undefined,
      action: undefined,
      entity: undefined,
      entityId: undefined,
      result: undefined,
      fromDate: undefined,
      toDate: undefined,
    },
  }),

  actions: {
    async fetchEntries() {
      this.loading = true;
      try {
        const api = useApi();
        const response: PageResponse<AuditEntry> = await api.getPage<AuditEntry>(
          '/api/v1/audit/entries',
          {
            page: this.currentPage,
            size: this.pageSize,
            ...this.cleanFilters(),
          }
        );
        this.entries = response.content;
        this.totalElements = response.totalElements;
      } catch (e) {
        console.error('Failed to fetch audit entries:', e);
      } finally {
        this.loading = false;
      }
    },

    async fetchEntry(id: string): Promise<AuditEntry> {
      const api = useApi();
      const entry = await api.get<AuditEntry>(`/api/v1/audit/entries/${id}`);
      this.currentEntry = entry;
      return entry;
    },

    async exportEntries(format: 'CSV' | 'PDF' | 'EXCEL') {
      const api = useApi();
      const response: any = await api.post('/api/v1/audit/export', {
        format,
        ...this.cleanFilters(),
      });
      return response;
    },

    cleanFilters(): Record<string, any> {
      const cleaned: Record<string, any> = {};
      Object.entries(this.filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          cleaned[key] = value;
        }
      });
      return cleaned;
    },
  },
});
