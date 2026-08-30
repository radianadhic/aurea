<template>
  <div class="profile-page">
    <PageHeader
      title="Profil Saya"
      subtitle="Kelola informasi akun Anda"
    />

    <div class="page-content">
      <div class="profile-grid">
        <!-- Avatar Card -->
        <div class="profile-card avatar-card">
          <div class="avatar">{{ authStore.initials }}</div>
          <h2 class="profile-name">{{ authStore.fullName }}</h2>
          <p class="profile-role">{{ userRole }}</p>
          <p class="profile-email">{{ authStore.user?.email }}</p>

          <div class="profile-stats">
            <div class="stat">
              <span class="stat-num">{{ stats.loginsToday }}</span>
              <span class="stat-label">Login hari ini</span>
            </div>
            <div class="stat">
              <span class="stat-num">{{ stats.tasksCompleted }}</span>
              <span class="stat-label">Tasks selesai</span>
            </div>
            <div class="stat">
              <span class="stat-num">{{ stats.daysActive }}</span>
              <span class="stat-label">Hari aktif</span>
            </div>
          </div>

          <el-button @click="changePassword" style="width: 100%; margin-top: 16px;">
            🔑 Ganti Password
          </el-button>
        </div>

        <!-- Profile Form -->
        <div class="profile-card">
          <h3 class="card-title">Informasi Pribadi</h3>
          <el-form :model="profile" label-position="top">
            <div class="form-grid">
              <FormField label="Nama Lengkap">
                <el-input v-model="profile.fullName" />
              </FormField>
              <FormField label="Email">
                <el-input v-model="profile.email" type="email" />
              </FormField>
              <FormField label="No. Telepon">
                <el-input v-model="profile.mobilePhone" />
              </FormField>
              <FormField label="Employee ID">
                <el-input v-model="profile.employeeId" disabled />
              </FormField>
              <FormField label="Branch">
                <el-input v-model="profile.branchName" disabled />
              </FormField>
              <FormField label="Bahasa">
                <el-select v-model="profile.language">
                  <el-option label="🇮🇩 Bahasa Indonesia" value="id" />
                  <el-option label="🇬🇧 English" value="en" />
                </el-select>
              </FormField>
            </div>
            <div class="form-actions">
              <el-button type="primary" @click="saveProfile" :loading="saving">
                💾 Simpan
              </el-button>
            </div>
          </el-form>
        </div>

        <!-- Roles & Permissions -->
        <div class="profile-card">
          <h3 class="card-title">Roles & Permissions</h3>
          <div class="roles-list">
            <el-tag
              v-for="role in authStore.user?.roles"
              :key="role"
              size="large"
              type="primary"
              effect="plain"
            >
              {{ roleLabel(role) }}
            </el-tag>
          </div>
          <h4 class="subtitle" style="margin-top: 24px;">Permissions ({{ (authStore.user?.permissions || []).length }})</h4>
          <div class="permissions-list">
            <code
              v-for="perm in authStore.user?.permissions?.slice(0, 20)"
              :key="perm"
              class="perm-chip"
            >
              {{ perm }}
            </code>
            <span v-if="(authStore.user?.permissions || []).length > 20" class="more-perms">
              +{{ (authStore.user?.permissions || []).length - 20 }} lainnya
            </span>
          </div>
        </div>

        <!-- Activity Log -->
        <div class="profile-card">
          <h3 class="card-title">Aktivitas Terakhir</h3>
          <Timeline :events="recentActivity" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useNotificationStore } from '~/stores/notification';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
});

const authStore = useAuthStore();
const notificationStore = useNotificationStore();

const saving = ref(false);

const profile = reactive({
  fullName: authStore.user?.fullName || '',
  email: authStore.user?.email || '',
  mobilePhone: '',
  employeeId: authStore.user?.employeeId || 'EMP-001',
  branchName: authStore.user?.branchName || 'KCP Jakarta Pusat',
  language: 'id',
});

const stats = reactive({
  loginsToday: 2,
  tasksCompleted: 156,
  daysActive: 287,
});

const recentActivity = ref([
  {
    id: '1',
    title: 'Login',
    description: 'Login dari 10.20.30.40',
    time: '5 menit lalu',
    status: 'success' as const,
  },
  {
    id: '2',
    title: 'KYC Approved',
    description: 'KYC untuk CIF-20260125-00198 disetujui',
    time: '2 jam lalu',
    user: 'Siti Aminah',
    status: 'success' as const,
  },
  {
    id: '3',
    title: 'Customer Updated',
    description: 'Mengubah data CIF-20260125-00198',
    time: '5 jam lalu',
    user: 'Budi Santoso',
    status: 'info' as const,
  },
  {
    id: '4',
    title: 'Password Changed',
    description: 'Password berhasil diubah',
    time: '30 hari lalu',
    status: 'info' as const,
  },
]);

const userRole = computed(() => {
  const roles = authStore.user?.roles || [];
  if (roles.includes('SUPER_ADMIN')) return 'Super Administrator';
  if (roles.includes('ADMIN')) return 'Administrator';
  if (roles.includes('STEWARD_CIF')) return 'Steward CIF';
  if (roles.includes('COMPLIANCE')) return 'Compliance Officer';
  return roles[0] || 'User';
});

function roleLabel(role: string): string {
  const labels: Record<string, string> = {
    SUPER_ADMIN: 'Super Admin',
    ADMIN: 'Administrator',
    STEWARD_CIF: 'Steward CIF',
    COMPLIANCE: 'Compliance',
    ANALYST: 'Analyst',
    AUDITOR: 'Auditor',
    EXECUTIVE: 'Executive',
    BRANCH_MANAGER: 'Branch Manager',
  };
  return labels[role] || role;
}

function changePassword() {
  notificationStore.showInfo('Fitur ganti password akan segera hadir');
}

async function saveProfile() {
  saving.value = true;
  try {
    await new Promise((r) => setTimeout(r, 800));
    authStore.updateUser({
      fullName: profile.fullName,
      email: profile.email,
    });
    notificationStore.showSuccess('Profil berhasil disimpan');
  } finally {
    saving.value = false;
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
}

.page-content {
  padding: 24px 32px;
}

.profile-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

.profile-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 24px;
}

.avatar-card {
  text-align: center;
  position: sticky;
  top: 88px;
  height: fit-content;
}

.avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 36px;
  margin: 0 auto 16px;
}

.profile-name {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 4px;
}

.profile-role {
  color: #1e40af;
  font-weight: 500;
  margin: 0 0 8px;
}

.profile-email {
  color: #6b7280;
  font-size: 13px;
  margin: 0 0 24px;
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-num {
  font-size: 18px;
  font-weight: 700;
  color: #1e40af;
}

.stat-label {
  font-size: 11px;
  color: #6b7280;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px;
}

.subtitle {
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  margin: 0 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

.form-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.roles-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.perm-chip {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  padding: 2px 6px;
  background: #f3f4f6;
  border-radius: 4px;
  color: #6b7280;
}

.more-perms {
  font-size: 12px;
  color: #6b7280;
  padding: 2px 6px;
}
</style>
