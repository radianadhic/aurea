/**
 * Matching queue store.
 * Manages duplicate detection and merging workflow.
 */
import { defineStore } from 'pinia';
import { useApi, type PageResponse } from '~/composables/useApi';

export type MatchStatus = 'PENDING' | 'IN_REVIEW' | 'AUTO_MERGED' | 'MANUALLY_MERGED' | 'REJECTED' | 'ESCALATED';
export type MatchType = 'EXACT' | 'FUZZY' | 'PHONETIC' | 'TRANSACTION';

export interface MatchGroup {
  id: string;
  matchType: MatchType;
  matchScore: number;
  status: MatchStatus;
  memberCount: number;
  totalRecords: number;
  algorithm: string;
  candidates: MatchCandidate[];
  reviewer?: string;
  reviewerId?: string;
  reviewedAt?: string;
  createdAt: string;
  updatedAt: string;
  notes?: string;
}

export interface MatchCandidate {
  id: string;
  cifNumber: string;
  fullName: string;
  dateOfBirth?: string;
  nik?: string;
  email?: string;
  mobilePhone?: string;
  address?: string;
  matchScore: number;
  matchFields: string[];
  selected: boolean;
}

interface MatchingState {
  matchGroups: MatchGroup[];
  currentGroup: MatchGroup | null;
  loading: boolean;
  totalElements: number;
  currentPage: number;
  pageSize: number;
  filters: {
    status?: MatchStatus;
    matchType?: MatchType;
    minScore?: number;
    maxScore?: number;
    algorithm?: string;
  };
}

export const useMatchingStore = defineStore('matching', {
  state: (): MatchingState => ({
    matchGroups: [],
    currentGroup: null,
    loading: false,
    totalElements: 0,
    currentPage: 0,
    pageSize: 20,
    filters: {
      status: undefined,
      matchType: undefined,
      minScore: undefined,
      maxScore: undefined,
      algorithm: undefined,
    },
  }),

  actions: {
    async fetchGroups() {
      this.loading = true;
      try {
        const api = useApi();
        const response: PageResponse<MatchGroup> = await api.getPage<MatchGroup>(
          '/api/v1/matching/groups',
          {
            page: this.currentPage,
            size: this.pageSize,
            ...this.cleanFilters(),
          }
        );
        this.matchGroups = response.content;
        this.totalElements = response.totalElements;
      } catch (e) {
        console.error('Failed to fetch match groups:', e);
      } finally {
        this.loading = false;
      }
    },

    async fetchGroup(id: string): Promise<MatchGroup> {
      const api = useApi();
      const group = await api.get<MatchGroup>(`/api/v1/matching/groups/${id}`);
      this.currentGroup = group;
      return group;
    },

    async merge(groupId: string, primaryId: string, secondaryIds: string[], notes?: string) {
      const api = useApi();
      const result = await api.post(`/api/v1/matching/groups/${groupId}/merge`, {
        primaryId,
        secondaryIds,
        notes,
      });
      await this.fetchGroups();
      return result;
    },

    async reject(groupId: string, reason: string) {
      const api = useApi();
      await api.post(`/api/v1/matching/groups/${groupId}/reject`, { reason });
      await this.fetchGroups();
    },

    async escalate(groupId: string, assignedTo: string, reason: string) {
      const api = useApi();
      await api.post(`/api/v1/matching/groups/${groupId}/escalate`, { assignedTo, reason });
      await this.fetchGroups();
    },

    setPage(page: number) {
      this.currentPage = page;
      this.fetchGroups();
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
