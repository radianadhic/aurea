/**
 * Vitest test setup for Vue 3 + Pinia + Element Plus.
 * Copy to your tests/setup.ts and import in vitest.config.ts.
 */
import { beforeEach, vi } from 'vitest';
import { createPinia, setActivePinia } from 'pinia';
import { config } from '@vue/test-utils';

// Element Plus mock (use the actual components, just reduce surface for tests)
vi.mock('element-plus', async () => {
  const actual = await vi.importActual('element-plus');
  return {
    ...actual,
    ElMessage: {
      success: vi.fn(),
      error: vi.fn(),
      warning: vi.fn(),
      info: vi.fn(),
    },
    ElMessageBox: {
      confirm: vi.fn().mockResolvedValue('confirm'),
      prompt: vi.fn().mockResolvedValue({ value: 'test' }),
    },
    ElNotification: vi.fn(),
  };
});

// Reset Pinia and mocks between tests
beforeEach(() => {
  setActivePinia(createPinia());
  vi.clearAllMocks();
  localStorage.clear();
});

// Global Vue Test Utils config
config.global.stubs = {
  // Stub heavy components if needed
  'el-icon': true,
  'el-button': true,
  'el-input': true,
};
