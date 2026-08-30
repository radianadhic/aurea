/**
 * Customer (CIF) Pinia store.
 * Manages customer data, search, filters, pagination.
 */
import { defineStore } from 'pinia';
import { useApi, type PageResponse } from '~/composables/useApi';
import type { Customer, CustomerSearchFilters } from '~/types/customer';

interface CustomerState {
  customers: Customer[];
  currentCustomer: Customer | null;
  loading: boolean;
  totalElements: number;
  totalPages: number;
  currentPage: number;
  pageSize: number;
  searchQuery: string;
  filters: CustomerSearchFilters;
  sortBy: string;
  sortDirection: 'asc' | 'desc';
}

export const useCustomerStore = defineStore('customer', {
  state: (): CustomerState => ({
    customers: [],
    currentCustomer: null,
    loading: false,
    totalElements: 0,
    totalPages: 0,
    currentPage: 0,
    pageSize: 20,
    searchQuery: '',
    filters: {
      cifStatus: undefined,
      kycStatus: undefined,
      riskProfile: undefined,
      branchId: undefined,
      customerType: undefined,
      dateOfBirthFrom: undefined,
      dateOfBirthTo: undefined,
      monthlyIncomeMin: undefined,
      monthlyIncomeMax: undefined,
    },
    sortBy: 'fullName',
    sortDirection: 'asc',
  }),

  getters: {
    hasFilters: (state) => {
      return Object.values(state.filters).some((v) => v !== undefined && v !== '' && v !== null);
    },
  },

  actions: {
    /**
     * Search customers with filters, pagination, sort.
     */
    async search() {
      this.loading = true;
      try {
        const api = useApi();
        const params: Record<string, any> = {
          q: this.searchQuery || undefined,
          page: this.currentPage,
          size: this.pageSize,
          sort: `${this.sortBy},${this.sortDirection}`,
          ...this.cleanFilters(),
        };

        const response: PageResponse<Customer> = await api.getPage<Customer>(
          '/api/v1/customers/search',
          params
        );

        this.customers = response.content;
        this.totalElements = response.totalElements;
        this.totalPages = response.totalPages;
        this.currentPage = response.page;
      } catch (e) {
        console.error('Search failed:', e);
      } finally {
        this.loading = false;
      }
    },

    /**
     * Get customer by ID.
     */
    async fetchById(id: string): Promise<Customer> {
      const api = useApi();
      const customer = await api.get<Customer>(`/api/v1/customers/${id}`);
      this.currentCustomer = customer;
      return customer;
    },

    /**
     * Get customer by CIF number.
     */
    async fetchByCif(cifNumber: string): Promise<Customer> {
      const api = useApi();
      const customer = await api.get<Customer>(`/api/v1/customers/cif/${cifNumber}`);
      this.currentCustomer = customer;
      return customer;
    },

    /**
     * Create a new customer.
     */
    async create(data: Partial<Customer>): Promise<Customer> {
      const api = useApi();
      const created = await api.post<Customer>('/api/v1/customers', data);
      this.customers.unshift(created);
      return created;
    },

    /**
     * Update customer.
     */
    async update(id: string, data: Partial<Customer>): Promise<Customer> {
      const api = useApi();
      const updated = await api.put<Customer>(`/api/v1/customers/${id}`, data);
      // Update in list
      const index = this.customers.findIndex((c) => c.id === id);
      if (index !== -1) {
        this.customers[index] = updated;
      }
      if (this.currentCustomer?.id === id) {
        this.currentCustomer = updated;
      }
      return updated;
    },

    /**
     * Soft delete customer.
     */
    async delete(id: string, reason: string) {
      const api = useApi();
      await api.delete(`/api/v1/customers/${id}?reason=${encodeURIComponent(reason)}`);
      this.customers = this.customers.filter((c) => c.id !== id);
    },

    /**
     * Set search query and trigger search.
     */
    setSearchQuery(query: string) {
      this.searchQuery = query;
      this.currentPage = 0;
      this.search();
    },

    /**
     * Set filter and trigger search.
     */
    setFilter<K extends keyof CustomerSearchFilters>(key: K, value: CustomerSearchFilters[K]) {
      this.filters[key] = value;
      this.currentPage = 0;
      this.search();
    },

    /**
     * Set sort and trigger search.
     */
    setSort(field: string, direction: 'asc' | 'desc' = 'asc') {
      this.sortBy = field;
      this.sortDirection = direction;
      this.search();
    },

    /**
     * Set page and trigger search.
     */
    setPage(page: number) {
      this.currentPage = page;
      this.search();
    },

    /**
     * Reset all filters.
     */
    resetFilters() {
      this.filters = {
        cifStatus: undefined,
        kycStatus: undefined,
        riskProfile: undefined,
        branchId: undefined,
        customerType: undefined,
        dateOfBirthFrom: undefined,
        dateOfBirthTo: undefined,
        monthlyIncomeMin: undefined,
        monthlyIncomeMax: undefined,
      };
      this.searchQuery = '';
      this.currentPage = 0;
      this.search();
    },

    /**
     * Remove undefined/null/empty values from filters for API call.
     */
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
