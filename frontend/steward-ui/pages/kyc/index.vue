<template>
  <div class="kyc-page">
    <PageHeader
      title="KYC Review"
      subtitle="Review dan setujui/tolak KYC nasabah"
    >
      <template #actions>
        <el-button @click="refresh">🔄 Refresh</el-button>
      </template>
    </PageHeader>

    <div class="page-content">
      <!-- Stats -->
      <div class="stats-row">
        <StatCard
          label="Pending"
          :value="formatNumber(stats.pending)"
          icon="⏳"
          color="#d97706"
        />
        <StatCard
          label="In Review"
          :value="formatNumber(stats.inReview)"
          icon="👀"
          color="#0284c7"
        />
        <StatCard
          label="Approved (MTD)"
          :value="formatNumber(stats.approved)"
          icon="✅"
          color="#16a34a"
        />
        <StatCard
          label="Expiring Soon"
          :value="formatNumber(stats.expiring)"
          icon="⏰"
          color="#dc2626"
        />
      </div>

      <!-- Filter -->
      <FilterPanel
        v-model="filterOpen"
        :active-count="activeFilterCount"
        @clear="clearFilters"
      >
        <FormField label="Status">
          <el-select v-model="filters.kycStatus" placeholder="Semua" clearable>
            <el-option label="Pending" value="PENDING" />
            <el-option label="In Review" value="IN_REVIEW" />
            <el-option label="Approved" value="APPROVED" />
            <el-option label="Rejected" value="REJECTED" />
            <el-option label="Expired" value="EXPIRED" />
          </el-select>
        </FormField>
        <FormField label="KYC Level">
          <el-select v-model="filters.kycLevel" placeholder="Semua" clearable>
            <el-option label="Simplified" value="SIMPLIFIED" />
            <el-option label="Standard" value="STANDARD" />
            <el-option label="Enhanced" value="ENHANCED" />
          </el-select>
        </FormField>
        <FormField label="PEP Only">
          <el-switch v-model="filters.pepOnly" />
        </FormField>
        <FormField label="Sanctions Match">
          <el-switch v-model="filters.sanctionsOnly" />
        </FormField>
      </FilterPanel>

      <!-- KYC list -->
      <div class="kyc-list">
        <KycCaseCard
          v-for="kycCase in cases"
          :key="kycCase.id"
          :case="kycCase"
          @view="viewCase"
          @approve="approveCase"
          @reject="rejectCase"
        />
        <EmptyState
          v-if="!loading && cases.length === 0"
          icon="✅"
          title="Tidak ada KYC yang perlu di-review"
          description="Semua KYC telah ditangani."
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue';
import { useNotificationStore } from '~/stores/notification';
import { useFormat } from '~/composables/useFormat';
import type { KycCase } from '~/stores/kyc';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
  roles: ['STEWARD_CIF', 'COMPLIANCE', 'ADMIN', 'SUPER_ADMIN'],
});

const notificationStore = useNotificationStore();
const { formatNumber } = useFormat();

const filterOpen = ref(false);
const loading = ref(false);
const filters = reactive({
  kycStatus: undefined as string | undefined,
  kycLevel: undefined as string | undefined,
  pepOnly: false,
  sanctionsOnly: false,
});

const stats = reactive({
  pending: 234,
  inReview: 56,
  approved: 1247,
  expiring: 23,
});

const cases = ref<KycCase[]>([
  {
    id: 'KYC-2026-0001',
    cifNumber: 'CIF-20260126-00045',
    customerName: 'Budi Santoso',
    customerId: 'cust-001',
    kycStatus: 'IN_REVIEW',
    kycLevel: 'STANDARD',
    riskScore: 35,
    pepStatus: false,
    sanctionsStatus: 'CLEAR',
    documentCompleteness: 95,
    daysSinceLastUpdate: 2,
    assignedTo: 'Siti Aminah',
    submittedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    documents: [
      { id: '1', type: 'KTP', fileName: 'ktp.pdf', fileSize: 1024000, uploadedAt: '2026-01-25', verified: true, url: '' },
      { id: '2', type: 'NPWP', fileName: 'npwp.pdf', fileSize: 512000, uploadedAt: '2026-01-25', verified: true, url: '' },
      { id: '3', type: 'SELFIE', fileName: 'selfie.jpg', fileSize: 2048000, uploadedAt: '2026-01-25', verified: true, url: '' },
    ],
    flags: [],
  },
  {
    id: 'KYC-2026-0002',
    cifNumber: 'CIF-20260125-00198',
    customerName: 'Andi Pratama',
    customerId: 'cust-002',
    kycStatus: 'PENDING',
    kycLevel: 'ENHANCED',
    riskScore: 78,
    pepStatus: true,
    sanctionsStatus: 'POTENTIAL_MATCH',
    documentCompleteness: 75,
    daysSinceLastUpdate: 5,
    submittedAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    documents: [
      { id: '1', type: 'KTP', fileName: 'ktp.pdf', fileSize: 1024000, uploadedAt: '2026-01-21', verified: true, url: '' },
      { id: '2', type: 'PASSPORT', fileName: 'passport.pdf', fileSize: 768000, uploadedAt: '2026-01-21', verified: false, url: '' },
      { id: '3', type: 'PROOF_OF_ADDRESS', fileName: 'pln.pdf', fileSize: 256000, uploadedAt: '2026-01-22', verified: true, url: '' },
    ],
    flags: ['PEP', 'Sanctions Potential Match', 'High Risk Country'],
  },
  {
    id: 'KYC-2026-0003',
    cifNumber: 'CIF-20260120-00145',
    customerName: 'Siti Aminah',
    customerId: 'cust-003',
    kycStatus: 'PENDING',
    kycLevel: 'STANDARD',
    riskScore: 25,
    pepStatus: false,
    sanctionsStatus: 'CLEAR',
    documentCompleteness: 100,
    daysSinceLastUpdate: 1,
    submittedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    documents: [
      { id: '1', type: 'KTP', fileName: 'ktp.pdf', fileSize: 1024000, uploadedAt: '2026-01-25', verified: true, url: '' },
      { id: '2', type: 'NPWP', fileName: 'npwp.pdf', fileSize: 512000, uploadedAt: '2026-01-25', verified: true, url: '' },
      { id: '3', type: 'SELFIE', fileName: 'selfie.jpg', fileSize: 2048000, uploadedAt: '2026-01-25', verified: true, url: '' },
    ],
    flags: [],
  },
]);

const activeFilterCount = computed(() => {
  let count = 0;
  Object.values(filters).forEach((v) => {
    if (v !== undefined && v !== null && v !== '' && v !== false) count++;
  });
  return count;
});

function viewCase(kycCase: KycCase) {
  notificationStore.showInfo(`Opening KYC ${kycCase.id}`);
}

function approveCase(kycCase: KycCase) {
  kycCase.kycStatus = 'APPROVED';
  notificationStore.showSuccess(`KYC ${kycCase.id} disetujui`);
}

function rejectCase(kycCase: KycCase) {
  kycCase.kycStatus = 'REJECTED';
  notificationStore.showWarning(`KYC ${kycCase.id} ditolak`);
}

function clearFilters() {
  filters.kycStatus = undefined;
  filters.kycLevel = undefined;
  filters.pepOnly = false;
  filters.sanctionsOnly = false;
}

function refresh() {
  notificationStore.showInfo('Refreshing KYC queue...');
}

onMounted(() => {});
</script>

<style scoped>
.kyc-page {
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

.kyc-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
  margin-top: 16px;
}
</style>
