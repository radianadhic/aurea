import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '~/stores/auth';

// Mock useApi
vi.mock('~/composables/useApi', () => ({
  useApi: () => ({
    getAccessToken: vi.fn().mockReturnValue(null),
    setTokens: vi.fn(),
    clearTokens: vi.fn(),
    get: vi.fn(),
    post: vi.fn(),
    delete: vi.fn(),
    logout: vi.fn(),
  }),
}));

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('initializes with empty state', () => {
    const store = useAuthStore();
    expect(store.user).toBeNull();
    expect(store.isAuthenticated).toBe(false);
    expect(store.loading).toBe(false);
    expect(store.initialized).toBe(false);
  });

  it('hasRole returns false when no user', () => {
    const store = useAuthStore();
    expect(store.hasRole('ADMIN')).toBe(false);
  });

  it('hasRole returns true for matching role', () => {
    const store = useAuthStore();
    store.user = {
      id: '1',
      username: 'test',
      email: 'test@example.com',
      fullName: 'Test User',
      roles: ['STEWARD_CIF', 'ADMIN'],
      permissions: [],
    };
    expect(store.hasRole('ADMIN')).toBe(true);
    expect(store.hasRole('SUPER_ADMIN')).toBe(false);
  });

  it('hasAnyRole works for multiple roles', () => {
    const store = useAuthStore();
    store.user = {
      id: '1',
      username: 'test',
      email: 'test@example.com',
      fullName: 'Test User',
      roles: ['STEWARD_CIF'],
      permissions: [],
    };
    expect(store.hasAnyRole('ADMIN', 'STEWARD_CIF')).toBe(true);
    expect(store.hasAnyRole('SUPER_ADMIN', 'ANALYST')).toBe(false);
  });

  it('hasAllRoles works for required roles', () => {
    const store = useAuthStore();
    store.user = {
      id: '1',
      username: 'test',
      email: 'test@example.com',
      fullName: 'Test User',
      roles: ['STEWARD_CIF', 'ANALYST'],
      permissions: [],
    };
    expect(store.hasAllRoles('STEWARD_CIF', 'ANALYST')).toBe(true);
    expect(store.hasAllRoles('STEWARD_CIF', 'ADMIN')).toBe(false);
  });

  it('hasPermission checks permissions list', () => {
    const store = useAuthStore();
    store.user = {
      id: '1',
      username: 'test',
      email: 'test@example.com',
      fullName: 'Test User',
      roles: ['STEWARD_CIF'],
      permissions: ['customer:read', 'customer:write'],
    };
    expect(store.hasPermission('customer:read')).toBe(true);
    expect(store.hasPermission('admin:user:write')).toBe(false);
  });

  it('isAdmin and isSteward computed correctly', () => {
    const store = useAuthStore();
    store.user = {
      id: '1',
      username: 'test',
      email: 'test@example.com',
      fullName: 'Test User',
      roles: ['STEWARD_CIF'],
      permissions: [],
    };
    expect(store.isSteward).toBe(true);
    expect(store.isAdmin).toBe(false);

    store.user.roles = ['ADMIN'];
    expect(store.isAdmin).toBe(true);
  });

  it('initials computed correctly', () => {
    const store = useAuthStore();
    store.user = {
      id: '1',
      username: 'budi.santoso',
      email: 'budi@example.com',
      fullName: 'Budi Santoso',
      roles: ['STEWARD_CIF'],
      permissions: [],
    };
    expect(store.initials).toBe('BS');
  });

  it('clearUser clears state', () => {
    const store = useAuthStore();
    store.user = {
      id: '1',
      username: 'test',
      email: 'test@example.com',
      fullName: 'Test',
      roles: ['STEWARD_CIF'],
      permissions: [],
    };
    store.clearUser();
    expect(store.user).toBeNull();
  });
});
