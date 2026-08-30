<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" />
        <q-toolbar-title>
          <q-avatar size="32px" class="q-mr-sm">
            <img src="logo.svg" alt="Bank XYZ" />
          </q-avatar>
          Bank XYZ
        </q-toolbar-title>
        <q-btn flat dense round icon="notifications">
          <q-badge color="negative" floating>3</q-badge>
        </q-btn>
        <q-btn flat dense round @click="showUserMenu">
          <q-avatar size="32px" color="white" text-color="primary">{{ userInitials }}</q-avatar>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header>Menu Utama</q-item-label>
        <q-item clickable v-ripple :to="'/dashboard'" exact>
          <q-item-section avatar><q-icon name="dashboard" /></q-item-section>
          <q-item-section>Dashboard</q-item-section>
        </q-item>
        <q-item clickable v-ripple :to="'/onboarding'">
          <q-item-section avatar><q-icon name="person_add" /></q-item-section>
          <q-item-section>Onboarding Nasabah</q-item-section>
        </q-item>
        <q-item clickable v-ripple :to="'/e-kyc'">
          <q-item-section avatar><q-icon name="verified_user" /></q-item-section>
          <q-item-section>e-KYC</q-item-section>
        </q-item>
        <q-item clickable v-ripple :to="'/accounts'">
          <q-item-section avatar><q-icon name="account_balance" /></q-item-section>
          <q-item-section>Rekening Saya</q-item-section>
        </q-item>
        <q-item clickable v-ripple :to="'/transactions'">
          <q-item-section avatar><q-icon name="receipt_long" /></q-item-section>
          <q-item-section>Mutasi</q-item-section>
        </q-item>

        <q-separator class="q-my-md" />

        <q-item-label header>Layanan</q-item-label>
        <q-item clickable v-ripple :to="'/transfer'">
          <q-item-section avatar><q-icon name="send" /></q-item-section>
          <q-item-section>Transfer</q-item-section>
        </q-item>
        <q-item clickable v-ripple :to="'/topup'">
          <q-item-section avatar><q-icon name="phone_iphone" /></q-item-section>
          <q-item-section>Top Up</q-item-section>
        </q-item>
        <q-item clickable v-ripple :to="'/qris'">
          <q-item-section avatar><q-icon name="qr_code_scanner" /></q-item-section>
          <q-item-section>QRIS</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="bg-transparent text-center q-pa-sm" style="border-top: 1px solid #e5e7eb;">
      <div class="text-caption text-grey-7">
        v{{ appVersion }} · {{ buildDate }} · Bank XYZ Internal
      </div>
    </q-footer>
  </q-layout>
</template>

<script setup lang="import">
import { ref, computed } from 'vue';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'stores/auth';

const $q = useQuasar();
const authStore = useAuthStore();

const leftDrawerOpen = ref(false);
const appVersion = process.env.APP_VERSION || '1.0.0';
const buildDate = new Date().toISOString().slice(0, 10);

const userInitials = computed(() => {
  const name = authStore.user?.fullName || 'Guest';
  const parts = name.trim().split(/\s+/);
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
});

function showUserMenu() {
  $q.bottomSheet({
    message: authStore.user?.fullName,
    actions: [
      { label: 'Profil Saya', icon: 'person', id: 'profile' },
      { label: 'Pengaturan', icon: 'settings', id: 'settings' },
      { label: 'Logout', icon: 'logout', id: 'logout' },
    ],
  }).onOk((action) => {
    if (action.id === 'logout') authStore.logout();
  });
}
</script>
