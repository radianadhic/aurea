<template>
  <div class="timeline" :class="`tl-${variant}`">
    <div
      v-for="(event, idx) in events"
      :key="event.id || idx"
      class="tl-item"
      :class="{
        active: event.active,
        [`tl-${event.status || 'info'}`]: true,
      }"
    >
      <div class="tl-marker">
        <div class="tl-dot">
          <span v-if="event.icon">{{ event.icon }}</span>
          <el-icon v-else-if="event.status === 'success'"><Check /></el-icon>
          <el-icon v-else-if="event.status === 'error'"><Close /></el-icon>
          <span v-else>{{ idx + 1 }}</span>
        </div>
        <div v-if="idx < events.length - 1" class="tl-line" />
      </div>
      <div class="tl-content">
        <div class="tl-header">
          <h4 class="tl-title">{{ event.title }}</h4>
          <time class="tl-time">{{ event.time }}</time>
        </div>
        <p v-if="event.description" class="tl-description">{{ event.description }}</p>
        <div v-if="event.user || event.location" class="tl-meta">
          <span v-if="event.user" class="tl-user">
            <el-icon><User /></el-icon>
            {{ event.user }}
          </span>
          <span v-if="event.location" class="tl-location">
            <el-icon><Location /></el-icon>
            {{ event.location }}
          </span>
        </div>
        <slot :name="`event-${idx}`" :event="event" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Check, Close, User, Location } from '@element-plus/icons-vue';

export interface TimelineEvent {
  id?: string;
  title: string;
  description?: string;
  time: string;
  user?: string;
  location?: string;
  icon?: string;
  status?: 'success' | 'error' | 'warning' | 'info' | 'pending';
  active?: boolean;
}

interface Props {
  events: TimelineEvent[];
  variant?: 'default' | 'compact' | 'detailed';
}

withDefaults(defineProps<Props>(), {
  variant: 'default',
});
</script>

<style scoped>
.timeline {
  display: flex;
  flex-direction: column;
  padding: 16px 0;
}

.tl-item {
  display: flex;
  gap: 16px;
  position: relative;
}

.tl-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.tl-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: white;
  border: 2px solid #d1d5db;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  z-index: 1;
  transition: all 0.2s;
}

.tl-info .tl-dot { border-color: #1e40af; color: #1e40af; }
.tl-success .tl-dot { background: #16a34a; border-color: #16a34a; color: white; }
.tl-error .tl-dot { background: #dc2626; border-color: #dc2626; color: white; }
.tl-warning .tl-dot { background: #ea580c; border-color: #ea580c; color: white; }
.tl-pending .tl-dot { border-color: #d1d5db; color: #9ca3af; }

.tl-line {
  width: 2px;
  flex: 1;
  background: #e5e7eb;
  margin-top: 4px;
  margin-bottom: -4px;
  min-height: 24px;
}

.tl-content {
  flex: 1;
  padding-bottom: 24px;
}

.tl-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 4px;
}

.tl-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.tl-time {
  font-size: 12px;
  color: #6b7280;
  white-space: nowrap;
}

.tl-description {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.5;
  margin: 0 0 8px;
}

.tl-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #6b7280;
}

.tl-user, .tl-location {
  display: flex;
  align-items: center;
  gap: 4px;
}

.tl-compact .tl-content {
  padding-bottom: 12px;
}

.tl-compact .tl-dot {
  width: 20px;
  height: 20px;
  font-size: 10px;
}

.tl-detailed .tl-dot {
  width: 40px;
  height: 40px;
  font-size: 14px;
}
</style>
