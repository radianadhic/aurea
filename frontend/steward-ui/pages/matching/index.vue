<template>
  <div class="matching-page">
    <PageHeader
      title="Antrian Matching"
      subtitle="Review dan merge duplikat nasabah"
    >
      <template #actions>
        <el-button @click="refreshData" :loading="matchingStore.loading">
          🔄 Refresh
        </el-button>
        <el-button type="primary" @click="runMatcher">
          ▶️ Jalankan Matcher
        </el-button>
      </template>
    </PageHeader>

    <div class="page-content">
      <!-- Stats -->
      <div class="stats-row">
        <StatCard
          label="Total Match Groups"
          :value="formatNumber(matchingStore.totalElements)"
          icon="🔄"
          color="#1e40af"
        />
        <StatCard
          label="Auto Merged"
          :value="formatNumber(stats.autoMerged)"
          icon="✅"
          color="#16a34a"
        />
        <StatCard
          label="Pending Review"
          :value="formatNumber(stats.pendingReview)"
          icon="⏳"
          color="#d97706"
        />
        <StatCard
          label="Avg Match Score"
          :value="`${stats.avgScore}%`"
          icon="📊"
          color="#0284c7"
        />
      </div>

      <!-- Filter -->
      <FilterPanel
        v-model="filterOpen"
        :active-count="activeFilterCount"
        @clear="handleClearFilters"
      >
        <FormField label="Status">
          <el-select v-model="matchingStore.filters.status" placeholder="Semua" clearable>
            <el-option label="Pending" value="PENDING" />
            <el-option label="In Review" value="IN_REVIEW" />
            <el-option label="Auto Merged" value="AUTO_MERGED" />
            <el-option label="Manually Merged" value="MANUALLY_MERGED" />
            <el-option label="Rejected" value="REJECTED" />
          </el-select>
        </FormField>
        <FormField label="Match Type">
          <el-select v-model="matchingStore.filters.matchType" placeholder="Semua" clearable>
            <el-option label="Exact" value="EXACT" />
            <el-option label="Fuzzy" value="FUZZY" />
            <el-option label="Phonetic" value="PHONETIC" />
          </el-select>
        </FormField>
        <FormField label="Min Score">
          <el-input-number v-model="matchingStore.filters.minScore" :min="0" :max="100" />
        </FormField>
        <FormField label="Max Score">
          <el-input-number v-model="matchingStore.filters.maxScore" :min="0" :max="100" />
        </FormField>
      </FilterPanel>

      <!-- Match Groups List -->
      <div class="match-list">
        <div
          v-for="group in matchingStore.matchGroups"
          :key="group.id"
          class="match-card"
        >
          <div class="match-card-header">
            <div>
              <div class="match-id">{{ group.id }}</div>
              <div class="match-meta">
                <el-tag size="small" :type="getMatchTypeColor(group.matchType)">
                  {{ group.matchType }}
                </el-tag>
                <span class="match-score" :class="getScoreClass(group.matchScore)">
                  Score: {{ group.matchScore }}%
                </span>
                <span class="match-time">{{ formatRelative(group.createdAt) }}</span>
              </div>
            </div>
            <div class="match-actions">
              <el-button text type="primary" @click="viewGroup(group)">
                Lihat
              </el-button>
              <el-button
                text
                type="success"
                :disabled="!canMergeCustomer"
                @click="handleMerge(group)"
              >
                Merge
              </el-button>
              <el-button
                text
                type="danger"
                :disabled="!canMergeCustomer"
                @click="handleReject(group)"
              >
                Reject
              </el-button>
            </div>
          </div>

          <div class="match-candidates">
            <div
              v-for="candidate in group.candidates.slice(0, 3)"
              :key="candidate.id"
              class="candidate"
            >
              <div class="candidate-avatar">
                {{ getInitials(candidate.fullName) }}
              </div>
              <div class="candidate-info">
                <div class="candidate-name">{{ candidate.fullName }}</div>
                <div class="candidate-cif">{{ candidate.cifNumber }}</div>
                <div class="candidate-details">
                  <span v-if="candidate.dateOfBirth">DOB: {{ formatDate(candidate.dateOfBirth) }}</span>
                  <span v-if="candidate.nik">NIK: {{ formatNik(candidate.nik) }}</span>
                </div>
              </div>
              <div class="candidate-score">
                <div class="score-circle" :class="getScoreClass(candidate.matchScore)">
                  {{ candidate.matchScore }}
                </div>
              </div>
            </div>
            <div v-if="group.candidates.length > 3" class="more-candidates">
              +{{ group.candidates.length - 3 }} lainnya
            </div>
          </div>

          <div class="match-footer">
            <div class="footer-info">
              <span class="status-pill" :class="`status-${group.status.toLowerCase()}`">
                {{ group.status }}
              </span>
              <span v-if="group.reviewer" class="reviewer">
                👤 {{ group.reviewer }}
              </span>
              <span class="algorithm">
                Algo: {{ group.algorithm }}
              </span>
            </div>
          </div>
        </div>

        <EmptyState
          v-if="!matchingStore.loading && matchingStore.matchGroups.length === 0"
          icon="🎉"
          title="Tidak ada match yang perlu di-review"
          description="Semua data nasabah sudah bersih dari duplikat."
        />
      </div>

      <!-- Pagination -->
      <PaginationBar
        :page="matchingStore.currentPage + 1"
        :page-size="matchingStore.pageSize"
        :total="matchingStore.totalElements"
        @update:page="matchingStore.setPage($event - 1)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue';
import { useMatchingStore } from '~/stores/matching';
import { usePermissions } from '~/composables/usePermissions';
import { useNotificationStore } from '~/stores/notification';
import { useFormat } from '~/composables/useFormat';
import type { MatchGroup, MatchType } from '~/stores/matching';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
});

const matchingStore = useMatchingStore();
const notificationStore = useNotificationStore();
const { canMergeCustomer } = usePermissions();
const { formatNumber, formatRelative, formatDate, formatNik, getInitials } = useFormat();

const filterOpen = ref(false);
const stats = reactive({
  autoMerged: 234,
  pendingReview: 89,
  avgScore: 87.5,
});

const activeFilterCount = computed(() => {
  return Object.values(matchingStore.filters).filter(
    (v) => v !== undefined && v !== null && v !== ''
  ).length;
});

function getMatchTypeColor(type: MatchType) {
  const colors: Record<MatchType, '' | 'success' | 'warning' | 'danger' | 'info'> = {
    EXACT: 'success',
    FUZZY: 'warning',
    PHONETIC: 'info',
    TRANSACTION: 'info',
  };
  return colors[type];
}

function getScoreClass(score: number) {
  if (score >= 90) return 'score-high';
  if (score >= 70) return 'score-medium';
  return 'score-low';
}

function viewGroup(group: MatchGroup) {
  navigateTo(`/matching/${group.id}`);
}

async function handleMerge(group: MatchGroup) {
  try {
    await ElMessageBox.confirm(
      `Yakin merge ${group.memberCount} nasabah menjadi 1 record? Tindakan ini tidak dapat dibatalkan.`,
      'Konfirmasi Merge',
      {
        confirmButtonText: 'Ya, Merge',
        cancelButtonText: 'Batal',
        type: 'warning',
      }
    );

    if (group.candidates.length === 0) {
      notificationStore.showError('Tidak ada kandidat untuk di-merge');
      return;
    }

    const primary = group.candidates[0];
    const secondaries = group.candidates.slice(1).map((c) => c.id);
    await matchingStore.merge(group.id, primary.id, secondaries);
    notificationStore.showSuccess('Berhasil merge');
  } catch (e: any) {
    if (e !== 'cancel') {
      notificationStore.showError('Gagal merge');
    }
  }
}

async function handleReject(group: MatchGroup) {
  try {
    const { value: reason } = await ElMessageBox.prompt(
      'Alasan reject match:',
      'Reject Match',
      {
        confirmButtonText: 'Reject',
        cancelButtonText: 'Batal',
        inputType: 'textarea',
        inputValidator: (val) => (val && val.length >= 5) || 'Minimal 5 karakter',
      }
    );

    await matchingStore.reject(group.id, reason);
    notificationStore.showSuccess('Match telah direject');
  } catch (e: any) {
    if (e !== 'cancel') {
      notificationStore.showError('Gagal reject');
    }
  }
}

function handleClearFilters() {
  matchingStore.filters = {
    status: undefined,
    matchType: undefined,
    minScore: undefined,
    maxScore: undefined,
    algorithm: undefined,
  };
  matchingStore.fetchGroups();
}

function refreshData() {
  matchingStore.fetchGroups();
}

function runMatcher() {
  notificationStore.showInfo('Matcher dijalankan di background. Hasil akan tersedia dalam 1-2 menit.');
}

onMounted(() => {
  // Load mock data
  matchingStore.matchGroups = [
    {
      id: 'MATCH-2026-00045',
      matchType: 'FUZZY',
      matchScore: 92,
      status: 'PENDING',
      memberCount: 2,
      totalRecords: 2,
      algorithm: 'Jaro-Winkler + Levenshtein',
      candidates: [
        {
          id: 'CUST-001',
          cifNumber: 'CIF-20260126-00045',
          fullName: 'Budi Santoso',
          dateOfBirth: '1985-04-12',
          nik: '3201234567890001',
          matchScore: 92,
          matchFields: ['fullName', 'dateOfBirth'],
          selected: false,
        },
        {
          id: 'CUST-002',
          cifNumber: 'CIF-20260126-00046',
          fullName: 'Budi Santosa',
          dateOfBirth: '1985-04-12',
          nik: '3201234567890002',
          matchScore: 90,
          matchFields: ['fullName', 'dateOfBirth'],
          selected: false,
        },
      ],
      createdAt: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
      updatedAt: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    },
    {
      id: 'MATCH-2026-00044',
      matchType: 'PHONETIC',
      matchScore: 88,
      status: 'IN_REVIEW',
      memberCount: 3,
      totalRecords: 3,
      algorithm: 'Metaphone + Soundex',
      candidates: [
        {
          id: 'CUST-003',
          cifNumber: 'CIF-20260125-00198',
          fullName: 'Siti Aminah',
          dateOfBirth: '1990-08-23',
          matchScore: 88,
          matchFields: ['fullName', 'mobilePhone'],
          selected: false,
        },
        {
          id: 'CUST-004',
          cifNumber: 'CIF-20260125-00199',
          fullName: 'Siti Aminah',
          dateOfBirth: '1990-08-23',
          matchScore: 87,
          matchFields: ['fullName', 'mobilePhone'],
          selected: false,
        },
        {
          id: 'CUST-005',
          cifNumber: 'CIF-20260125-00200',
          fullName: 'City Aminah',
          dateOfBirth: '1990-08-23',
          matchScore: 75,
          matchFields: ['fullName'],
          selected: false,
        },
      ],
      reviewer: 'Andi Wijaya',
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
      updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 1).toISOString(),
    },
  ];
  matchingStore.totalElements = 2;
});
</script>

<style scoped>
.matching-page {
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

.match-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}

.match-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 16px;
  transition: all 0.2s;
}

.match-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.match-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.match-id {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 600;
  color: #1e40af;
  margin-bottom: 4px;
}

.match-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #6b7280;
}

.match-score {
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.match-score.score-high {
  background: rgba(220, 38, 38, 0.1);
  color: #b91c1c;
}

.match-score.score-medium {
  background: rgba(234, 88, 12, 0.1);
  color: #c2410c;
}

.match-score.score-low {
  background: rgba(22, 163, 74, 0.1);
  color: #15803d;
}

.match-time {
  color: #9ca3af;
}

.match-actions {
  display: flex;
  gap: 4px;
}

.match-candidates {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.candidate {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.candidate-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #1e40af;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 12px;
  flex-shrink: 0;
}

.candidate-info {
  flex: 1;
  min-width: 0;
}

.candidate-name {
  font-weight: 600;
  font-size: 14px;
  color: #111827;
}

.candidate-cif {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #6b7280;
}

.candidate-details {
  font-size: 12px;
  color: #6b7280;
  display: flex;
  gap: 12px;
  margin-top: 2px;
}

.candidate-score {
  flex-shrink: 0;
}

.score-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  border: 3px solid;
}

.score-circle.score-high {
  border-color: #dc2626;
  color: #b91c1c;
  background: rgba(220, 38, 38, 0.1);
}

.score-circle.score-medium {
  border-color: #ea580c;
  color: #c2410c;
  background: rgba(234, 88, 12, 0.1);
}

.score-circle.score-low {
  border-color: #16a34a;
  color: #15803d;
  background: rgba(22, 163, 74, 0.1);
}

.more-candidates {
  text-align: center;
  font-size: 12px;
  color: #6b7280;
  padding: 6px;
}

.match-footer {
  padding-top: 8px;
  border-top: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #6b7280;
}

.footer-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-pill {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
  font-size: 11px;
}

.status-pill.status-pending {
  background: rgba(234, 88, 12, 0.1);
  color: #c2410c;
}

.status-pill.status-in_review {
  background: rgba(2, 132, 199, 0.1);
  color: #075985;
}

.status-pill.status-auto_merged {
  background: rgba(22, 163, 74, 0.1);
  color: #15803d;
}

.status-pill.status-manually_merged {
  background: rgba(22, 163, 74, 0.1);
  color: #15803d;
}

.status-pill.status-rejected {
  background: rgba(220, 38, 38, 0.1);
  color: #b91c1c;
}

.algorithm {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #9ca3af;
}
</style>
