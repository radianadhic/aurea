<template>
  <div class="rich-text-editor">
    <div class="rte-toolbar">
      <button
        v-for="btn in toolbarButtons"
        :key="btn.command"
        class="rte-btn"
        :class="{ active: activeStates[btn.command] }"
        :title="btn.tooltip"
        @click.prevent="exec(btn.command, btn.value)"
      >
        <span v-html="btn.icon"></span>
      </button>
      <span class="rte-divider"></span>
      <button class="rte-btn" title="Bold" @click.prevent="exec('bold')"><strong>B</strong></button>
      <button class="rte-btn" title="Italic" @click.prevent="exec('italic')"><em>I</em></button>
      <button class="rte-btn" title="Underline" @click.prevent="exec('underline')"><u>U</u></button>
      <button class="rte-btn" title="Strike" @click.prevent="exec('strikeThrough')"><s>S</s></button>
      <span class="rte-divider"></span>
      <button class="rte-btn" title="Bulleted list" @click.prevent="exec('insertUnorderedList')">•</button>
      <button class="rte-btn" title="Numbered list" @click.prevent="exec('insertOrderedList')">1.</button>
      <span class="rte-divider"></span>
      <select class="rte-select" @change="onFontSize($event)">
        <option value="">Ukuran</option>
        <option value="1">Sangat kecil</option>
        <option value="2">Kecil</option>
        <option value="3">Normal</option>
        <option value="4">Besar</option>
        <option value="5">Sangat besar</option>
        <option value="6">Heading</option>
        <option value="7">Heading utama</option>
      </select>
      <button class="rte-btn" title="Link" @click.prevent="addLink">🔗</button>
      <button class="rte-btn" title="Image" @click.prevent="addImage">🖼️</button>
      <span class="rte-divider"></span>
      <button class="rte-btn" title="Undo" @click.prevent="exec('undo')">↶</button>
      <button class="rte-btn" title="Redo" @click.prevent="exec('redo')">↷</button>
      <span class="rte-divider"></span>
      <button class="rte-btn" title="Source" @click.prevent="toggleSource">
        {{ sourceMode ? 'Preview' : 'HTML' }}
      </button>
    </div>
    <div v-if="!sourceMode" ref="editorRef" class="rte-content" contenteditable @input="onInput" v-html="modelValue" />
    <textarea
      v-else
      :value="modelValue"
      class="rte-source"
      @input="onSourceInput($event)"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';

interface Props {
  modelValue?: string;
  placeholder?: string;
  minHeight?: string;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: 'Tulis sesuatu...',
  minHeight: '200px',
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
  (e: 'change', value: string): void;
}>();

const editorRef = ref<HTMLElement>();
const sourceMode = ref(false);

const activeStates = reactive<Record<string, boolean>>({});

const toolbarButtons = [
  { command: 'justifyLeft', value: '', tooltip: 'Rata kiri', icon: '⬅' },
  { command: 'justifyCenter', value: '', tooltip: 'Rata tengah', icon: '↔' },
  { command: 'justifyRight', value: '', tooltip: 'Rata kanan', icon: '➡' },
  { command: 'justifyFull', value: '', tooltip: 'Rata penuh', icon: '⬌' },
];

function exec(command: string, value: string = '') {
  document.execCommand(command, false, value);
  updateActiveStates();
  onInput();
}

function updateActiveStates() {
  toolbarButtons.forEach((btn) => {
    activeStates[btn.command] = document.queryCommandState(btn.command);
  });
}

function onInput() {
  if (editorRef.value) {
    const html = editorRef.value.innerHTML;
    emit('update:modelValue', html);
    emit('change', html);
  }
}

function onSourceInput(event: Event) {
  const value = (event.target as HTMLTextAreaElement).value;
  emit('update:modelValue', value);
  emit('change', value);
}

function onFontSize(event: Event) {
  const size = (event.target as HTMLSelectElement).value;
  if (size) {
    exec('fontSize', size);
    (event.target as HTMLSelectElement).value = '';
  }
}

function addLink() {
  const url = prompt('Masukkan URL:');
  if (url) {
    exec('createLink', url);
  }
}

function addImage() {
  const url = prompt('Masukkan URL gambar:');
  if (url) {
    exec('insertImage', url);
  }
}

function toggleSource() {
  sourceMode.value = !sourceMode.value;
}

onMounted(() => {
  if (editorRef.value && !props.modelValue) {
    editorRef.value.innerHTML = `<p><span style="color: #9ca3af;">${props.placeholder}</span></p>`;
  }
  document.addEventListener('selectionchange', updateActiveStates);
});
</script>

<style scoped>
.rich-text-editor {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.rte-toolbar {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 6px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
}

.rte-btn {
  background: transparent;
  border: 0;
  padding: 6px 10px;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.15s;
  min-width: 28px;
}

.rte-btn:hover {
  background: #e5e7eb;
}

.rte-btn.active {
  background: #dbeafe;
  color: #1e40af;
}

.rte-divider {
  width: 1px;
  height: 20px;
  background: #e5e7eb;
  margin: 0 4px;
}

.rte-select {
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 13px;
  background: white;
  cursor: pointer;
}

.rte-content {
  padding: 12px 16px;
  min-height: 200px;
  outline: none;
  font-size: 14px;
  line-height: 1.6;
  color: #111827;
}

.rte-content:focus {
  outline: none;
}

.rte-source {
  width: 100%;
  min-height: 200px;
  border: 0;
  padding: 12px 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  outline: none;
  resize: vertical;
}
</style>
