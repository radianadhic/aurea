<template>
  <div class="match-candidate" :class="{ primary, selected }">
    <div class="mc-header">
      <div class="mc-rank" v-if="rank">#{{ rank }}</div>
      <div class="mc-avatar">{{ initials }}</div>
      <div class="mc-info">
        <div class="mc-name">{{ candidate.fullName }}</div>
        <div class="mc-cif">{{ candidate.cifNumber }}</div>
      </div>
      <div class="mc-score" :class="scoreClass">
        <div class="score-value">{{ candidate.matchScore }}</div>
        <div class="score-label">SCORE</div>
      </div>
    </div>

    <div class="mc-fields">
      <div
        v-for="(field, idx) in matchedFieldsList"
        :key="idx"
        class="mc-field"
        :class="{ matched: candidate.matchFields?.includes(field.key) }"
      >
        <span class="field-icon">{{ candidate.matchFields?.includes(field.key) ? '✓' : '○' }}</span>
        <span class="field-label">{{ field.label }}</span>
        <span class="field-value">{{ formatFieldValue(field.key) }}</span>
      </div>
    </div>

    <div v-if="$slots.actions" class="mc-actions">
      <slot name="actions" :candidate="candidate" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useFormat } from '~/composables/useFormat';
import type { MatchCandidate } from '~/stores/matching';

interface Props {
  candidate: MatchCandidate;
  rank?: number;
  primary?: boolean;
  selected?: boolean;
  showFields?: string[];
}

const props = withDefaults(defineProps<Props>(), {
  primary: false,
  selected: false,
  showFields: () => ['fullName', 'dateOfBirth', 'nik', 'email', 'mobilePhone', 'address'],
});

defineEmits<{
  (e: 'select', candidate: MatchCandidate): void;
}>();

const { formatDate, formatNik, getInitials } = useFormat();

const initials = computed(() => getInitials(props.candidate.fullName));

const scoreClass = computed(() => {
  if (props.candidate.matchScore >= 90) return 'score-high';
  if (props.candidate.matchScore >= 70) return 'score-medium';
  return 'score-low';
});

const fieldLabels: Record<string, string> = {
  fullName: 'Nama',
  dateOfBirth: 'Tgl Lahir',
  nik: 'NIK',
  email: 'Email',
  mobilePhone: 'No. HP',
  address: 'Alamat',
};

const matchedFieldsList = computed(() =>
  props.showFields.map((key) => ({ key, label: fieldLabels[key] || key }))
);

function formatFieldValue(key: string): string {
  const value = (props.candidate as any)[key];
  if (!value) return '-';
  switch (key) {
    case 'dateOfBirth':
      return formatDate(value);
    case 'nik':
      return formatNik(value);
    default:
      return String(value);
  }
}
</script>

<style scoped>
.match-candidate {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 12px;
  transition: all 0.2s;
}

.match-candidate.primary {
  border-color: #1e40af;
  background: rgba(30, 64, 175, 0.02);
}

.match-candidate.selected {
  border-color: #16a34a;
  background: rgba(22, 163, 74, 0.02);
}

.mc-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.mc-rank {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
}

.mc-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #1e40af;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 13px;
}

.mc-info {
  flex: 1;
  min-width: 0;
}

.mc-name {
  font-weight: 600;
  font-size: 14px;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mc-cif {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #6b7280;
}

.mc-score {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
  border: 3px solid;
}

.mc-score.score-high {
  border-color: #dc2626;
  color: #b91c1c;
  background: rgba(220, 38, 38, 0.1);
}

.mc-score.score-medium {
  border-color: #ea580c;
  color: #c2410c;
  background: rgba(234, 88, 12, 0.1);
}

.mc-score.score-low {
  border-color: #16a34a;
  color: #15803d;
  background: rgba(22, 163, 74, 0.1);
}

.score-value {
  font-size: 16px;
  line-height: 1;
}

.score-label {
  font-size: 8px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.mc-fields {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mc-field {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  padding: 4px 6px;
  border-radius: 4px;
}

.mc-field.matched {
  background: rgba(22, 163, 74, 0.05);
}

.field-icon {
  width: 14px;
  text-align: center;
  font-size: 11px;
}

.mc-field.matched .field-icon {
  color: #16a34a;
  font-weight: 700;
}

.mc-field:not(.matched) .field-icon {
  color: #d1d5db;
}

.field-label {
  color: #6b7280;
  min-width: 80px;
}

.field-value {
  color: #111827;
  font-weight: 500;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
}

.mc-actions {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
  display: flex;
  gap: 6px;
  justify-content: flex-end;
}
</style>
