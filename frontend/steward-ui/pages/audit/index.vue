<template>
  <div class="audit-page">
    <PageHeader
      title="Audit Trail"
      subtitle="Log aktivitas sistem untuk compliance & security"
    >
      <template #actions>
        <el-button @click="exportCsv" :disabled="!canExportAudit">
          📥 Export CSV
        </el-button>
        <el-button type="primary" @click="exportPdf" :disabled="!canExportAudit">
          📄 Export PDF
        </el-button>
      </template>
    </PageHeader>

    <div class="page-content">
      <!-- Filter Bar -->
      <div class="filter-bar">
        <el-input
          v-model="auditStore.filters.username"
          placeholder="Cari username..."
          style="width: 200px;"
          clearable
        />
        <el-select v-model="auditStore.filters.action" placeholder="Action" style="width: 200px;" clearable>
          <el-option label="Customer Create" value="CUSTOMER_CREATE" />
          <el-option label="Customer Update" value="CUSTOMER_UPDATE" />
          <el-option label="Customer Delete" value="CUSTOMER_DELETE" />
          <el-option label="KYC Approve" value="KYC_APPROVE" />
          <el-option label="KYC Reject" value="KYC_REJECT" />
          <el-option label="Match Auto" value="MATCH_AUTO" />
          <el-option label="Match Merge" value="MATCH_MERGE" />
          <el-option label="Config Change" value="CONFIG_CHANGE" />
        </el-select>
        <el-select v-model="auditStore.filters.entity" placeholder="Entity" style="width: 160px;" clearable>
          <el-option label="Customer" value="Customer" />
          <el-option label="MatchGroup" value="MatchGroup" />
          <el-option label="KycCase" value="KycCase" />
          <el-option label="User" value="User" />
          <el-option label="Role" value="Role" />
          <el-option label="Config" value="Config" />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="datetimerange"
          range-separator="→"
          start-placeholder="Dari"
          end-placeholder="Sampai"
          style="width: 360px;"
          @change="handleDateChange"
        />
        <el-button type="primary" @click="auditStore.fetchEntries()">
          Cari
        </el-button>
      </div>

      <!-- Audit Table -->
      <el-table
        :data="auditStore.entries"
        :loading="auditStore.loading"
        stripe
        border
        style="width: 100%; margin-top: 16px;"
        @row-click="viewDetail"
      >
        <el-table-column prop="timestamp" label="Waktu" width="180">
          <template #default="{ row }">
            <div>{{ formatDateTime(row.timestamp) }}</div>
            <div class="meta-time">{{ formatRelative(row.timestamp) }}</div>
          </template>
        </el-table-column>

        <el-table-column prop="username" label="User" width="180">
          <template #default="{ row }">
            <div class="user-cell">
              <div class="user-avatar-sm">{{ getInitials(row.userFullName || row.username) }}</div>
              <div>
                <div>{{ row.userFullName || row.username }}</div>
                <div class="user-role-sm">{{ row.userRole }}</div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="action" label="Action" width="200">
          <template #default="{ row }">
            <el-tag size="small" :type="getActionType(row.action)">
              {{ row.action }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="entity" label="Entity" width="140" />

        <el-table-column prop="entityId" label="ID" min-width="180">
          <template #default="{ row }">
            <span class="mono">{{ row.entityId }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="ipAddress" label="IP" width="140">
          <template #default="{ row }">
            <span class="mono-sm">{{ row.ipAddress }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="result" label="Result" width="100">
          <template #default="{ row }">
            <el-tag size="small" :type="row.result === 'SUCCESS' ? 'success' : 'danger'">
              {{ row.result }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Changes" width="100" align="center">
          <template #default="{ row }">
            <el-button
              v-if="row.changes && row.changes.length"
              text
              type="primary"
              size="small"
              @click.stop="viewChanges(row)"
            >
              {{ row.changes.length }} field
            </el-button>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <PaginationBar
        :page="auditStore.currentPage + 1"
        :page-size="auditStore.pageSize"
        :total="auditStore.totalElements"
        @update:page="(p) => { auditStore.currentPage = p - 1; auditStore.fetchEntries(); }"
      />
    </div>

    <!-- Detail Dialog -->
    <el-dialog v-model="detailOpen" title="Audit Entry Detail" width="800px">
      <div v-if="selectedEntry" class="audit-detail">
        <div class="detail-header">
          <div>
            <h3>{{ selectedEntry.action }}</h3>
            <p class="text-muted">{{ formatDateTime(selectedEntry.timestamp) }}</p>
          </div>
          <el-tag :type="selectedEntry.result === 'SUCCESS' ? 'success' : 'danger'">
            {{ selectedEntry.result }}
          </el-tag>
        </div>

        <div class="detail-grid">
          <div class="detail-item">
            <label>User</label>
            <span>{{ selectedEntry.userFullName }} ({{ selectedEntry.username }})</span>
          </div>
          <div class="detail-item">
            <label>Role</label>
            <span>{{ selectedEntry.userRole }}</span>
          </div>
          <div class="detail-item">
            <label>IP Address</label>
            <span class="mono">{{ selectedEntry.ipAddress }}</span>
          </div>
          <div class="detail-item">
            <label>User Agent</label>
            <span class="mono-sm">{{ selectedEntry.userAgent }}</span>
          </div>
          <div class="detail-item">
            <label>Entity</label>
            <span>{{ selectedEntry.entity }}</span>
          </div>
          <div class="detail-item">
            <label>Entity ID</label>
            <span class="mono">{{ selectedEntry.entityId }}</span>
          </div>
          <div v-if="selectedEntry.sessionId" class="detail-item">
            <label>Session</label>
            <span class="mono-sm">{{ selectedEntry.sessionId }}</span>
          </div>
          <div v-if="selectedEntry.errorMessage" class="detail-item">
            <label>Error</label>
            <span class="text-error">{{ selectedEntry.errorMessage }}</span>
          </div>
        </div>

        <div v-if="selectedEntry.changes && selectedEntry.changes.length" class="changes-section">
          <h4>Changes</h4>
          <el-table :data="selectedEntry.changes" size="small" border>
            <el-table-column prop="field" label="Field" width="200" />
            <el-table-column label="Old Value">
              <template #default="{ row }">
                <span class="old-value">{{ row.oldValue }}</span>
              </template>
            </el-table-column>
            <el-table-column label="New Value">
              <template #default="{ row }">
                <span class="new-value">{{ row.newValue }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div v-if="selectedEntry.metadata" class="metadata">
          <h4>Metadata</h4>
          <pre>{{ JSON.stringify(selectedEntry.metadata, null, 2) }}</pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuditStore } from '~/stores/audit';
import { usePermissions } from '~/composables/usePermissions';
import { useNotificationStore } from '~/stores/notification';
import { useFormat } from '~/composables/useFormat';
import type { AuditAction, AuditEntry } from '~/stores/audit';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
  roles: ['AUDITOR', 'COMPLIANCE', 'ADMIN', 'SUPER_ADMIN'],
});

const auditStore = useAuditStore();
const notificationStore = useNotificationStore();
const { canExportAudit } = usePermissions();
const { formatDateTime, formatRelative, getInitials } = useFormat();

const dateRange = ref();
const detailOpen = ref(false);
const selectedEntry = ref<AuditEntry | null>(null);

function getActionType(action: AuditAction): '' | 'success' | 'warning' | 'danger' | 'info' {
  const types: Partial<Record<AuditAction, '' | 'success' | 'warning' | 'danger' | 'info'>> = {
    CUSTOMER_CREATE: 'success',
    CUSTOMER_UPDATE: 'info',
    CUSTOMER_DELETE: 'danger',
    KYC_APPROVE: 'success',
    KYC_REJECT: 'danger',
    MATCH_AUTO: 'info',
    MATCH_MERGE: 'warning',
    BLACKLIST_ADD: 'danger',
    CONFIG_CHANGE: 'warning',
    LOGIN: 'info',
    LOGIN_FAILED: 'danger',
  };
  return types[action] || '';
}

function handleDateChange(range: [Date, Date] | null) {
  if (range) {
    auditStore.filters.fromDate = range[0].toISOString();
    auditStore.filters.toDate = range[1].toISOString();
  } else {
    auditStore.filters.fromDate = undefined;
    auditStore.filters.toDate = undefined;
  }
}

function viewDetail(entry: AuditEntry) {
  selectedEntry.value = entry;
  detailOpen.value = true;
}

function viewChanges(entry: AuditEntry) {
  selectedEntry.value = entry;
  detailOpen.value = true;
}

function exportCsv() {
  notificationStore.showInfo('Mengekspor CSV...');
  auditStore.exportEntries('CSV').then(() => {
    notificationStore.showSuccess('Berhasil mengekspor CSV');
  });
}

function exportPdf() {
  notificationStore.showInfo('Mengekspor PDF...');
  auditStore.exportEntries('PDF').then(() => {
    notificationStore.showSuccess('Berhasil mengekspor PDF');
  });
}

onMounted(() => {
  // Mock data
  auditStore.entries = [
    {
      id: 'AUD-2026-0001',
      timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
      userId: 'U-001',
      username: 'budi.santoso',
      userFullName: 'Budi Santoso',
      userRole: 'STEWARD_CIF',
      action: 'CUSTOMER_CREATE',
      entity: 'Customer',
      entityId: 'CIF-20260126-00045',
      ipAddress: '10.20.30.40',
      userAgent: 'Mozilla/5.0...',
      result: 'SUCCESS',
      sessionId: 'sess-abc-123',
      changes: [
        { field: 'fullName', oldValue: null, newValue: 'Andi Pratama' },
        { field: 'kycStatus', oldValue: 'PENDING', newValue: 'PENDING' },
      ],
    },
    {
      id: 'AUD-2026-0002',
      timestamp: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
      userId: 'U-002',
      username: 'siti.aminah',
      userFullName: 'Siti Aminah',
      userRole: 'COMPLIANCE',
      action: 'KYC_APPROVE',
      entity: 'Customer',
      entityId: 'CIF-20260126-00044',
      ipAddress: '10.20.30.41',
      userAgent: 'Mozilla/5.0...',
      result: 'SUCCESS',
      changes: [
        { field: 'kycStatus', oldValue: 'IN_REVIEW', newValue: 'APPROVED' },
        { field: 'kycExpiryDate', oldValue: null, newValue: '2027-01-26' },
      ],
    },
    {
      id: 'AUD-2026-0003',
      timestamp: new Date(Date.now() - 1000 * 60 * 23).toISOString(),
      userId: 'system',
      username: 'system',
      userFullName: 'System',
      userRole: 'SYSTEM',
      action: 'MATCH_AUTO',
      entity: 'MatchGroup',
      entityId: 'MATCH-20260126-00012',
      ipAddress: '127.0.0.1',
      userAgent: 'mdm-batch/1.0',
      result: 'SUCCESS',
    },
    {
      id: 'AUD-2026-0004',
      timestamp: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
      userId: 'U-003',
      username: 'andi.wijaya',
      userFullName: 'Andi Wijaya',
      userRole: 'STEWARD_CIF',
      action: 'CUSTOMER_UPDATE',
      entity: 'Customer',
      entityId: 'CIF-20260125-00198',
      ipAddress: '10.20.30.42',
      userAgent: 'Mozilla/5.0...',
      result: 'SUCCESS',
      changes: [
        { field: 'mobilePhone', oldValue: '081234567890', newValue: '081234567891' },
      ],
    },
    {
      id: 'AUD-2026-0005',
      timestamp: new Date(Date.now() - 1000 * 60 * 47).toISOString(),
      userId: 'U-004',
      username: 'dewi.lestari',
      userFullName: 'Dewi Lestari',
      userRole: 'STEWARD_CIF',
      action: 'MATCH_MERGE',
      entity: 'MatchGroup',
      entityId: 'MATCH-20260126-00011',
      ipAddress: '10.20.30.43',
      userAgent: 'Mozilla/5.0...',
      result: 'SUCCESS',
      changes: [
        { field: 'status', oldValue: 'PENDING', newValue: 'MANUALLY_MERGED' },
        { field: 'primaryRecord', oldValue: 'CIF-20260125-00150', newValue: 'CIF-20260125-00150' },
      ],
    },
    {
      id: 'AUD-2026-0006',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 1).toISOString(),
      userId: 'U-005',
      username: 'admin',
      userFullName: 'Admin',
      userRole: 'ADMIN',
      action: 'CONFIG_CHANGE',
      entity: 'Config',
      entityId: 'config.matching.algorithm',
      ipAddress: '10.20.30.1',
      userAgent: 'Mozilla/5.0...',
      result: 'SUCCESS',
      changes: [
        { field: 'algorithm', oldValue: 'JAROWINKLER', newValue: 'JAROWINKLER+LEVENSHTEIN' },
      ],
    },
  ];
  auditStore.totalElements = 6;
});
</script>

<style scoped>
.audit-page {
  min-height: 100vh;
}

.page-content {
  padding: 24px 32px;
}

.filter-bar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar-sm {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #1e40af;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
}

.user-role-sm {
  font-size: 11px;
  color: #6b7280;
}

.mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
}

.mono-sm {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #6b7280;
}

.meta-time {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 2px;
}

.audit-detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.detail-header h3 {
  margin: 0 0 4px;
  font-size: 18px;
  font-weight: 600;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.detail-item label {
  font-size: 11px;
  text-transform: uppercase;
  color: #6b7280;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.detail-item span {
  font-size: 13px;
  color: #111827;
}

.changes-section h4, .metadata h4 {
  margin: 0 0 8px;
  font-size: 14px;
  font-weight: 600;
}

.old-value {
  text-decoration: line-through;
  color: #dc2626;
  background: rgba(220, 38, 38, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
}

.new-value {
  color: #16a34a;
  background: rgba(22, 163, 74, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
}

.metadata pre {
  background: #1f2937;
  color: #f9fafb;
  padding: 12px;
  border-radius: 8px;
  font-size: 12px;
  overflow-x: auto;
  margin: 0;
}
</style>
