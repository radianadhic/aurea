<template>
  <q-page padding>
    <!-- Greeting -->
    <q-card flat class="greeting-card q-mb-md">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <q-avatar size="56px" color="primary" text-color="white">{{ userInitials }}</q-avatar>
          <div>
            <div class="text-caption text-grey-6">Selamat datang,</div>
            <div class="text-h6">{{ userName }}</div>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Account Balance -->
    <q-card flat class="balance-card q-mb-md">
      <q-card-section>
        <div class="text-caption text-white" style="opacity: 0.8;">Saldo Total</div>
        <div class="text-h4 text-white text-weight-bold q-mt-xs">{{ formatCurrency(balance) }}</div>
        <div class="row q-gutter-sm q-mt-sm">
          <q-chip dense color="white" text-color="primary" icon="trending_up">+12.4% bulan ini</q-chip>
        </div>
      </q-card-section>
    </q-card>

    <!-- Quick Actions -->
    <q-card flat bordered class="q-mb-md">
      <q-card-section>
        <div class="text-subtitle2 q-mb-sm">Aksi Cepat</div>
        <div class="row q-gutter-md">
          <div class="col-3" v-for="action in quickActions" :key="action.label" @click="navigateTo(action.to)">
            <q-btn flat color="primary" :icon="action.icon" :label="action.label" stack size="md" class="full-width" />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Onboarding Status -->
    <q-card flat bordered class="q-mb-md" v-if="!isOnboarded">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <q-icon name="pending_actions" size="40px" color="orange" />
          <div class="col">
            <div class="text-subtitle1">Lengkapi Onboarding</div>
            <div class="text-caption text-grey-7">Selesaikan e-KYC untuk akses penuh</div>
          </div>
        </div>
        <q-linear-progress :value="onboardingProgress" color="primary" class="q-mt-md" rounded />
        <div class="row q-mt-md q-gutter-sm">
          <q-btn label="Lanjutkan" color="primary" unelevated to="/onboarding" no-caps />
          <q-btn flat label="Lewati" no-caps />
        </div>
      </q-card-section>
    </q-card>

    <!-- Recent Transactions -->
    <q-card flat bordered>
      <q-card-section>
        <div class="row items-center q-mb-sm">
          <div class="text-subtitle1">Mutasi Terbaru</div>
          <q-space />
          <q-btn flat dense label="Lihat Semua" color="primary" :to="'/transactions'" no-caps />
        </div>
        <q-list separator>
          <q-item v-for="txn in recentTransactions" :key="txn.id" clickable>
            <q-item-section avatar>
              <q-avatar :color="txn.type === 'CREDIT' ? 'positive' : 'grey-3'" text-color="white">
                <q-icon :name="txn.type === 'CREDIT' ? 'arrow_downward' : 'arrow_upward'" />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ txn.description }}</q-item-label>
              <q-item-label caption>{{ formatDate(txn.date) }}</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-item-label :class="txn.type === 'CREDIT' ? 'text-positive' : 'text-negative'" class="text-weight-bold">
                {{ txn.type === 'CREDIT' ? '+' : '-' }} {{ formatCurrency(txn.amount) }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="import">
import { ref, computed } from 'vue';
import { useAuthStore } from 'stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const balance = ref(15_750_000);
const isOnboarded = ref(false);
const onboardingProgress = ref(0.4);

const userName = computed(() => authStore.user?.fullName || 'Nasabah');
const userInitials = computed(() => {
  const name = authStore.user?.fullName || 'User';
  const parts = name.trim().split(/\s+/);
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
});

const quickActions = [
  { label: 'Transfer', icon: 'send', to: '/transfer' },
  { label: 'Top Up', icon: 'phone_iphone', to: '/topup' },
  { label: 'QRIS', icon: 'qr_code_scanner', to: '/qris' },
  { label: 'Bayar', icon: 'receipt', to: '/bills' },
];

const recentTransactions = ref([
  { id: '1', description: 'Transfer dari BUDI SANTOSO', date: '2026-01-26', amount: 5_000_000, type: 'CREDIT' },
  { id: '2', description: 'Bayar PLN', date: '2026-01-25', amount: 250_000, type: 'DEBIT' },
  { id: '3', description: 'Top Up GoPay', date: '2026-01-25', amount: 100_000, type: 'DEBIT' },
  { id: '4', description: 'Gaji Januari', date: '2026-01-25', amount: 12_000_000, type: 'CREDIT' },
  { id: '5', description: 'Belanja Tokopedia', date: '2026-01-24', amount: 450_000, type: 'DEBIT' },
]);

function formatCurrency(amount) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(amount);
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' });
}

function navigateTo(path) {
  router.push(path);
}
</script>

<style scoped>
.greeting-card {
  background: transparent;
}
.balance-card {
  background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
  color: white;
}
</style>
