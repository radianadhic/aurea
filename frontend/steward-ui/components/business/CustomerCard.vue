<template>
  <div class="customer-card" :class="{ selected }" @click="$emit('click', customer)">
    <div class="customer-card-header">
      <div class="avatar" :style="{ background: avatarColor }">
        {{ initials }}
      </div>
      <div class="info">
        <div class="name">{{ customer.fullName || customer.legalName }}</div>
        <div class="cif">{{ customer.cifNumber }}</div>
      </div>
      <div v-if="customer.pepStatus" class="pep-badge" title="Politically Exposed Person">
        PEP
      </div>
    </div>
    <div class="customer-card-body">
      <div class="info-row">
        <span class="info-label">Tipe</span>
        <el-tag size="small">{{ customerTypeLabel }}</el-tag>
      </div>
      <div class="info-row">
        <span class="info-label">KYC</span>
        <el-tag size="small" :type="kycType">{{ kycLabel }}</el-tag>
      </div>
      <div class="info-row">
        <span class="info-label">Risk</span>
        <span class="risk-pill" :class="`risk-${customer.riskProfile?.toLowerCase()}`">
          {{ customer.riskProfile || '-' }}
        </span>
      </div>
      <div class="info-row">
        <span class="info-label">Cabang</span>
        <span class="info-value">{{ customer.branchName || '-' }}</span>
      </div>
    </div>
    <div class="customer-card-footer">
      <span class="updated">
        Update {{ formatRelative(customer.updatedAt) }}
      </span>
      <span v-if="customer.tags && customer.tags.length" class="tags">
        <el-tag v-for="tag in customer.tags.slice(0, 2)" :key="tag" size="small" effect="plain">
          {{ tag }}
        </el-tag>
        <span v-if="customer.tags.length > 2" class="more-tags">+{{ customer.tags.length - 2 }}</span>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useFormat } from '~/composables/useFormat';
import type { Customer, CustomerType, KycStatus } from '~/types/customer';

interface Props {
  customer: Customer;
  selected?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  selected: false,
});

defineEmits<{
  (e: 'click', customer: Customer): void;
}>();

const { formatRelative, getInitials } = useFormat();

const initials = computed(() => getInitials(props.customer.fullName));
const avatarColor = computed(() => {
  const colors = ['#1e40af', '#d97706', '#16a34a', '#dc2626', '#0284c7', '#7c3aed', '#db2777'];
  let hash = 0;
  for (let i = 0; i < props.customer.id.length; i++) {
    hash = props.customer.id.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
});

const customerTypeLabel = computed(() => {
  const labels: Record<CustomerType, string> = {
    INDIVIDUAL: 'Individual',
    CORPORATE: 'Corporate',
    SYARIAH: 'Syariah',
  };
  return labels[props.customer.customerType] || props.customer.customerType;
});

const kycLabel = computed(() => {
  const labels: Record<KycStatus, string> = {
    PENDING: 'Pending',
    IN_REVIEW: 'In Review',
    APPROVED: 'Approved',
    REJECTED: 'Rejected',
    EXPIRED: 'Expired',
    FAILED: 'Failed',
  };
  return labels[props.customer.kycStatus];
});

const kycType = computed(() => {
  const types: Record<KycStatus, '' | 'success' | 'warning' | 'danger' | 'info'> = {
    PENDING: 'warning',
    IN_REVIEW: 'warning',
    APPROVED: 'success',
    REJECTED: 'danger',
    EXPIRED: 'info',
    FAILED: 'danger',
  };
  return types[props.customer.kycStatus];
});
</script>

<style scoped>
.customer-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.customer-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

.customer-card.selected {
  border-color: #1e40af;
  background: rgba(30, 64, 175, 0.02);
  box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
}

.customer-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.info {
  flex: 1;
  min-width: 0;
}

.name {
  font-weight: 600;
  color: #111827;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cif {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
}

.pep-badge {
  background: rgba(124, 58, 237, 0.1);
  color: #6d28d9;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.customer-card-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  padding: 8px 0;
  border-top: 1px solid #f3f4f6;
  border-bottom: 1px solid #f3f4f6;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
}

.info-label {
  color: #6b7280;
  min-width: 36px;
}

.info-value {
  color: #374151;
  font-weight: 500;
}

.risk-pill {
  display: inline-block;
  padding: 1px 8px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 500;
}

.risk-pill.risk-low {
  background: rgba(22, 163, 74, 0.1);
  color: #15803d;
}

.risk-pill.risk-medium {
  background: rgba(234, 88, 12, 0.1);
  color: #c2410c;
}

.risk-pill.risk-high {
  background: rgba(220, 38, 38, 0.1);
  color: #b91c1c;
}

.customer-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  color: #6b7280;
}

.tags {
  display: flex;
  gap: 4px;
  align-items: center;
}

.more-tags {
  font-size: 11px;
  color: #6b7280;
}
</style>
