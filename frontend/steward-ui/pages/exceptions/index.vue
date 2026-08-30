<template>
  <div class="exceptions-page">
    <PageHeader
      title="Exception Queue"
      subtitle="Kelola exception & error yang memerlukan tindak lanjut"
    >
      <template #actions>
        <el-button @click="refresh">🔄 Refresh</el-button>
        <el-button type="primary" @click="exportExceptions">📥 Export</el-button>
      </template>
    </PageHeader>

    <div class="page-content">
      <!-- Stats -->
      <div class="stats-row">
        <StatCard
          label="Total Open"
          :value="formatNumber(stats.totalOpen)"
          icon="📋"
          color="#ea580c"
        />
        <StatCard
          label="Critical"
          :value="formatNumber(stats.critical)"
          icon="🚨"
          color="#dc2626"
        />
        <StatCard
          label="SLA Breach"
          :value="formatNumber(stats.slaBreach)"
          icon="⏰"
          color="#dc2626"
        />
        <StatCard
          label="Avg Resolution"
          :value="`${stats.avgResolution}h`"
          icon="⚡"
          color="#16a34a"
        />
      </div>

      <!-- Filter -->
      <FilterPanel
        v-model="filterOpen"
        :active-count="activeFilterCount"
        @clear="clearFilters"
      >
        <FormField label="Severity">
          <el-select v-model="filters.severity" placeholder="Semua" clearable>
            <el-option label="Critical" value="CRITICAL" />
            <el-option label="High" value="HIGH" />
            <el-option label="Medium" value="MEDIUM" />
            <el-option label="Low" value="LOW" />
          </el-select>
        </FormField>
        <FormField label="Status">
          <el-select v-model="filters.status" placeholder="Semua" clearable>
            <el-option label="Open" value="OPEN" />
            <el-option label="Assigned" value="ASSIGNED" />
            <el-option label="In Progress" value="IN_PROGRESS" />
            <el-option label="Resolved" value="RESOLVED" />
          </el-select>
        </FormField>
        <FormField label="Assigned to me">
          <el-switch v-model="filters.assignedToMe" />
        </FormField>
      </FilterPanel>

      <!-- Exception list -->
      <div class="exception-list">
        <ExceptionCard
          v-for="ex in exceptions"
          :key="ex.id"
          :exception="ex"
          @view="viewException"
          @assign="assignToMe"
          @resolve="resolveException"
        />
        <EmptyState
          v-if="!loading && exceptions.length === 0"
          icon="🎉"
          title="Tidak ada exception"
          description="Semua exception telah ditangani."
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue';
import { useNotificationStore } from '~/stores/notification';
import { useFormat } from '~/composables/useFormat';
import type { Exception } from '~/components/business/ExceptionCard.vue';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
});

const notificationStore = useNotificationStore();
const { formatNumber } = useFormat();

const filterOpen = ref(false);
const loading = ref(false);
const filters = reactive({
  severity: undefined as string | undefined,
  status: undefined as string | undefined,
  assignedToMe: false,
});

const stats = reactive({
  totalOpen: 12,
  critical: 3,
  slaBreach: 2,
  avgResolution: 4.2,
});

const exceptions = ref<Exception[]>([
  {
    id: 'EXC-2026-0001',
    title: 'ETL Sync Gagal - Source System CBS',
    description: 'Sync data dari Core Banking System gagal sejak 30 menit yang lalu. 5,234 record belum tersinkronisasi.',
    type: 'ETL_FAILURE',
    severity: 'CRITICAL',
    priority: 'URGENT',
    status: 'OPEN',
    entity: 'ETLJob',
    entityId: 'cbs-customer-sync-001',
    reportedAt: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
    reportedBy: 'system',
    tags: ['ETL', 'CBS', 'PRODUCTION'],
    slaDeadline: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
  },
  {
    id: 'EXC-2026-0002',
    title: 'Match Group Stuck in Review > 7 days',
    description: 'Match group MATCH-2026-00045 belum di-review oleh steward yang ditugaskan selama 7 hari.',
    type: 'SLA_BREACH',
    severity: 'HIGH',
    priority: 'HIGH',
    status: 'ASSIGNED',
    entity: 'MatchGroup',
    entityId: 'MATCH-2026-00045',
    reportedAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
    assignedTo: 'Andi Wijaya',
    assignedAt: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString(),
    tags: ['MATCHING', 'SLA'],
    slaDeadline: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'EXC-2026-0003',
    title: 'KYC Document Expiring - Customer CIF-20260115-00456',
    description: 'Dokumen KTP akan expired dalam 14 hari. Customer perlu di-notifikasi untuk update dokumen.',
    type: 'KYC_EXPIRING',
    severity: 'MEDIUM',
    priority: 'NORMAL',
    status: 'OPEN',
    entity: 'Customer',
    entityId: 'CIF-20260115-00456',
    reportedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    reportedBy: 'system',
    tags: ['KYC', 'EXPIRY'],
    slaDeadline: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'EXC-2026-0004',
    title: 'Duplicate Customer Terdeteksi - Budi Santoso',
    description: 'Customer baru dibuat dengan NIK yang sudah ada di sistem. Kemungkinan duplikat.',
    type: 'DUPLICATE_DETECTED',
    severity: 'HIGH',
    priority: 'HIGH',
    status: 'OPEN',
    entity: 'Customer',
    entityId: 'CIF-20260126-00045',
    reportedAt: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
    reportedBy: 'Andi Wijaya',
    tags: ['DUPLICATE', 'NEW_CUSTOMER'],
  },
]);

const activeFilterCount = computed(() => {
  let count = 0;
  Object.values(filters).forEach((v) => {
    if (v !== undefined && v !== null && v !== '' && v !== false) count++;
  });
  return count;
});

function viewException(ex: Exception) {
  notificationStore.showInfo(`Opening detail for ${ex.id}`);
}

function assignToMe(ex: Exception) {
  ex.assignedTo = 'You';
  ex.status = 'ASSIGNED';
  notificationStore.showSuccess(`${ex.id} assigned to you`);
}

function resolveException(ex: Exception) {
  ex.status = 'RESOLVED';
  ex.resolvedAt = new Date().toISOString();
  notificationStore.showSuccess(`${ex.id} resolved`);
}

function clearFilters() {
  filters.severity = undefined;
  filters.status = undefined;
  filters.assignedToMe = false;
}

function refresh() {
  notificationStore.showInfo('Refreshing exceptions...');
}

function exportExceptions() {
  notificationStore.showInfo('Exporting exceptions...');
}

onMounted(() => {});
</script>

<style scoped>
.exceptions-page {
  min-height: 100vh;
}

.page-content {
  padding: 24px 32px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.exception-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
  margin-top: 16px;
}
</style>
