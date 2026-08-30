<template>
  <nav class="breadcrumb-nav" :class="size">
    <ol>
      <li v-for="(item, idx) in items" :key="idx" class="breadcrumb-item">
        <span v-if="idx > 0" class="separator">{{ separator }}</span>
        <NuxtLink v-if="item.to && !item.active" :to="item.to" class="link">
          <span v-if="item.icon" class="icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </NuxtLink>
        <span v-else class="current">
          <span v-if="item.icon" class="icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </span>
      </li>
    </ol>
  </nav>
</template>

<script setup lang="ts">
interface BreadcrumbItem {
  label: string;
  to?: string;
  icon?: string;
  active?: boolean;
}

interface Props {
  items: BreadcrumbItem[];
  size?: 'sm' | 'md' | 'lg';
  separator?: string;
}

withDefaults(defineProps<Props>(), {
  size: 'md',
  separator: '/',
});
</script>

<style scoped>
.breadcrumb-nav ol {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  flex-wrap: wrap;
  gap: 4px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
}

.separator {
  color: #9ca3af;
  margin: 0 4px;
}

.link {
  color: #6b7280;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 6px;
  border-radius: 4px;
  transition: all 0.2s;
}

.link:hover {
  color: #1e40af;
  background: rgba(30, 64, 175, 0.05);
}

.current {
  color: #111827;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 6px;
}

.icon {
  font-size: 14px;
}

.size-sm { font-size: 12px; }
.size-lg { font-size: 14px; }
</style>
