<template>
  <div class="settings-page">
    <PageHeader
      title="Pengaturan"
      subtitle="Konfigurasi tampilan, notifikasi, dan preferensi aplikasi"
    />

    <div class="page-content">
      <Tabs v-model="activeTab" :tabs="tabs">
        <template #appearance>
          <div class="settings-section">
            <h3 class="section-title">Tampilan</h3>
            <div class="settings-list">
              <div class="setting-item">
                <div>
                  <div class="setting-label">Theme</div>
                  <div class="setting-description">Pilih tema tampilan</div>
                </div>
                <el-radio-group v-model="settings.theme">
                  <el-radio-button value="light">☀️ Light</el-radio-button>
                  <el-radio-button value="dark">🌙 Dark</el-radio-button>
                  <el-radio-button value="auto">🖥️ Auto</el-radio-button>
                </el-radio-group>
              </div>

              <div class="setting-item">
                <div>
                  <div class="setting-label">Compact Mode</div>
                  <div class="setting-description">Tampilan lebih ringkas</div>
                </div>
                <el-switch v-model="settings.compactMode" />
              </div>

              <div class="setting-item">
                <div>
                  <div class="setting-label">Page Size</div>
                  <div class="setting-description">Jumlah baris per halaman</div>
                </div>
                <el-select v-model="settings.pageSize" style="width: 100px;">
                  <el-option v-for="s in [10, 20, 50, 100]" :key="s" :value="s" :label="`${s}`" />
                </el-select>
              </div>
            </div>
          </div>
        </template>

        <template #notifications>
          <div class="settings-section">
            <h3 class="section-title">Notifikasi</h3>
            <div class="settings-list">
              <div class="setting-item">
                <div>
                  <div class="setting-label">Email Notifications</div>
                  <div class="setting-description">Kirim notifikasi via email</div>
                </div>
                <el-switch v-model="settings.emailNotif" />
              </div>

              <div class="setting-item">
                <div>
                  <div class="setting-label">Push Notifications</div>
                  <div class="setting-description">Notifikasi real-time di browser</div>
                </div>
                <el-switch v-model="settings.pushNotif" />
              </div>

              <div class="setting-item">
                <div>
                  <div class="setting-label">KYC Updates</div>
                  <div class="setting-description">Notifikasi perubahan status KYC</div>
                </div>
                <el-switch v-model="settings.kycNotif" />
              </div>

              <div class="setting-item">
                <div>
                  <div class="setting-label">Match Queue</div>
                  <div class="setting-description">Notifikasi match group baru</div>
                </div>
                <el-switch v-model="settings.matchNotif" />
              </div>

              <div class="setting-item">
                <div>
                  <div class="setting-label">Daily Digest</div>
                  <div class="setting-description">Ringkasan harian via email</div>
                </div>
                <el-switch v-model="settings.dailyDigest" />
              </div>
            </div>
          </div>
        </template>

        <template #security>
          <div class="settings-section">
            <h3 class="section-title">Keamanan</h3>
            <div class="settings-list">
              <div class="setting-item">
                <div>
                  <div class="setting-label">Two-Factor Authentication</div>
                  <div class="setting-description">Login dengan MFA</div>
                </div>
                <el-switch v-model="settings.mfa" />
              </div>

              <div class="setting-item">
                <div>
                  <div class="setting-label">Session Timeout</div>
                  <div class="setting-description">Auto-logout setelah inactivity</div>
                </div>
                <el-select v-model="settings.sessionTimeout" style="width: 120px;">
                  <el-option label="15 menit" :value="15" />
                  <el-option label="30 menit" :value="30" />
                  <el-option label="1 jam" :value="60" />
                  <el-option label="4 jam" :value="240" />
                </el-select>
              </div>

              <div class="setting-item">
                <div>
                  <div class="setting-label">Login Alerts</div>
                  <div class="setting-description">Email alert untuk login baru</div>
                </div>
                <el-switch v-model="settings.loginAlerts" />
              </div>
            </div>

            <h3 class="section-title" style="margin-top: 24px;">Active Sessions</h3>
            <el-table :data="activeSessions" size="small">
              <el-table-column prop="device" label="Device" />
              <el-table-column prop="location" label="Location" />
              <el-table-column prop="ip" label="IP" />
              <el-table-column prop="lastActive" label="Last Active" />
              <el-table-column label="Action" align="right">
                <template #default>
                  <el-button text type="danger" size="small">Revoke</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </template>
      </Tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useNotificationStore } from '~/stores/notification';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
});

const notificationStore = useNotificationStore();

const activeTab = ref(0);

const tabs = [
  { name: 'appearance', label: '🎨 Tampilan' },
  { name: 'notifications', label: '🔔 Notifikasi' },
  { name: 'security', label: '🔐 Keamanan' },
];

const settings = reactive({
  theme: 'light',
  compactMode: false,
  pageSize: 20,
  emailNotif: true,
  pushNotif: true,
  kycNotif: true,
  matchNotif: true,
  dailyDigest: true,
  mfa: true,
  sessionTimeout: 30,
  loginAlerts: true,
});

const activeSessions = ref([
  { device: 'Chrome on Windows', location: 'Jakarta, ID', ip: '10.20.30.40', lastActive: 'Sekarang' },
  { device: 'Safari on iPhone', location: 'Jakarta, ID', ip: '10.20.30.41', lastActive: '2 jam lalu' },
  { device: 'Firefox on Linux', location: 'Bandung, ID', ip: '10.20.30.42', lastActive: '1 hari lalu' },
]);
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
}

.page-content {
  padding: 24px 32px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  margin: 0 32px 32px;
}

.settings-section {
  padding: 16px 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px;
}

.settings-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  gap: 16px;
}

.setting-label {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.setting-description {
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
}
</style>
