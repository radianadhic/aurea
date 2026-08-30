<template>
  <div class="wizard" :class="{ vertical }">
    <div v-if="!hideSteps" class="wizard-steps" :class="`steps-${position}`">
      <div
        v-for="(step, idx) in computedSteps"
        :key="step.id"
        class="wizard-step"
        :class="{
          active: idx === currentIndex,
          done: idx < currentIndex,
          error: step.error,
          clickable: clickable,
        }"
        @click="onStepClick(idx)"
      >
        <div class="step-indicator">
          <div class="step-circle">
            <el-icon v-if="step.error"><WarningFilled /></el-icon>
            <el-icon v-else-if="idx < currentIndex"><Check /></el-icon>
            <span v-else>{{ idx + 1 }}</span>
          </div>
          <div v-if="idx < computedSteps.length - 1 && position === 'horizontal'" class="step-line"></div>
        </div>
        <div class="step-content">
          <div class="step-title">{{ step.title }}</div>
          <div v-if="step.description" class="step-description">{{ step.description }}</div>
        </div>
      </div>
    </div>

    <div class="wizard-body">
      <div v-if="loading" class="wizard-loading">
        <LoadingSpinner :message="loadingMessage" />
      </div>
      <slot v-else :name="`step-${currentStep.id}`" :step="currentStep" :index="currentIndex" />
    </div>

    <div v-if="!hideFooter" class="wizard-footer">
      <div class="footer-left">
        <slot name="footer-left" />
      </div>
      <div class="footer-center">
        <el-button v-if="showCancel" @click="onCancel">{{ cancelText }}</el-button>
        <el-button
          v-if="currentIndex > 0"
          :disabled="loading"
          @click="onPrev"
        >
          ← {{ prevText }}
        </el-button>
        <el-button
          v-if="currentIndex < computedSteps.length - 1"
          type="primary"
          :loading="loading"
          :disabled="disableNext"
          @click="onNext"
        >
          {{ nextText }} →
        </el-button>
        <el-button
          v-else
          type="primary"
          :loading="loading"
          :disabled="disableSubmit"
          @click="onSubmit"
        >
          {{ submitText }}
        </el-button>
      </div>
      <div class="footer-right">
        <slot name="footer-right" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { Check, WarningFilled } from '@element-plus/icons-vue';

export interface WizardStep {
  id: string;
  title: string;
  description?: string;
  error?: boolean | string;
  optional?: boolean;
  validate?: () => boolean | Promise<boolean>;
}

interface Props {
  modelValue: number;
  steps: WizardStep[];
  position?: 'horizontal' | 'vertical';
  vertical?: boolean;
  hideSteps?: boolean;
  hideFooter?: boolean;
  showCancel?: boolean;
  cancelText?: string;
  prevText?: string;
  nextText?: string;
  submitText?: string;
  loading?: boolean;
  loadingMessage?: string;
  clickable?: boolean;
  disableNext?: boolean;
  disableSubmit?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  position: 'horizontal',
  vertical: false,
  hideSteps: false,
  hideFooter: false,
  showCancel: true,
  cancelText: 'Batal',
  prevText: 'Sebelumnya',
  nextText: 'Selanjutnya',
  submitText: 'Selesai',
  loading: false,
  loadingMessage: 'Memproses...',
  clickable: true,
  disableNext: false,
  disableSubmit: false,
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void;
  (e: 'change', step: WizardStep, index: number): void;
  (e: 'next', step: WizardStep, index: number): void;
  (e: 'prev', step: WizardStep, index: number): void;
  (e: 'submit', step: WizardStep, index: number): void;
  (e: 'cancel'): void;
  (e: 'validate', step: WizardStep, index: number): Promise<boolean> | boolean;
}>();

const currentIndex = ref<number>(props.modelValue);

const computedSteps = computed(() => props.steps);
const currentStep = computed<WizardStep>(() => computedSteps.value[currentIndex.value]);

watch(() => props.modelValue, (val) => {
  if (val !== currentIndex.value) {
    currentIndex.value = val;
  }
});

async function onNext() {
  if (currentIndex.value >= computedSteps.value.length - 1) return;
  const step = computedSteps.value[currentIndex.value];
  if (step.validate) {
    const valid = await step.validate();
    if (!valid) {
      step.error = true;
      return;
    }
  }
  step.error = false;
  emit('next', step, currentIndex.value);
  if (currentIndex.value < computedSteps.value.length - 1) {
    currentIndex.value++;
    emit('update:modelValue', currentIndex.value);
    emit('change', computedSteps.value[currentIndex.value], currentIndex.value);
  }
}

function onPrev() {
  if (currentIndex.value <= 0) return;
  const step = computedSteps.value[currentIndex.value];
  emit('prev', step, currentIndex.value);
  currentIndex.value--;
  emit('update:modelValue', currentIndex.value);
  emit('change', computedSteps.value[currentIndex.value], currentIndex.value);
}

async function onSubmit() {
  const step = computedSteps.value[currentIndex.value];
  if (step.validate) {
    const valid = await step.validate();
    if (!valid) {
      step.error = true;
      return;
    }
  }
  step.error = false;
  emit('submit', step, currentIndex.value);
}

function onCancel() {
  emit('cancel');
}

function onStepClick(idx: number) {
  if (!props.clickable) return;
  if (idx === currentIndex.value) return;
  // Allow backward navigation
  if (idx < currentIndex.value) {
    currentIndex.value = idx;
    emit('update:modelValue', idx);
    emit('change', computedSteps.value[idx], idx);
  }
}
</script>

<style scoped>
.wizard {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.wizard.vertical {
  flex-direction: row;
}

.wizard-steps {
  display: flex;
  padding: 24px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.wizard-steps.steps-vertical {
  flex-direction: column;
  border-right: 1px solid #e5e7eb;
  border-bottom: 0;
  min-width: 240px;
}

.wizard-step {
  display: flex;
  align-items: flex-start;
  flex: 1;
  cursor: pointer;
  position: relative;
}

.wizard-steps.steps-vertical .wizard-step {
  flex: none;
  margin-bottom: 16px;
}

.wizard-step:not(.clickable) {
  cursor: default;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.step-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: white;
  border: 2px solid #d1d5db;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  z-index: 1;
  transition: all 0.2s;
}

.wizard-step.active .step-circle {
  background: #1e40af;
  border-color: #1e40af;
  color: white;
  box-shadow: 0 0 0 4px rgba(30, 64, 175, 0.15);
}

.wizard-step.done .step-circle {
  background: #16a34a;
  border-color: #16a34a;
  color: white;
}

.wizard-step.error .step-circle {
  background: #dc2626;
  border-color: #dc2626;
  color: white;
}

.step-line {
  position: absolute;
  top: 32px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: #e5e7eb;
  z-index: 0;
}

.wizard-step.done .step-line {
  background: #16a34a;
}

.wizard-steps.steps-vertical .step-line {
  display: none;
}

.step-content {
  margin-left: 12px;
  margin-top: 4px;
  flex: 1;
}

.step-title {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.wizard-step.active .step-title {
  color: #1e40af;
  font-weight: 600;
}

.wizard-step.done .step-title {
  color: #16a34a;
}

.wizard-step.error .step-title {
  color: #dc2626;
}

.step-description {
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
  line-height: 1.4;
}

.wizard-body {
  flex: 1;
  padding: 24px;
  min-height: 240px;
  position: relative;
}

.wizard-loading {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.85);
}

.wizard-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

.footer-left, .footer-right {
  flex: 1;
}

.footer-right {
  display: flex;
  justify-content: flex-end;
}

.footer-center {
  display: flex;
  gap: 8px;
}
</style>
