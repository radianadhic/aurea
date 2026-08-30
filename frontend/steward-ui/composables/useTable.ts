/**
 * useTable composable - Server-side table state management.
 * Handles pagination, sorting, filtering, fetching.
 */
import { ref, reactive, computed, watch } from 'vue';
import { useApi, type PageResponse } from '~/composables/useApi';

export interface UseTableOptions<T> {
  endpoint: string;
  initialPage?: number;
  initialPageSize?: number;
  initialSort?: { field: string; direction: 'asc' | 'desc' };
  initialFilters?: Record<string, any>;
  pageSizes?: number[];
  autoFetch?: boolean;
  transform?: (data: any) => T;
}

export function useTable<T = any>(options: UseTableOptions<T>) {
  const api = useApi();

  const data = ref<T[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const totalElements = ref(0);
  const totalPages = ref(0);
  const currentPage = ref(options.initialPage || 0);
  const pageSize = ref(options.initialPageSize || 20);
  const sortBy = ref(options.initialSort?.field || '');
  const sortDirection = ref<'asc' | 'desc'>(options.initialSort?.direction || 'asc');
  const filters = reactive<Record<string, any>>({ ...(options.initialFilters || {}) });
  const search = ref('');
  const pageSizes = ref(options.pageSizes || [10, 20, 50, 100]);

  const hasFilters = computed(
    () => Object.values(filters).some((v) => v !== undefined && v !== null && v !== '') || !!search.value
  );

  const startIndex = computed(() => {
    if (totalElements.value === 0) return 0;
    return currentPage.value * pageSize.value + 1;
  });

  const endIndex = computed(() => {
    return Math.min((currentPage.value + 1) * pageSize.value, totalElements.value);
  });

  function cleanParams() {
    const params: Record<string, any> = {
      page: currentPage.value,
      size: pageSize.value,
    };
    if (sortBy.value) {
      params.sort = `${sortBy.value},${sortDirection.value}`;
    }
    if (search.value) {
      params.q = search.value;
    }
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params[key] = value;
      }
    });
    return params;
  }

  async function fetchData() {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getPage<any>(options.endpoint, cleanParams());
      data.value = options.transform
        ? response.content.map(options.transform)
        : response.content;
      totalElements.value = response.totalElements;
      totalPages.value = response.totalPages;
      currentPage.value = response.page;
    } catch (e: any) {
      error.value = e.message || 'Failed to load data';
      data.value = [];
    } finally {
      loading.value = false;
    }
  }

  function setPage(page: number) {
    if (page < 0 || page >= totalPages.value) return;
    currentPage.value = page;
    fetchData();
  }

  function setPageSize(size: number) {
    pageSize.value = size;
    currentPage.value = 0;
    fetchData();
  }

  function setSort(field: string, direction?: 'asc' | 'desc') {
    if (sortBy.value === field) {
      sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortBy.value = field;
      sortDirection.value = direction || 'asc';
    }
    fetchData();
  }

  function setFilter(key: string, value: any) {
    filters[key] = value;
    currentPage.value = 0;
    fetchData();
  }

  function clearFilter(key: string) {
    delete filters[key];
    currentPage.value = 0;
    fetchData();
  }

  function clearAllFilters() {
    Object.keys(filters).forEach((k) => delete filters[k]);
    search.value = '';
    currentPage.value = 0;
    fetchData();
  }

  function setSearch(query: string) {
    search.value = query;
    currentPage.value = 0;
    fetchData();
  }

  function refresh() {
    return fetchData();
  }

  if (options.autoFetch !== false) {
    fetchData();
  }

  return {
    data,
    loading,
    error,
    totalElements,
    totalPages,
    currentPage,
    pageSize,
    sortBy,
    sortDirection,
    filters,
    search,
    pageSizes,
    hasFilters,
    startIndex,
    endIndex,
    fetchData,
    setPage,
    setPageSize,
    setSort,
    setFilter,
    clearFilter,
    clearAllFilters,
    setSearch,
    refresh,
  };
}
