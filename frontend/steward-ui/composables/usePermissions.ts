/**
 * Permission/RBAC composable.
 * Provides reactive permission checks based on user roles.
 */
import { computed } from 'vue';
import { useAuthStore } from '~/stores/auth';

export function usePermissions() {
  const authStore = useAuthStore();

  const hasRole = (role: string) => computed(() => authStore.hasRole(role));
  const hasAnyRole = (...roles: string[]) => computed(() => authStore.hasAnyRole(...roles));
  const hasAllRoles = (...roles: string[]) => computed(() => authStore.hasAllRoles(...roles));
  const hasPermission = (permission: string) => computed(() => authStore.hasPermission(permission));

  // Common role checks
  const isSuperAdmin = computed(() => authStore.hasRole('SUPER_ADMIN'));
  const isAdmin = computed(() => authStore.hasRole('ADMIN') || authStore.hasRole('SUPER_ADMIN'));
  const isSteward = computed(() => authStore.hasRole('STEWARD_CIF') || authStore.hasRole('ADMIN'));
  const isAnalyst = computed(() => authStore.hasRole('ANALYST') || authStore.hasRole('ADMIN'));
  const isAuditor = computed(() => authStore.hasRole('AUDITOR') || authStore.hasRole('ADMIN'));
  const isCompliance = computed(() => authStore.hasRole('COMPLIANCE') || authStore.hasRole('ADMIN'));
  const isExecutive = computed(() => authStore.hasRole('EXECUTIVE') || authStore.hasRole('ADMIN'));
  const isBranchManager = computed(() => authStore.hasRole('BRANCH_MANAGER') || authStore.hasRole('ADMIN'));

  // Permission-based checks (granular)
  const canReadCustomer = computed(() => hasPermission('customer:read').value);
  const canWriteCustomer = computed(() => hasPermission('customer:write').value);
  const canDeleteCustomer = computed(() => hasPermission('customer:delete').value);
  const canMergeCustomer = computed(() => hasPermission('customer:merge').value);
  const canBlacklistCustomer = computed(() => hasPermission('customer:blacklist').value);
  const canApproveKyc = computed(() => hasPermission('customer:kyc:approve').value);

  const canViewAudit = computed(() => hasPermission('audit:read').value);
  const canExportAudit = computed(() => hasPermission('audit:export').value);

  const canReadReport = computed(() => hasPermission('report:read').value);
  const canRunReport = computed(() => hasPermission('report:run').value);
  const canExportReport = computed(() => hasPermission('report:export').value);

  const canManageUsers = computed(() => hasPermission('admin:user:write').value);
  const canManageRoles = computed(() => hasPermission('admin:role:write').value);
  const canManageConfig = computed(() => hasPermission('admin:config:write').value);
  const canManageBusinessRules = computed(() => hasPermission('admin:br:write').value);

  /**
   * Generic check helper.
   */
  const check = (predicate: () => boolean) => computed(() => predicate());

  return {
    hasRole,
    hasAnyRole,
    hasAllRoles,
    hasPermission,
    isSuperAdmin,
    isAdmin,
    isSteward,
    isAnalyst,
    isAuditor,
    isCompliance,
    isExecutive,
    isBranchManager,
    canReadCustomer,
    canWriteCustomer,
    canDeleteCustomer,
    canMergeCustomer,
    canBlacklistCustomer,
    canApproveKyc,
    canViewAudit,
    canExportAudit,
    canReadReport,
    canRunReport,
    canExportReport,
    canManageUsers,
    canManageRoles,
    canManageConfig,
    canManageBusinessRules,
    check,
  };
}
