<template>
  <div class="customer-detail">
    <PageHeader
      :back="true"
      :title="customer?.fullName || 'Customer Detail'"
      :subtitle="`CIF: ${customer?.cifNumber || '-'}`"
      @back="navigateTo('/customers')"
    >
      <template #actions>
        <el-button
          v-if="canWriteCustomer"
          @click="navigateTo(`/customers/${customerId}/edit`)"
        >
          ✏️ Edit
        </el-button>
        <el-button
          v-if="canMergeCustomer && !isBlacklisted"
          type="warning"
          @click="showMergeDialog = true"
        >
          🔄 Merge
        </el-button>
        <el-button
          v-if="canBlacklistCustomer && !isBlacklisted"
          type="danger"
          @click="showBlacklistDialog = true"
        >
          🚫 Blacklist
        </el-button>
        <el-dropdown>
          <el-button>
            ⋮ Lainnya
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="exportCustomer">📥 Export Data</el-dropdown-item>
              <el-dropdown-item @click="printCustomer">🖨️ Print</el-dropdown-item>
              <el-dropdown-item divided>
                <span class="text-error">🗑️ Hapus</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
    </PageHeader>

    <div v-if="loading" class="loading-section">
      <LoadingSpinner message="Memuat data nasabah..." />
    </div>

    <div v-else-if="customer" class="detail-content">
      <div class="detail-grid">
        <!-- Sidebar: Status Card -->
        <div class="status-card">
          <div class="status-avatar" :style="{ background: avatarColor }">
            {{ initials }}
          </div>
          <h2 class="status-name">{{ customer.fullName }}</h2>
          <div class="status-cif">{{ customer.cifNumber }}</div>

          <div class="status-tags">
            <el-tag :type="cifStatusType">{{ cifStatusLabel }}</el-tag>
            <el-tag :type="kycStatusType">{{ kycStatusLabel }}</el-tag>
            <el-tag v-if="customer.pepStatus" type="danger" effect="dark">PEP</el-tag>
          </div>

          <div class="status-meta">
            <div class="meta-row">
              <span class="meta-label">Tipe</span>
              <span class="meta-value">{{ customerTypeLabel }}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Risk</span>
              <span class="meta-value" :class="`risk-${customer.riskProfile?.toLowerCase()}`">
                {{ customer.riskProfile || '-' }}
              </span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Cabang</span>
              <span class="meta-value">{{ customer.branchName || '-' }}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Created</span>
              <span class="meta-value">{{ formatDate(customer.createdAt) }}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Last Update</span>
              <span class="meta-value">{{ formatRelative(customer.updatedAt) }}</span>
            </div>
          </div>
        </div>

        <!-- Main: Tabs -->
        <div class="main-content">
          <Tabs v-model="activeTab" :tabs="tabs">
            <!-- Personal -->
            <template #personal>
              <div class="tab-content">
                <h3 class="section-title">Informasi Pribadi</h3>
                <div class="info-grid">
                  <div class="info-item">
                    <span class="info-label">Nama Lengkap</span>
                    <span class="info-value">{{ customer.fullName }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Nama Legal</span>
                    <span class="info-value">{{ customer.legalName || '-' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Tempat Lahir</span>
                    <span class="info-value">{{ customer.placeOfBirth || '-' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Tanggal Lahir</span>
                    <span class="info-value">{{ formatDate(customer.dateOfBirth) }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Jenis Kelamin</span>
                    <span class="info-value">{{ genderLabel }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Kewarganegaraan</span>
                    <span class="info-value">{{ customer.nationality || '-' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Status Pernikahan</span>
                    <span class="info-value">{{ maritalStatusLabel }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Agama</span>
                    <span class="info-value">{{ customer.religion || '-' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Pekerjaan</span>
                    <span class="info-value">{{ customer.occupation || '-' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Pendapatan/Bulan</span>
                    <span class="info-value">{{ formatCurrency(customer.monthlyIncome) }}</span>
                  </div>
                </div>
              </div>
            </template>

            <!-- KYC -->
            <template #kyc>
              <div class="tab-content">
                <h3 class="section-title">Status KYC</h3>
                <div class="kyc-info">
                  <div class="kyc-row">
                    <span class="kyc-label">Status</span>
                    <el-tag :type="kycStatusType" size="large">{{ kycStatusLabel }}</el-tag>
                  </div>
                  <div class="kyc-row">
                    <span class="kyc-label">Berlaku Sampai</span>
                    <span class="kyc-value">{{ formatDate(customer.kycExpiryDate) }}</span>
                  </div>
                  <div class="kyc-row">
                    <span class="kyc-label">Risk Score</span>
                    <div class="risk-meter">
                      <el-progress
                        :percentage="customer.riskProfile === 'HIGH' ? 75 : customer.riskProfile === 'MEDIUM' ? 50 : 25"
                        :color="customer.riskProfile === 'HIGH' ? '#dc2626' : customer.riskProfile === 'MEDIUM' ? '#ea580c' : '#16a34a'"
                        :stroke-width="10"
                      />
                    </div>
                  </div>
                </div>

                <h3 class="section-title" style="margin-top: 24px;">Dokumen KYC</h3>
                <div class="docs-list">
                  <div v-for="doc in kycDocuments" :key="doc.id" class="doc-item">
                    <div class="doc-icon">{{ doc.icon }}</div>
                    <div class="doc-info">
                      <div class="doc-name">{{ doc.type }}</div>
                      <div class="doc-meta">{{ doc.fileName }} · {{ formatFileSize(doc.size) }}</div>
                    </div>
                    <el-tag :type="doc.verified ? 'success' : 'warning'" size="small">
                      {{ doc.verified ? '✓ Verified' : '⏳ Pending' }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </template>

            <!-- Audit -->
            <template #audit>
              <div class="tab-content">
                <h3 class="section-title">Riwayat Perubahan</h3>
                <Timeline :events="auditEvents" />
              </div>
            </template>

            <!-- Documents -->
            <template #documents>
              <div class="tab-content">
                <h3 class="section-title">Semua Dokumen</h3>
                <FileUpload
                  v-model="uploadedFiles"
                  :multiple="true"
                  :auto-upload="false"
                  drag
                  accept=".pdf,.jpg,.jpeg,.png"
                  :max-size="10 * 1024 * 1024"
                  drag-title="Drop file di sini atau klik untuk upload"
                  tip="PDF, JPG, PNG · Maks 10MB"
                />
              </div>
            </template>
          </Tabs>
        </div>
      </div>
    </div>

    <EmptyState
      v-else
      icon="🔍"
      title="Customer tidak ditemukan"
      description="Customer mungkin sudah dihapus atau Anda tidak memiliki akses."
    />

    <!-- Blacklist Dialog -->
    <Modal v-model="showBlacklistDialog" title="Blacklist Customer" size="md">
      <p>Yakin ingin menambahkan <strong>{{ customer?.fullName }}</strong> ke blacklist?</p>
      <FormField label="Alasan" required class="mt-3">
        <el-input v-model="blacklistReason" type="textarea" :rows="3" placeholder="Jelaskan alasan blacklist..." />
      </FormField>
      <template #footer>
        <el-button @click="showBlacklistDialog = false">Batal</el-button>
        <el-button type="danger" :loading="blacklisting" @click="handleBlacklist">
          Blacklist
        </el-button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCustomerStore } from '~/stores/customer';
import { useAuthStore } from '~/stores/auth';
import { useNotificationStore } from '~/stores/notification';
import { useFormat } from '~/composables/useFormat';
import { usePermissions } from '~/composables/usePermissions';
import type { Customer, CustomerType, KycStatus, CustomerStatus, Gender, MaritalStatus } from '~/types/customer';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
});

const route = useRoute();
const customerStore = useCustomerStore();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();
const { formatDate, formatRelative, formatCurrency, formatFileSize, getInitials } = useFormat();
const { canWriteCustomer, canMergeCustomer, canBlacklistCustomer } = usePermissions();

const customerId = computed(() => route.params.id as string);
const loading = ref(true);
const activeTab = ref(0);
const showBlacklistDialog = ref(false);
const showMergeDialog = ref(false);
const blacklisting = ref(false);
const blacklistReason = ref('');
const uploadedFiles = ref([]);

const customer = computed(() => customerStore.currentCustomer);

const isBlacklisted = computed(() => customer.value?.cifStatus === 'BLACKLIST');

const tabs = [
  { name: 'personal', label: 'Informasi Pribadi' },
  { name: 'kyc', label: 'KYC' },
  { name: 'audit', label: 'Audit Trail' },
  { name: 'documents', label: 'Dokumen' },
];

const initials = computed(() => getInitials(customer.value?.fullName));

const avatarColor = computed(() => {
  if (!customer.value) return '#1e40af';
  const colors = ['#1e40af', '#d97706', '#16a34a', '#dc2626', '#0284c7', '#7c3aed', '#db2777'];
  let hash = 0;
  for (let i = 0; i < customer.value.id.length; i++) {
    hash = customer.value.id.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
});

const cifStatusLabel = computed(() => {
  const labels: Record<CustomerStatus, string> = {
    ACTIVE: 'Aktif', DORMANT: 'Dormant', CLOSED: 'Ditutup',
    BLACKLIST: 'Blacklist', DECEASED: 'Meninggal', SUSPENDED: 'Suspended',
  };
  return customer.value ? labels[customer.value.cifStatus] : '-';
});

const cifStatusType = computed(() => {
  const types: Record<CustomerStatus, '' | 'success' | 'warning' | 'danger' | 'info'> = {
    ACTIVE: 'success', DORMANT: 'info', CLOSED: 'info',
    BLACKLIST: 'danger', DECEASED: 'info', SUSPENDED: 'warning',
  };
  return customer.value ? types[customer.value.cifStatus] : '';
});

const kycStatusLabel = computed(() => {
  const labels: Record<KycStatus, string> = {
    PENDING: 'Pending', IN_REVIEW: 'In Review', APPROVED: 'Disetujui',
    REJECTED: 'Ditolak', EXPIRED: 'Expired', FAILED: 'Gagal',
  };
  return customer.value ? labels[customer.value.kycStatus] : '-';
});

const kycStatusType = computed(() => {
  const types: Record<KycStatus, '' | 'success' | 'warning' | 'danger' | 'info'> = {
    PENDING: 'warning', IN_REVIEW: 'warning', APPROVED: 'success',
    REJECTED: 'danger', EXPIRED: 'info', FAILED: 'danger',
  };
  return customer.value ? types[customer.value.kycStatus] : '';
});

const customerTypeLabel = computed(() => {
  const labels: Record<CustomerType, string> = {
    INDIVIDUAL: 'Individual', CORPORATE: 'Corporate', SYARIAH: 'Syariah',
  };
  return customer.value ? labels[customer.value.customerType] : '-';
});

const genderLabel = computed(() => {
  const labels: Record<Gender, string> = { MALE: 'Laki-laki', FEMALE: 'Perempuan' };
  return customer.value?.gender ? labels[customer.value.gender] : '-';
});

const maritalStatusLabel = computed(() => {
  const labels: Record<MaritalStatus, string> = {
    SINGLE: 'Belum Menikah', MARRIED: 'Menikah', DIVORCED: 'Cerai', WIDOWED: 'Duda/Janda',
  };
  return customer.value?.maritalStatus ? labels[customer.value.maritalStatus] : '-';
});

const kycDocuments = ref([
  { id: '1', type: 'KTP', icon: '🪪', fileName: 'ktp_budi_santoso.pdf', size: 1024000, verified: true },
  { id: '2', type: 'NPWP', icon: '📋', fileName: 'npwp.pdf', size: 512000, verified: true },
  { id: '3', type: 'Selfie', icon: '🤳', fileName: 'selfie_verification.jpg', size: 2048000, verified: true },
  { id: '4', type: 'Proof of Address', icon: '🏠', fileName: 'pln_bill.pdf', size: 768000, verified: false },
]);

const auditEvents = ref([
  {
    id: '1',
    title: 'KYC Disetujui',
    description: 'Siti Aminah menyetujui KYC customer',
    time: '2 hari lalu',
    user: 'Siti Aminah',
    status: 'success' as const,
  },
  {
    id: '2',
    title: 'Data Nasabah Diperbarui',
    description: 'Nomor telepon diperbarui dari 081234567890 ke 081234567891',
    time: '5 hari lalu',
    user: 'Andi Wijaya',
    status: 'info' as const,
  },
  {
    id: '3',
    title: 'Customer Dibuat',
    description: 'Customer baru dibuat di sistem',
    time: '1 bulan lalu',
    user: 'Budi Santoso',
    status: 'success' as const,
  },
]);

async function handleBlacklist() {
  if (!blacklistReason.value) {
    notificationStore.showError('Alasan blacklist wajib diisi');
    return;
  }
  blacklisting.value = true;
  try {
    await new Promise((r) => setTimeout(r, 1000));
    notificationStore.showSuccess(`${customer.value?.fullName} telah di-blacklist`);
    showBlacklistDialog.value = false;
    await customerStore.fetchById(customerId.value);
  } finally {
    blacklisting.value = false;
  }
}

function exportCustomer() {
  notificationStore.showInfo('Mengekspor data customer...');
}

function printCustomer() {
  window.print();
}

onMounted(async () => {
  loading.value = true;
  try {
    await customerStore.fetchById(customerId.value);
  } catch (e) {
    notificationStore.showError('Gagal memuat data customer');
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.customer-detail {
  min-height: 100vh;
}

.loading-section {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.detail-content {
  padding: 24px 32px;
}

.detail-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}

.status-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 24px;
  text-align: center;
  position: sticky;
  top: 88px;
  height: fit-content;
}

.status-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 28px;
  margin: 0 auto 16px;
}

.status-name {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 4px;
}

.status-cif {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 16px;
}

.status-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f3f4f6;
}

.status-meta {
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.meta-label {
  color: #6b7280;
}

.meta-value {
  color: #111827;
  font-weight: 500;
}

.risk-low { color: #16a34a; }
.risk-medium { color: #ea580c; }
.risk-high { color: #dc2626; }

.main-content {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.tab-content {
  padding: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f3f4f6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 11px;
  text-transform: uppercase;
  color: #6b7280;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.info-value {
  font-size: 14px;
  color: #111827;
  font-weight: 500;
}

.kyc-info {
  background: #f9fafb;
  padding: 16px;
  border-radius: 8px;
}

.kyc-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #e5e7eb;
}

.kyc-row:last-child { border-bottom: 0; }

.kyc-label {
  font-size: 13px;
  color: #6b7280;
  min-width: 120px;
}

.kyc-value {
  font-size: 14px;
  color: #111827;
  font-weight: 500;
}

.risk-meter {
  flex: 1;
}

.docs-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

.doc-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.doc-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.doc-info {
  flex: 1;
  min-width: 0;
}

.doc-name {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.doc-meta {
  font-size: 11px;
  color: #6b7280;
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
