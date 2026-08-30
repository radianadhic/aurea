<template>
  <div class="exception-card" :class="[`severity-${exception.severity?.toLowerCase()}`]">
    <div class="ex-header">
      <div class="ex-icon">{{ exceptionIcon }}</div>
      <div class="ex-info">
        <div class="ex-title">{{ exception.title }}</div>
        <div class="ex-id">{{ exception.id }}</div>
      </div>
      <div class="ex-priority" :class="`priority-${exception.priority?.toLowerCase()}`">
        {{ exception.priority }}
      </div>
    </div>

    <div v-if="exception.description" class="ex-description">
      {{ exception.description }}
    </div>

    <div class="ex-meta-grid">
      <div class="meta-item">
        <span class="meta-label">Type</span>
        <span class="meta-value">{{ exception.type }}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Entity</span>
        <span class="meta-value">{{ exception.entity }} · {{ exception.entityId }}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Reported</span>
        <span class="meta-value">{{ formatRelative(exception.reportedAt) }}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">SLA</span>
        <span class="meta-value" :class="slaClass">
          {{ slaText }}
        </span>
      </div>
    </div>

    <div v-if="exception.tags && exception.tags.length" class="ex-tags">
      <el-tag v-for="tag in exception.tags" :key="tag" size="small" effect="plain">
        {{ tag }}
      </el-tag>
    </div>

    <div class="ex-footer">
      <div class="ex-assignment">
        <div v-if="exception.assignedTo" class="assigned">
          <el-icon><User /></el-icon>
          <span>{{ exception.assignedTo }}</span>
        </div>
        <div v-else class="unassigned">
          <el-icon><Warning /></el-icon>
          <span>Belum di-assign</span>
        </div>
      </div>
      <div class="ex-actions">
        <el-button size="small" @click="$emit('view', exception)">
          Detail
        </el-button>
        <el-button
          v-if="!exception.assignedTo && canAssign"
          size="small"
          type="primary"
          @click="$emit('assign', exception)"
        >
          Assign ke Saya
        </el-button>
        <el-button
          v-if="exception.assignedTo"
          size="small"
          type="success"
          @click="$emit('resolve', exception)"
        >
          Resolve
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { User, Warning } from '@element-plus/icons-vue';
import { useFormat } from '~/composables/useFormat';

export type ExceptionSeverity = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
export type ExceptionPriority = 'URGENT' | 'HIGH' | 'NORMAL' | 'LOW';

export interface Exception {
  id: string;
  title: string;
  description?: string;
  type: string;
  severity: ExceptionSeverity;
  priority: ExceptionPriority;
  status: 'OPEN' | 'ASSIGNED' | 'IN_PROGRESS' | 'RESOLVED' | 'CLOSED';
  entity: string;
  entityId: string;
  reportedAt: string;
  reportedBy?: string;
  assignedTo?: string;
  assignedAt?: string;
  resolvedAt?: string;
  resolution?: string;
  tags?: string[];
  slaDeadline?: string;
  notes?: string;
}

interface Props {
  exception: Exception;
  canAssign?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  canAssign: true,
});

defineEmits<{
  (e: 'view', exception: Exception): void;
  (e: 'assign', exception: Exception): void;
  (e: 'resolve', exception: Exception): void;
}>();

const { formatRelative } = useFormat();

const exceptionIcon = computed(() => {
  const icons: Record<ExceptionSeverity, string> = {
    CRITICAL: '🚨',
    HIGH: '⚠️',
    MEDIUM: '⚡',
    LOW: 'ℹ️',
  };
  return icons[props.exception.severity] || '⚠️';
});

const slaText = computed(() => {
  if (!props.exception.slaDeadline) return 'No SLA';
  return new Date(props.exception.slaDeadline).toLocaleString('id-ID');
});

const slaClass = computed(() => {
  if (!props.exception.slaDeadline) return 'text-muted';
  const now = new Date();
  const deadline = new Date(props.exception.slaDeadline);
  if (deadline < now) return 'text-error';
  if (deadline.getTime() - now.getTime() < 60 * 60 * 1000) return 'text-warning';
  return 'text-muted';
});
</script>

<style scoped>
.exception-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 16px;
  transition: all 0.2s;
}

.exception-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.exception-card.severity-critical {
  border-left: 4px solid #dc2626;
  background: linear-gradient(to right, rgba(220, 38, 38, 0.02), transparent 30%);
}

.exception-card.severity-high {
  border-left: 4px solid #ea580c;
}

.exception-card.severity-medium {
  border-left: 4px solid #d97706;
}

.exception-card.severity-low {
  border-left: 4px solid #6b7280;
}

.ex-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.ex-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ex-info {
  flex: 1;
  min-width: 0;
}

.ex-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  line-height: 1.3;
}

.ex-id {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #6b7280;
  margin-top: 2px;
}

.ex-priority {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.priority-urgent {
  background: rgba(220, 38, 38, 0.1);
  color: #b91c1c;
}

.priority-high {
  background: rgba(234, 88, 12, 0.1);
  color: #c2410c;
}

.priority-normal {
  background: rgba(217, 119, 6, 0.1);
  color: #b45309;
}

.priority-low {
  background: rgba(107, 114, 128, 0.1);
  color: #4b5563;
}

.ex-description {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.5;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: #f9fafb;
  border-radius: 6px;
}

.ex-meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 16px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-label {
  font-size: 10px;
  text-transform: uppercase;
  color: #6b7280;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.meta-value {
  font-size: 12px;
  color: #111827;
  font-weight: 500;
}

.text-error { color: #dc2626; }
.text-warning { color: #ea580c; }
.text-muted { color: #6b7280; }

.ex-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 12px;
}

.ex-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.ex-assignment {
  font-size: 12px;
}

.assigned {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #1e40af;
}

.unassigned {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #ea580c;
  font-style: italic;
}

.ex-actions {
  display: flex;
  gap: 4px;
}
</style>
