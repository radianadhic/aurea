<template>
  <div class="customer-table-wrapper">
    <el-table
      :data="customers"
      :loading="loading"
      :default-sort="defaultSort"
      :row-key="rowKey"
      stripe
      border
      style="width: 100%"
      @row-click="handleRowClick"
      @sort-change="handleSortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column v-if="selectable" type="selection" width="48" />
      <el-table-column type="index" label="No" width="56" :index="indexMethod" />

      <el-table-column
        prop="cifNumber"
        label="CIF"
        width="120"
        sortable="custom"
        fixed="left"
      >
        <template #default="{ row }">
          <span class="cif-number">{{ row.cifNumber }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fullName"
        label="Nama Lengkap"
        min-width="200"
        sortable="custom"
      >
        <template #default="{ row }">
          <div class="customer-name-cell">
            <div class="customer-avatar" :style="{ background: avatarColor(row.id) }">
              {{ getInitials(row.fullName) }}
            </div>
            <div>
              <div class="customer-name">{{ row.fullName }}</div>
              <div class="customer-meta">
                <span v-if="row.occupation">{{ row.occupation }}</span>
                <span v-if="row.nationality">· {{ row.nationality }}</span>
              </div>
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="customerType" label="Tipe" width="120" sortable="custom">
        <template #default="{ row }">
          <el-tag size="small" :type="row.customerType === 'INDIVIDUAL' ? '' : 'warning'">
            {{ customerTypeLabel(row.customerType) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column
        prop="kycStatus"
        label="KYC"
        width="120"
        sortable="custom"
      >
        <template #default="{ row }">
          <el-tag
            size="small"
            :type="kycTagType(row.kycStatus)"
          >
            {{ kycStatusLabel(row.kycStatus) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column
        prop="riskProfile"
        label="Risk"
        width="100"
        sortable="custom"
      >
        <template #default="{ row }">
          <span class="risk-badge" :class="`risk-${row.riskProfile?.toLowerCase()}`">
            <span class="risk-dot"></span>
            {{ riskLabel(row.riskProfile) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column prop="cifStatus" label="Status" width="120" sortable="custom">
        <template #default="{ row }">
          <span :class="`status-badge status-${row.cifStatus?.toLowerCase()}`">
            {{ statusLabel(row.cifStatus) }}
          </span>
        </template>
      </el-table-column>

      <el-table-column prop="branchName" label="Cabang" width="150">
        <template #default="{ row }">
          <span class="branch">{{ row.branchName || '-' }}</span>
        </template>
      </el-table-column>

      <el-table-column
        v-if="showMonthlyIncome"
        prop="monthlyIncome"
        label="Income/bulan"
        width="140"
        sortable="custom"
        align="right"
      >
        <template #default="{ row }">
          {{ formatCurrency(row.monthlyIncome) }}
        </template>
      </el-table-column>

      <el-table-column
        prop="updatedAt"
        label="Last Update"
        width="140"
        sortable="custom"
      >
        <template #default="{ row }">
          <div>{{ formatDate(row.updatedAt) }}</div>
          <div class="meta-time">{{ formatRelative(row.updatedAt) }}</div>
        </template>
      </el-table-column>

      <el-table-column
        v-if="showActions"
        label="Aksi"
        width="120"
        fixed="right"
      >
        <template #default="{ row }">
          <el-button text type="primary" size="small" @click.stop="handleView(row)">
            Detail
          </el-button>
          <el-button
            v-if="canEdit"
            text
            type="primary"
            size="small"
            @click.stop="handleEdit(row)"
          >
            Edit
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useFormat } from '~/composables/useFormat';
import type { Customer, KycStatus, RiskProfile, CustomerStatus, CustomerType } from '~/types/customer';

interface Props {
  customers: Customer[];
  loading?: boolean;
  selectable?: boolean;
  showActions?: boolean;
  showMonthlyIncome?: boolean;
  canEdit?: boolean;
  currentPage?: number;
  pageSize?: number;
  defaultSortField?: string;
  defaultSortOrder?: 'ascending' | 'descending';
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  selectable: false,
  showActions: true,
  showMonthlyIncome: false,
  canEdit: true,
  currentPage: 1,
  pageSize: 20,
  defaultSortField: 'fullName',
  defaultSortOrder: 'ascending',
});

const emit = defineEmits<{
  (e: 'view', customer: Customer): void;
  (e: 'edit', customer: Customer): void;
  (e: 'sort', payload: { field: string; order: 'ascending' | 'descending' | null }): void;
  (e: 'selection-change', selection: Customer[]): void;
  (e: 'row-click', customer: Customer): void;
}>();

const { formatCurrency, formatDate, formatRelative, getInitials } = useFormat();

const defaultSort = computed(() => ({
  prop: props.defaultSortField,
  order: props.defaultSortOrder,
}));

const rowKey = (row: Customer) => row.id;

function indexMethod(index: number) {
  return (props.currentPage - 1) * props.pageSize + index + 1;
}

function avatarColor(id: string) {
  const colors = ['#1e40af', '#d97706', '#16a34a', '#dc2626', '#0284c7', '#7c3aed', '#db2777'];
  let hash = 0;
  for (let i = 0; i < id.length; i++) {
    hash = id.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
}

function customerTypeLabel(type: CustomerType) {
  const labels: Record<CustomerType, string> = {
    INDIVIDUAL: 'Individual',
    CORPORATE: 'Corporate',
    SYARIAH: 'Syariah',
  };
  return labels[type] || type;
}

function kycStatusLabel(status: KycStatus) {
  const labels: Record<KycStatus, string> = {
    PENDING: 'Pending',
    IN_REVIEW: 'In Review',
    APPROVED: 'Approved',
    REJECTED: 'Rejected',
    EXPIRED: 'Expired',
    FAILED: 'Failed',
  };
  return labels[status] || status;
}

function kycTagType(status: KycStatus) {
  const types: Record<KycStatus, '' | 'success' | 'warning' | 'danger' | 'info'> = {
    PENDING: 'warning',
    IN_REVIEW: 'warning',
    APPROVED: 'success',
    REJECTED: 'danger',
    EXPIRED: 'info',
    FAILED: 'danger',
  };
  return types[status] || '';
}

function riskLabel(risk?: RiskProfile) {
  if (!risk) return '-';
  return risk.charAt(0) + risk.slice(1).toLowerCase();
}

function statusLabel(status: CustomerStatus) {
  const labels: Record<CustomerStatus, string> = {
    ACTIVE: 'Active',
    DORMANT: 'Dormant',
    CLOSED: 'Closed',
    BLACKLIST: 'Blacklist',
    DECEASED: 'Deceased',
    SUSPENDED: 'Suspended',
  };
  return labels[status] || status;
}

function handleView(customer: Customer) {
  emit('view', customer);
}

function handleEdit(customer: Customer) {
  emit('edit', customer);
}

function handleRowClick(row: Customer) {
  emit('row-click', row);
}

function handleSortChange({ prop, order }: any) {
  emit('sort', { field: prop, order });
}

function handleSelectionChange(selection: Customer[]) {
  emit('selection-change', selection);
}
</script>

<style scoped>
.customer-table-wrapper {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.cif-number {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 600;
  color: #1e40af;
}

.customer-name-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.customer-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 12px;
  flex-shrink: 0;
}

.customer-name {
  font-weight: 500;
  color: #111827;
  font-size: 14px;
}

.customer-meta {
  font-size: 12px;
  color: #6b7280;
}

.risk-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
}

.risk-low {
  background: rgba(22, 163, 74, 0.1);
  color: #15803d;
}

.risk-medium {
  background: rgba(234, 88, 12, 0.1);
  color: #c2410c;
}

.risk-high {
  background: rgba(220, 38, 38, 0.1);
  color: #b91c1c;
}

.risk-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-active {
  background: rgba(22, 163, 74, 0.1);
  color: #15803d;
}

.status-dormant {
  background: rgba(2, 132, 199, 0.1);
  color: #075985;
}

.status-closed {
  background: #e5e7eb;
  color: #374151;
}

.status-blacklist {
  background: rgba(220, 38, 38, 0.1);
  color: #b91c1c;
}

.status-deceased {
  background: #e5e7eb;
  color: #4b5563;
}

.status-suspended {
  background: rgba(234, 88, 12, 0.1);
  color: #c2410c;
}

.branch {
  font-size: 13px;
  color: #374151;
}

.meta-time {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 2px;
}
</style>
