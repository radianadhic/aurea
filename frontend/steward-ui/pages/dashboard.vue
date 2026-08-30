<template>
  <div class="dashboard">
    <PageHeader
      title="Dashboard"
      :subtitle="`Selamat datang kembali, ${authStore.fullName}! Berikut ringkasan aktivitas hari ini.`"
    >
      <template #actions>
        <el-button @click="refreshData" :loading="loading">
          🔄 Refresh
        </el-button>
        <el-button type="primary" @click="navigateTo('/customers/new')">
          ➕ Nasabah Baru
        </el-button>
      </template>
    </PageHeader>

    <div class="dashboard-content">
      <!-- Stat Cards -->
      <div class="stat-grid">
        <StatCard
          label="Total Nasabah"
          :value="formatNumber(stats.totalCustomers)"
          icon="👥"
          color="#1e40af"
          :trend="8.2"
          trend-period="vs bulan lalu"
          :sub-value="`${formatNumber(stats.activeCustomers)} aktif`"
        />
        <StatCard
          label="KYC Pending"
          :value="formatNumber(stats.kycPending)"
          icon="📋"
          color="#d97706"
          :trend="-12.5"
          trend-period="vs minggu lalu"
          :sub-value="`${formatNumber(stats.kycExpiring)} akan expired`"
        />
        <StatCard
          label="Match Queue"
          :value="formatNumber(stats.matchQueue)"
          icon="🔄"
          color="#0284c7"
          :sub-value="`${formatNumber(stats.matchAutoMerged)} auto-merged hari ini`"
        />
        <StatCard
          label="Exceptions"
          :value="formatNumber(stats.exceptions)"
          icon="⚠️"
          color="#dc2626"
          :trend="3.1"
          trend-period="vs kemarin"
          :sub-value="`${formatNumber(stats.exceptionsCritical)} critical`"
        />
      </div>

      <!-- Charts Row -->
      <div class="dashboard-row">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Pertumbuhan Nasabah (12 bulan)</h3>
            <el-radio-group v-model="growthPeriod" size="small" @change="loadGrowthChart">
              <el-radio-button label="month">Bulanan</el-radio-button>
              <el-radio-button label="week">Mingguan</el-radio-button>
            </el-radio-group>
          </div>
          <LineChart
            :categories="growthData.categories"
            :series="growthData.series"
            height="280px"
          />
        </div>

        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Distribusi Risk Profile</h3>
          </div>
          <PieChart
            :data="riskDistribution"
            height="280px"
            :show-legend="true"
            :donut="true"
          />
        </div>
      </div>

      <!-- More Stats -->
      <div class="dashboard-row">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Aktivitas Matching (7 hari)</h3>
          </div>
          <BarChart
            :categories="matchingData.categories"
            :series="matchingData.series"
            height="240px"
          />
        </div>

        <div class="card">
          <div class="card-header">
            <h3 class="card-title">KYC Status</h3>
            <NuxtLink to="/kyc" class="view-all">Lihat semua →</NuxtLink>
          </div>
          <div class="kyc-summary">
            <div
              v-for="(item, idx) in kycSummary"
              :key="idx"
              class="kyc-item"
            >
              <div class="kyc-info">
                <div class="kyc-status-name">{{ item.label }}</div>
                <div class="kyc-count">{{ formatNumber(item.count) }}</div>
              </div>
              <el-progress
                :percentage="item.percentage"
                :color="item.color"
                :show-text="false"
                :stroke-width="8"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Aktivitas Terbaru</h3>
          <NuxtLink to="/audit" class="view-all">Lihat audit trail →</NuxtLink>
        </div>
        <el-table :data="recentActivity" stripe style="width: 100%">
          <el-table-column prop="timestamp" label="Waktu" width="180">
            <template #default="{ row }">
              <div>{{ formatDateTime(row.timestamp) }}</div>
              <div class="meta-time">{{ formatRelative(row.timestamp) }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="user" label="User" width="180">
            <template #default="{ row }">
              <div class="user-cell">
                <div class="user-avatar-sm">{{ getInitials(row.user) }}</div>
                <span>{{ row.user }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="action" label="Aksi" width="200">
            <template #default="{ row }">
              <el-tag size="small" :type="getActionType(row.action)">
                {{ row.action }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="entity" label="Entity" min-width="200" />
          <el-table-column prop="entityId" label="ID" width="160">
            <template #default="{ row }">
              <span class="mono">{{ row.entityId }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useFormat } from '~/composables/useFormat';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
});

const authStore = useAuthStore();
const { formatNumber, formatDateTime, formatRelative, getInitials } = useFormat();

const loading = ref(false);
const growthPeriod = ref('month');

const stats = reactive({
  totalCustomers: 1_245_872,
  activeCustomers: 1_187_203,
  kycPending: 234,
  kycExpiring: 56,
  matchQueue: 89,
  matchAutoMerged: 23,
  exceptions: 12,
  exceptionsCritical: 3,
});

const growthData = reactive({
  categories: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
  series: [
    {
      name: 'Nasabah Baru',
      data: [1240, 1340, 1580, 1420, 1690, 1820, 1950, 2110, 2280, 2420, 2610, 2890],
    },
    {
      name: 'Update Data',
      data: [820, 940, 1010, 1180, 1340, 1420, 1480, 1610, 1720, 1850, 1980, 2120],
    },
  ],
});

const riskDistribution = ref([
  { name: 'Low Risk', value: 985_320 },
  { name: 'Medium Risk', value: 198_400 },
  { name: 'High Risk', value: 62_152 },
]);

const matchingData = reactive({
  categories: ['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'],
  series: [
    { name: 'Auto-merged', data: [42, 56, 38, 64, 51, 28, 18] },
    { name: 'Manual Review', data: [12, 18, 15, 22, 14, 8, 4] },
    { name: 'Rejected', data: [3, 5, 4, 6, 4, 2, 1] },
  ],
});

const kycSummary = ref([
  { label: 'Approved', count: 1_187_203, percentage: 95.3, color: '#16a34a' },
  { label: 'Pending', count: 234, percentage: 0.02, color: '#d97706' },
  { label: 'In Review', count: 124, percentage: 0.01, color: '#0284c7' },
  { label: 'Expired', count: 56, percentage: 0.005, color: '#9ca3af' },
  { label: 'Rejected', count: 38, percentage: 0.003, color: '#dc2626' },
]);

const recentActivity = ref([
  {
    timestamp: new Date(Date.now() - 1000 * 60 * 5),
    user: 'Budi Santoso',
    action: 'CUSTOMER_CREATE',
    entity: 'Customer',
    entityId: 'CIF-20260126-00045',
  },
  {
    timestamp: new Date(Date.now() - 1000 * 60 * 12),
    user: 'Siti Aminah',
    action: 'KYC_APPROVE',
    entity: 'Customer',
    entityId: 'CIF-20260126-00044',
  },
  {
    timestamp: new Date(Date.now() - 1000 * 60 * 23),
    user: 'system',
    action: 'MATCH_AUTO',
    entity: 'Match Group',
    entityId: 'MATCH-20260126-00012',
  },
  {
    timestamp: new Date(Date.now() - 1000 * 60 * 35),
    user: 'Andi Wijaya',
    action: 'CUSTOMER_UPDATE',
    entity: 'Customer',
    entityId: 'CIF-20260125-00198',
  },
  {
    timestamp: new Date(Date.now() - 1000 * 60 * 47),
    user: 'Dewi Lestari',
    action: 'MATCH_MERGE',
    entity: 'Match Group',
    entityId: 'MATCH-20260126-00011',
  },
]);

function getActionType(action: string): '' | 'success' | 'warning' | 'danger' | 'info' {
  const types: Record<string, '' | 'success' | 'warning' | 'danger' | 'info'> = {
    CUSTOMER_CREATE: 'success',
    CUSTOMER_UPDATE: 'info',
    CUSTOMER_DELETE: 'danger',
    KYC_APPROVE: 'success',
    KYC_REJECT: 'danger',
    MATCH_AUTO: 'info',
    MATCH_MERGE: 'warning',
    BLACKLIST_ADD: 'danger',
  };
  return types[action] || '';
}

async function refreshData() {
  loading.value = true;
  try {
    await new Promise((r) => setTimeout(r, 800));
  } finally {
    loading.value = false;
  }
}

function loadGrowthChart() {
  // Toggle chart data
}

onMounted(() => {
  // Load dashboard data
});
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
}

.dashboard-content {
  padding: 24px 32px;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.dashboard-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

@media (max-width: 1024px) {
  .dashboard-row {
    grid-template-columns: 1fr;
  }
}

.card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 20px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.view-all {
  font-size: 13px;
  color: #1e40af;
  text-decoration: none;
}

.view-all:hover {
  text-decoration: underline;
}

.kyc-summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.kyc-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.kyc-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.kyc-status-name {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.kyc-count {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.user-avatar-sm {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #1e40af;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
}

.mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #6b7280;
}

.meta-time {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 2px;
}
</style>
