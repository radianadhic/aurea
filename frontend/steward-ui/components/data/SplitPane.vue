<template>
  <div class="split-pane" :class="direction">
    <div class="pane first-pane" :style="firstPaneStyle">
      <slot name="first" />
    </div>
    <div
      class="splitter"
      :class="{ dragging: isDragging }"
      @mousedown="startDrag"
    >
      <div v-if="direction === 'horizontal'" class="splitter-grip">
        <span></span><span></span><span></span>
      </div>
    </div>
    <div class="pane second-pane" :style="secondPaneStyle">
      <slot name="second" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue';

interface Props {
  modelValue?: number;
  direction?: 'horizontal' | 'vertical';
  minSize?: number;
  maxSize?: number;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 50,
  direction: 'horizontal',
  minSize: 10,
  maxSize: 90,
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void;
  (e: 'resize', value: number): void;
}>();

const size = ref<number>(props.modelValue);
const isDragging = ref(false);
const containerRef = ref<HTMLElement | null>(null);

const firstPaneStyle = computed(() => {
  if (props.direction === 'horizontal') {
    return { flexBasis: `${size.value}%`, flexGrow: 0, flexShrink: 0 };
  }
  return { height: `${size.value}%`, flexBasis: `${size.value}%` };
});

const secondPaneStyle = computed(() => {
  if (props.direction === 'horizontal') {
    return { flex: 1, minWidth: 0 };
  }
  return { flex: 1, minHeight: 0 };
});

function startDrag(e: MouseEvent) {
  isDragging.value = true;
  e.preventDefault();
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', stopDrag);
}

function onDrag(e: MouseEvent) {
  if (!isDragging.value) return;
  const container = (e.target as HTMLElement).closest('.split-pane') as HTMLElement;
  if (!container) return;
  const rect = container.getBoundingClientRect();
  let newSize: number;
  if (props.direction === 'horizontal') {
    newSize = ((e.clientX - rect.left) / rect.width) * 100;
  } else {
    newSize = ((e.clientY - rect.top) / rect.height) * 100;
  }
  newSize = Math.max(props.minSize, Math.min(props.maxSize, newSize));
  size.value = newSize;
  emit('update:modelValue', newSize);
  emit('resize', newSize);
}

function stopDrag() {
  isDragging.value = false;
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);
}

onUnmounted(() => {
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);
});
</script>

<style scoped>
.split-pane {
  display: flex;
  width: 100%;
  height: 100%;
  min-height: 200px;
}

.split-pane.vertical {
  flex-direction: column;
}

.pane {
  flex: 1;
  min-width: 0;
  min-height: 0;
  overflow: auto;
}

.splitter {
  flex-shrink: 0;
  background: #e5e7eb;
  position: relative;
  transition: background 0.2s;
}

.split-pane.horizontal .splitter {
  width: 4px;
  cursor: col-resize;
}

.split-pane.vertical .splitter {
  height: 4px;
  cursor: row-resize;
}

.splitter:hover, .splitter.dragging {
  background: #1e40af;
}

.splitter-grip {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  gap: 3px;
  pointer-events: none;
}

.splitter-grip span {
  width: 2px;
  height: 14px;
  background: rgba(255, 255, 255, 0);
  border-radius: 1px;
}

.splitter:hover .splitter-grip span,
.splitter.dragging .splitter-grip span {
  background: rgba(255, 255, 255, 0.8);
}
</style>
