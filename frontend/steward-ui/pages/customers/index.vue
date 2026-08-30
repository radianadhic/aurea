<template>
  <div class="customers-page">
    <PageHeader
      title="Pencarian Nasabah"
      subtitle="Cari dan kelola data nasabah (CIF) Bank XYZ"
    >
      <template #actions>
        <el-button @click="exportData" :disabled="!customers.length">
          📥 Export
        </el-button>
        <el-button
          v-if="canWriteCustomer"
          type="primary"
          @click="navigateTo('/customers/new')"
        >
          ➕ Nasabah Baru
        </el-button>
      </template>
    </PageHeader>

    <div class="page-content">
      <!-- Search + Filter -->
      <div class="search-section">
        <SearchBar
          :model-value="customerStore.searchQuery"
          placeholder="Cari CIF, nama, NIK, email, no. rekening..."
          @update:model-value="customerStore.searchQuery = $event"
          @search="handleSearch"
          @clear="handleClear"
        />

        <FilterPanel
          v-model="filterOpen"
          :active-count="activeFilterCount"
          @clear="handleClearFilters"
        >
          <FormField label="Tipe Nasabah">
            <el-select
              v-model="customerStore.filters.customerType"
              placeholder="Semua"
              clearable
              @change="customerStore.setFilter('customerType', $event)"
            >
              <el-option v-for="t in customerTypes" :key="t.value" :value="t.value" :label="t.label" />
            </el-select>
          </FormField>

          <FormField label="Status CIF">
            <el-select
              v-model="customerStore.filters.cifStatus"
              placeholder="Semua"
              clearable
              @change="customerStore.setFilter('cifStatus', $event)"
            >
              <el-option v-for="s in cifStatuses" :key="s.value" :value="s.value" :label="s.label" />
            </el-select>
          </FormField>

          <FormField label="Status KYC">
            <el-select
              v-model="customerStore.filters.kycStatus"
              placeholder="Semua"
              clearable
              @change="customerStore.setFilter('kycStatus', $event)"
            >
              <el-option v-for="s in kycStatuses" :key="s.value" :value="s.value" :label="s.label" />
            </el-select>
          </FormField>

          <FormField label="Risk Profile">
            <el-select
              v-model="customerStore.filters.riskProfile"
              placeholder="Semua"
              clearable
              @change="customerStore.setFilter('riskProfile', $event)"
            >
              <el-option v-for="r in riskProfiles" :key="r.value" :value="r.value" :label="r.label" />
            </el-select>
          </FormField>

          <FormField label="Cabang">
            <el-select
              v-model="customerStore.filters.branchId"
              placeholder="Semua"
              clearable
              @change="customerStore.setFilter('branchId', $event)"
            >
              <el-option label="KCP Jakarta Pusat" value="JKT-001" />
              <el-option label="KCP Jakarta Selatan" value="JKT-002" />
              <el-option label="KCP Bandung" value="BDG-001" />
              <el-option label="KCP Surabaya" value="SBY-001" />
            </el-select>
          </FormField>

          <FormField label="Tgl Lahir (dari)">
            <el-date-picker
              v-model="customerStore.filters.dateOfBirthFrom"
              type="date"
              placeholder="Pilih tanggal"
              value-format="YYYY-MM-DD"
              @change="customerStore.search()"
            />
          </FormField>

          <FormField label="Income Minimum">
            <el-input-number
              v-model="customerStore.filters.monthlyIncomeMin"
              :min="0"
              :step="1000000"
              placeholder="0"
              @change="customerStore.search()"
            />
          </FormField>

          <FormField label="Tag">
            <el-select
              v-model="tagFilter"
              multiple
              placeholder="Pilih tag"
              @change="handleTagFilter"
            >
              <el-option label="VIP" value="VIP" />
              <el-option label="Nasabah Prioritas" value="PRIORITAS" />
              <el-option label="Blacklist Watch" value="WATCH" />
              <el-option label="Korporat" value="KORPORAT" />
            </el-select>
          </FormField>
        </FilterPanel>
      </div>

      <!-- Results Table -->
      <CustomerTable
        :customers="customerStore.customers"
        :loading="customerStore.loading"
        :current-page="customerStore.currentPage + 1"
        :page-size="customerStore.pageSize"
        :can-edit="canWriteCustomer"
        :show-monthly-income="true"
        @view="handleView"
        @edit="handleEdit"
        @sort="handleSort"
      />

      <!-- Pagination -->
      <PaginationBar
        :page="customerStore.currentPage + 1"
        :page-size="customerStore.pageSize"
        :total="customerStore.totalElements"
        @update:page="customerStore.setPage($event - 1)"
        @update:page-size="(s) => { customerStore.pageSize = s; customerStore.search(); }"
        @change="({ page, pageSize }) => {
          customerStore.setPage(page - 1);
        }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useCustomerStore } from '~/stores/customer';
import { usePermissions } from '~/composables/usePermissions';
import {
  CUSTOMER_TYPES,
  KYC_STATUSES,
  RISK_PROFILES,
  CUSTOMER_STATUSES,
} from '~/types/customer';
import type { Customer } from '~/types/customer';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
});

const route = useRoute();
const customerStore = useCustomerStore();
const { canWriteCustomer } = usePermissions();

const filterOpen = ref(false);
const tagFilter = ref<string[]>([]);

const customers = computed(() => customerStore.customers);
const customerTypes = CUSTOMER_TYPES;
const kycStatuses = KYC_STATUSES;
const riskProfiles = RISK_PROFILES;
const cifStatuses = CUSTOMER_STATUSES;

const activeFilterCount = computed(() => {
  let count = 0;
  if (customerStore.searchQuery) count++;
  if (customerStore.hasFilters) {
    count += Object.values(customerStore.filters).filter(
      (v) => v !== undefined && v !== null && v !== ''
    ).length;
  }
  return count;
});

function handleSearch(query: string) {
  customerStore.searchQuery = query;
  customerStore.currentPage = 0;
  customerStore.search();
}

function handleClear() {
  customerStore.resetFilters();
  tagFilter.value = [];
}

function handleClearFilters() {
  customerStore.resetFilters();
  tagFilter.value = [];
}

function handleTagFilter(tags: string[]) {
  // Tag filtering
}

function handleView(customer: Customer) {
  navigateTo(`/customers/${customer.id}`);
}

function handleEdit(customer: Customer) {
  navigateTo(`/customers/${customer.id}/edit`);
}

function handleSort({ field, order }: { field: string; order: 'ascending' | 'descending' | null }) {
  if (order) {
    customerStore.setSort(field, order === 'ascending' ? 'asc' : 'desc');
  }
}

function exportData() {
  // Trigger export
  const csv = [
    ['CIF', 'Nama', 'Tipe', 'KYC', 'Risk', 'Status'],
    ...customers.value.map((c) => [
      c.cifNumber,
      c.fullName || '',
      c.customerType,
      c.kycStatus,
      c.riskProfile || '',
      c.cifStatus,
    ]),
  ]
    .map((row) => row.join(','))
    .join('\n');

  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `customers-${new Date().toISOString().slice(0, 10)}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

onMounted(() => {
  // If we have a query param, use it
  if (route.query.q) {
    customerStore.searchQuery = route.query.q as string;
  }
  customerStore.search();
});
</script>

<style scoped>
.customers-page {
  min-height: 100vh;
}

.page-content {
  padding: 24px 32px;
}

.search-section {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
