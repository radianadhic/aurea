<template>
  <div class="calendar" :class="[`size-${size}`]">
    <div class="cal-header">
      <button class="cal-nav-btn" @click="prevMonth" aria-label="Previous month">‹</button>
      <div class="cal-title">
        <span class="cal-month">{{ monthName }} {{ year }}</span>
      </div>
      <button class="cal-nav-btn" @click="nextMonth" aria-label="Next month">›</button>
    </div>

    <div class="cal-weekdays">
      <div v-for="day in weekdays" :key="day" class="cal-weekday">{{ day }}</div>
    </div>

    <div class="cal-days">
      <div
        v-for="(day, idx) in calendarDays"
        :key="idx"
        class="cal-day"
        :class="{
          'other-month': !day.currentMonth,
          today: day.isToday,
          selected: isSelected(day.date),
          disabled: isDisabled(day.date),
          'has-events': day.events && day.events.length > 0,
        }"
        @click="selectDate(day)"
      >
        <span class="day-number">{{ day.day }}</span>
        <div v-if="day.events && day.events.length > 0" class="day-events">
          <span
            v-for="(event, i) in day.events.slice(0, 3)"
            :key="i"
            class="day-event-dot"
            :style="{ background: event.color || '#1e40af' }"
            :title="event.title"
          />
        </div>
      </div>
    </div>

    <div v-if="showTodayButton" class="cal-footer">
      <button class="cal-today-btn" @click="goToToday">Hari ini</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

export interface CalendarEvent {
  date: string | Date;
  title: string;
  color?: string;
}

interface Props {
  modelValue?: Date | string | null;
  events?: CalendarEvent[];
  minDate?: Date | string;
  maxDate?: Date | string;
  showTodayButton?: boolean;
  size?: 'sm' | 'md' | 'lg';
  locale?: string;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  events: () => [],
  showTodayButton: true,
  size: 'md',
  locale: 'id-ID',
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: Date): void;
  (e: 'change', value: Date): void;
  (e: 'monthChange', value: { year: number; month: number }): void;
}>();

const currentDate = ref(new Date());
const selectedDate = ref<Date | null>(
  props.modelValue ? new Date(props.modelValue) : null
);

const monthNames = [
  'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember',
];

const weekdays = computed(() => {
  return ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'];
});

const monthName = computed(() => monthNames[currentDate.value.getMonth()]);
const year = computed(() => currentDate.value.getFullYear());

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const startOffset = firstDay.getDay();
  const daysInMonth = lastDay.getDate();
  const days: Array<{
    day: number;
    date: Date;
    currentMonth: boolean;
    isToday: boolean;
    events?: CalendarEvent[];
  }> = [];

  // Previous month
  for (let i = startOffset - 1; i >= 0; i--) {
    const d = new Date(year, month, -i);
    days.push({
      day: d.getDate(),
      date: d,
      currentMonth: false,
      isToday: false,
      events: getEventsForDate(d),
    });
  }

  // Current month
  const today = new Date();
  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, month, d);
    days.push({
      day: d,
      date,
      currentMonth: true,
      isToday:
        date.getDate() === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear(),
      events: getEventsForDate(date),
    });
  }

  // Next month (to complete the 6 weeks)
  const remaining = 42 - days.length;
  for (let d = 1; d <= remaining; d++) {
    const date = new Date(year, month + 1, d);
    days.push({
      day: d,
      date,
      currentMonth: false,
      isToday: false,
      events: getEventsForDate(date),
    });
  }

  return days;
});

function getEventsForDate(date: Date): CalendarEvent[] {
  return props.events.filter((e) => {
    const eventDate = new Date(e.date);
    return (
      eventDate.getDate() === date.getDate() &&
      eventDate.getMonth() === date.getMonth() &&
      eventDate.getFullYear() === date.getFullYear()
    );
  });
}

function isSelected(date: Date): boolean {
  if (!selectedDate.value) return false;
  return (
    date.getDate() === selectedDate.value.getDate() &&
    date.getMonth() === selectedDate.value.getMonth() &&
    date.getFullYear() === selectedDate.value.getFullYear()
  );
}

function isDisabled(date: Date): boolean {
  if (props.minDate && date < new Date(props.minDate)) return true;
  if (props.maxDate && date > new Date(props.maxDate)) return true;
  return false;
}

function selectDate(day: { date: Date; currentMonth: boolean }) {
  if (!day.currentMonth) {
    currentDate.value = new Date(day.date);
  }
  if (isDisabled(day.date)) return;
  selectedDate.value = day.date;
  emit('update:modelValue', day.date);
  emit('change', day.date);
}

function prevMonth() {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() - 1,
    1
  );
  emit('monthChange', {
    year: currentDate.value.getFullYear(),
    month: currentDate.value.getMonth(),
  });
}

function nextMonth() {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() + 1,
    1
  );
  emit('monthChange', {
    year: currentDate.value.getFullYear(),
    month: currentDate.value.getMonth(),
  });
}

function goToToday() {
  const today = new Date();
  currentDate.value = new Date(today.getFullYear(), today.getMonth(), 1);
  selectedDate.value = today;
  emit('update:modelValue', today);
  emit('change', today);
}
</script>

<style scoped>
.calendar {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  width: 100%;
  max-width: 360px;
}

.size-sm { max-width: 280px; padding: 12px; }
.size-lg { max-width: 420px; padding: 20px; }

.cal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.cal-nav-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: transparent;
  border: 0;
  cursor: pointer;
  font-size: 18px;
  color: #6b7280;
  transition: all 0.15s;
}

.cal-nav-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.cal-title {
  flex: 1;
  text-align: center;
}

.cal-month {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  text-transform: capitalize;
}

.cal-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  margin-bottom: 4px;
}

.cal-weekday {
  text-align: center;
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  padding: 6px 0;
  text-transform: uppercase;
}

.cal-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}

.cal-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 8px;
  font-size: 13px;
  color: #374151;
  position: relative;
  transition: all 0.15s;
  padding: 4px;
}

.cal-day:hover:not(.disabled) {
  background: #f3f4f6;
}

.cal-day.other-month {
  color: #d1d5db;
}

.cal-day.today .day-number {
  font-weight: 700;
  color: #1e40af;
}

.cal-day.selected {
  background: #1e40af;
  color: white;
}

.cal-day.selected .day-number {
  color: white;
  font-weight: 600;
}

.cal-day.disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.day-number {
  font-size: 13px;
}

.day-events {
  display: flex;
  gap: 2px;
  margin-top: 2px;
  justify-content: center;
}

.day-event-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
}

.cal-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
  text-align: center;
}

.cal-today-btn {
  background: transparent;
  border: 1px solid #e5e7eb;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  color: #1e40af;
  cursor: pointer;
  transition: all 0.15s;
}

.cal-today-btn:hover {
  background: #f3f4f6;
}
</style>
