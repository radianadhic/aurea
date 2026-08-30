<template>
  <div class="kyc-card" :class="[`severity-${case.kycStatus?.toLowerCase()}`]">
    <div class="kyc-header">
      <div class="kyc-customer">
        <div class="kyc-avatar" :style="{ background: avatarColor }">
          {{ initials }}
        </div>
        <div>
          <div class="kyc-name">{{ case.customerName }}</div>
          <div class="kyc-cif">{{ case.cifNumber }}</div>
        </div>
      </div>
      <div class="kyc-badges">
        <span v-if="case.pepStatus" class="badge-pep">PEP</span>
        <el-tag v-if="case.sanctionsStatus === 'MATCH'" type="danger" size="small">
          Sanctions Match
        </el-tag>
        <el-tag v-if="case.sanctionsStatus === 'POTENTIAL_MATCH'" type="warning" size="small">
          Potential Match
        </el-tag>
      </div>
    </div>

    <div class="kyc-info-grid">
      <div class="info-cell">
        <span class="cell-label">KYC Level</span>
        <span class="cell-value">{{ kycLevelLabel }}</span>
      </div>
      <div class="info-cell">
        <span class="cell-label">Risk Score</span>
        <div class="risk-bar">
          <div class="risk-fill" :style="{ width: `${case.riskScore}%`, background: riskColor }"></div>
          <span class="risk-text" :style="{ color: riskColor }">{{ case.riskScore }}</span>
        </div>
      </div>
      <div class="info-cell">
        <span class="cell-label">Documents</span>
        <div class="doc-progress">
          <el-progress
            :percentage="case.documentCompleteness"
            :color="docColor"
            :stroke-width="6"
            :show-text="false"
          />
          <span class="doc-text">{{ case.documentCompleteness }}%</span>
        </div>
      </div>
      <div class="info-cell">
        <span class="cell-label">Days Idle</span>
        <span class="cell-value" :class="idleClass">
          {{ case.daysSinceLastUpdate }} hari
        </span>
      </div>
    </div>

    <div v-if="case.flags && case.flags.length" class="kyc-flags">
      <el-tag
        v-for="flag in case.flags"
        :key="flag"
        size="small"
        type="warning"
        effect="plain"
      >
        ⚠ {{ flag }}
      </el-tag>
    </div>

    <div v-if="case.documents && case.documents.length" class="kyc-documents">
      <div class="docs-label">Dokumen ({{ case.documents.length }}):</div>
      <div class="docs-list">
        <span
          v-for="doc in case.documents.slice(0, 4)"
          :key="doc.id"
          class="doc-chip"
          :class="{ verified: doc.verified }"
          :title="doc.fileName"
        >
          {{ doc.type }} {{ doc.verified ? '✓' : '⏳' }}
        </span>
        <span v-if="case.documents.length > 4" class="doc-more">
          +{{ case.documents.length - 4 }} lagi
        </span>
      </div>
    </div>

    <div class="kyc-footer">
      <div class="footer-meta">
        <span v-if="case.assignedTo" class="assigned-to">
          Assigned: <strong>{{ case.assignedTo }}</strong>
        </span>
        <span v-else class="unassigned">Belum di-assign</span>
        <span v-if="case.reviewDeadline" class="deadline">
          Deadline: {{ formatDate(case.reviewDeadline) }}
        </span>
      </div>
      <div class="footer-actions">
        <el-button size="small" @click="$emit('view', case)">
          Detail
        </el-button>
        <el-button
          v-if="canApprove"
          size="small"
          type="success"
          @click="$emit('approve', case)"
        >
          Approve
        </el-button>
        <el-button
          v-if="canApprove"
          size="small"
          type="danger"
          @click="$emit('reject', case)"
        >
          Reject
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useFormat } from '~/composables/useFormat';
import type { KycCase } from '~/stores/kyc';

interface Props {
  case: KycCase;
  canApprove?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  canApprove: true,
});

defineEmits<{
  (e: 'view', kycCase: KycCase): void;
  (e: 'approve', kycCase: KycCase): void;
  (e: 'reject', kycCase: KycCase): void;
}>();

const { formatDate, getInitials } = useFormat();

const initials = computed(() => getInitials(props.case.customerName));

const avatarColor = computed(() => {
  const colors = ['#1e40af', '#d97706', '#16a34a', '#dc2626', '#0284c7', '#7c3aed', '#db2777'];
  let hash = 0;
  for (let i = 0; i < props.case.customerId.length; i++) {
    hash = props.case.customerId.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
});

const kycLevelLabel = computed(() => {
  const labels: Record<string, string> = {
    STANDARD: 'Standard',
    ENHANCED: 'Enhanced',
    SIMPLIFIED: 'Simplified',
  };
  return labels[props.case.kycLevel] || props.case.kycLevel;
});

const riskColor = computed(() => {
  if (props.case.riskScore >= 70) return '#dc2626';
  if (props.case.riskScore >= 40) return '#ea580c';
  return '#16a34a';
});

const docColor = computed(() => {
  if (props.case.documentCompleteness >= 80) return '#16a34a';
  if (props.case.documentCompleteness >= 50) return '#ea580c';
  return '#dc2626';
});

const idleClass = computed(() => {
  if (props.case.daysSinceLastUpdate > 14) return 'text-error';
  if (props.case.daysSinceLastUpdate > 7) return 'text-warning';
  return 'text-muted';
});
</script>

<style scoped>
.kyc-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  transition: all 0.2s;
}

.kyc-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.kyc-card.severity-rejected {
  border-left: 4px solid #dc2626;
}

.kyc-card.severity-expired {
  border-left: 4px solid #ea580c;
}

.kyc-card.severity-approved {
  border-left: 4px solid #16a34a;
}

.kyc-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.kyc-customer {
  display: flex;
  align-items: center;
  gap: 12px;
}

.kyc-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.kyc-name {
  font-weight: 600;
  font-size: 14px;
  color: #111827;
}

.kyc-cif {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #6b7280;
}

.kyc-badges {
  display: flex;
  gap: 6px;
  align-items: center;
}

.badge-pep {
  background: rgba(124, 58, 237, 0.1);
  color: #6d28d9;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.kyc-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 12px;
}

.info-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.cell-label {
  font-size: 11px;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.cell-value {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.risk-bar {
  position: relative;
  height: 18px;
  background: #f3f4f6;
  border-radius: 9px;
  overflow: hidden;
}

.risk-fill {
  height: 100%;
  border-radius: 9px;
  transition: width 0.3s;
}

.risk-text {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 11px;
  font-weight: 600;
}

.doc-progress {
  display: flex;
  align-items: center;
  gap: 8px;
}

.doc-text {
  font-size: 12px;
  color: #6b7280;
  white-space: nowrap;
}

.kyc-flags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 12px;
}

.kyc-documents {
  margin-bottom: 12px;
  padding: 8px;
  background: #f9fafb;
  border-radius: 6px;
}

.docs-label {
  font-size: 11px;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 6px;
}

.docs-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.doc-chip {
  font-size: 11px;
  padding: 2px 6px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  color: #6b7280;
}

.doc-chip.verified {
  background: rgba(22, 163, 74, 0.05);
  border-color: #16a34a;
  color: #15803d;
}

.doc-more {
  font-size: 11px;
  color: #6b7280;
  padding: 2px 6px;
}

.kyc-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.footer-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 12px;
  color: #6b7280;
}

.assigned-to strong {
  color: #1e40af;
}

.unassigned {
  color: #ea580c;
  font-style: italic;
}

.deadline {
  color: #dc2626;
}

.text-error { color: #dc2626; }
.text-warning { color: #ea580c; }
.text-muted { color: #6b7280; }

.footer-actions {
  display: flex;
  gap: 4px;
}
</style>
