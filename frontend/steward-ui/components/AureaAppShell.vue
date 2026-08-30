<template>
  <div class="aurea-app-container">
    <!-- AUREA SPLASH (only on first load) -->
    <Transition name="splash-fade">
      <div v-if="showSplash" class="aurea-splash-screen" @click="hideSplash">
        <div class="aurea-splash-bg">
          <div v-for="i in 8" :key="i" class="aurea-particle"
               :style="`left: ${i*12}%; --drift: ${(i%2===0?40:-40)}px; animation-delay: ${i*0.3}s;`"></div>
        </div>
        <div class="aurea-splash-content">
          <div class="aurea-splash-mark">
            <div class="aurea-splash-circle"></div>
            <div class="aurea-splash-a">A</div>
            <div class="aurea-splash-dots">
              <div class="aurea-splash-dot"></div>
              <div class="aurea-splash-dot"></div>
              <div class="aurea-splash-dot"></div>
            </div>
          </div>
          <h1 class="aurea-splash-text">AUREA</h1>
          <div class="aurea-splash-divider"></div>
          <p class="aurea-splash-tagline">STEWARD</p>
          <div class="aurea-splash-loader"></div>
          <p class="aurea-splash-hint">Klik untuk skip</p>
        </div>
      </div>
    </Transition>

    <div class="aurea-app-shell" v-show="!showSplash">
      <!-- AUREA Sidebar (Navy + Gold) -->
      <aside class="aurea-sidebar" :class="{ open: sidebarOpen }">
        <div class="aurea-sidebar-logo">
          <img src="/logo-mark.svg" alt="AUREA" class="aurea-sidebar-icon" />
          <div>
            <div class="aurea-sidebar-title">AUREA</div>
            <div class="aurea-sidebar-subtitle">Steward Console</div>
          </div>
        </div>

        <nav class="aurea-sidebar-menu">
          <div class="aurea-menu-section">Main</div>
          <NuxtLink to="/dashboard" class="aurea-menu-item" exact-active-class="active">
            <span class="aurea-menu-icon">📊</span>
            <span>Dashboard</span>
          </NuxtLink>
          <NuxtLink to="/customers" class="aurea-menu-item" active-class="active">
            <span class="aurea-menu-icon">👥</span>
            <span>Pencarian Nasabah</span>
          </NuxtLink>
          <NuxtLink to="/customers/new" class="aurea-menu-item">
            <span class="aurea-menu-icon">➕</span>
            <span>Nasabah Baru</span>
          </NuxtLink>

          <div class="aurea-menu-section">Operasional</div>
          <NuxtLink to="/matching" class="aurea-menu-item">
            <span class="aurea-menu-icon">🔄</span>
            <span>Antrian Matching</span>
          </NuxtLink>
          <NuxtLink to="/exceptions" class="aurea-menu-item">
            <span class="aurea-menu-icon">⚠️</span>
            <span>Exception Queue</span>
          </NuxtLink>
          <NuxtLink to="/kyc" class="aurea-menu-item">
            <span class="aurea-menu-icon">🛡️</span>
            <span>KYC Review</span>
          </NuxtLink>

          <div class="aurea-menu-section">Compliance</div>
          <NuxtLink to="/audit" class="aurea-menu-item">
            <span class="aurea-menu-icon">📋</span>
            <span>Audit Trail</span>
          </NuxtLink>
          <NuxtLink to="/reports" class="aurea-menu-item">
            <span class="aurea-menu-icon">📈</span>
            <span>Laporan</span>
          </NuxtLink>
        </nav>

        <div class="aurea-sidebar-footer">
          <div class="aurea-version">AUREA v1.0.0</div>
          <div class="aurea-tagline-mini">THE GOLD STANDARD</div>
        </div>
      </aside>

      <!-- Main content -->
      <div class="aurea-main-content">
        <!-- Top bar -->
        <header class="aurea-top-bar">
          <div class="aurea-top-bar-left">
            <button class="aurea-hamburger" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle menu">
              <span></span><span></span><span></span>
            </button>
            <div class="aurea-page-title-wrapper">
              <h1 class="aurea-page-title">{{ pageTitle }}</h1>
              <span class="aurea-page-badge">AUREA</span>
            </div>
          </div>
          <div class="aurea-top-bar-right">
            <div class="aurea-search-box">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Cari CIF, nama, NIK..."
                @keyup.enter="handleGlobalSearch"
              />
              <span class="aurea-search-icon">🔍</span>
            </div>

            <button class="aurea-icon-btn" title="Notifikasi">
              <span>🔔</span>
              <span v-if="unreadCount > 0" class="aurea-badge">{{ unreadCount }}</span>
            </button>

            <div class="aurea-user-menu" @click="showUserMenu = !showUserMenu">
              <div class="aurea-user-avatar">{{ authStore.initials }}</div>
              <div class="aurea-user-info">
                <div class="aurea-user-name">{{ authStore.fullName }}</div>
                <div class="aurea-user-role">{{ userRole }}</div>
              </div>
              <transition name="dropdown">
                <div v-if="showUserMenu" class="aurea-user-dropdown" @click.stop>
                  <div class="aurea-dropdown-header">
                    <div class="aurea-user-name">{{ authStore.fullName }}</div>
                    <div class="aurea-user-email">{{ authStore.user?.email }}</div>
                  </div>
                  <hr/>
                  <NuxtLink to="/profile" class="aurea-dropdown-item">👤 Profil Saya</NuxtLink>
                  <NuxtLink to="/settings" class="aurea-dropdown-item">⚙️ Pengaturan</NuxtLink>
                  <hr/>
                  <button class="aurea-dropdown-item" @click="handleLogout">
                    🚪 Logout
                  </button>
                </div>
              </transition>
            </div>
          </div>
        </header>

        <!-- Page content -->
        <main class="aurea-page-content fade-in">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '~/stores/auth';
import { useNotificationStore } from '~/stores/notification';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

const sidebarOpen = ref(false);
const showUserMenu = ref(false);
const searchQuery = ref('');
const unreadCount = ref(3);
const showSplash = ref(false);

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/dashboard': 'Dashboard',
    '/customers': 'Pencarian Nasabah',
    '/customers/new': 'Nasabah Baru',
    '/matching': 'Antrian Matching',
    '/exceptions': 'Exception Queue',
    '/kyc': 'KYC Review',
    '/audit': 'Audit Trail',
    '/reports': 'Laporan',
  };

  if (titles[route.path]) return titles[route.path];

  for (const path of Object.keys(titles)) {
    if (route.path.startsWith(path) && path !== '/dashboard') {
      return titles[path];
    }
  }

  return 'AUREA Steward';
});

const userRole = computed(() => {
  const roles = authStore.user?.roles || [];
  if (roles.includes('SUPER_ADMIN')) return 'Super Admin';
  if (roles.includes('ADMIN')) return 'Administrator';
  if (roles.includes('STEWARD_CIF')) return 'Steward CIF';
  if (roles.includes('ANALYST')) return 'Analyst';
  if (roles.includes('COMPLIANCE')) return 'Compliance';
  if (roles.includes('AUDITOR')) return 'Auditor';
  return roles[0] || 'User';
});

function handleGlobalSearch() {
  if (!searchQuery.value.trim()) return;
  router.push({ path: '/customers', query: { q: searchQuery.value } });
}

async function handleLogout() {
  await authStore.logout();
  notificationStore.showInfo('Anda telah logout');
}

function hideSplash() {
  showSplash.value = false;
  // Persist "seen" state for session
  if (typeof sessionStorage !== 'undefined') {
    sessionStorage.setItem('aurea-splash-seen', '1');
  }
}

function closeOnOutside() {
  showUserMenu.value = false;
}

onMounted(() => {
  document.addEventListener('click', closeOnOutside);
  // Show splash only first time in session
  if (typeof sessionStorage !== 'undefined' && !sessionStorage.getItem('aurea-splash-seen')) {
    showSplash.value = true;
    // Auto-hide after 3.5s
    setTimeout(() => {
      if (showSplash.value) hideSplash();
    }, 3500);
  }
});

onUnmounted(() => {
  document.removeEventListener('click', closeOnOutside);
});
</script>

<style scoped>
/* AUREA BRAND VARIABLES */
.aurea-app-container {
  --aurea-gold-500: #D4AF37;
  --aurea-gold-300: #FFD764;
  --aurea-gold-700: #B8860B;
  --aurea-navy-600: #0A1929;
  --aurea-navy-500: #1A2F47;
  --aurea-navy-200: #B3C2D2;
  --aurea-navy-300: #809AB3;
  --aurea-navy-400: #4D7193;

  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
}

/* ============================================
   AUREA SPLASH SCREEN
   ============================================ */
.aurea-splash-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0A1929 0%, #1A2F47 100%);
  cursor: pointer;
  overflow: hidden;
}
.aurea-splash-bg { position: absolute; inset: 0; pointer-events: none; }
.aurea-particle {
  position: absolute;
  bottom: -20px;
  width: 3px; height: 3px;
  background: #D4AF37;
  border-radius: 50%;
  opacity: 0;
  animation: aurea-particle-float 6s linear infinite;
}
@keyframes aurea-particle-float {
  0% { opacity: 0; transform: translateY(0) translateX(0); }
  10% { opacity: 0.6; }
  90% { opacity: 0.6; }
  100% { opacity: 0; transform: translateY(-100vh) translateX(var(--drift, 30px)); }
}
.aurea-splash-content {
  position: relative; z-index: 1;
  display: flex; flex-direction: column; align-items: center;
  color: white;
}
.aurea-splash-mark {
  position: relative;
  width: 150px; height: 150px;
  margin-bottom: 24px;
  animation: aurea-mark-in 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s both;
}
@keyframes aurea-mark-in {
  0% { transform: scale(0); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.aurea-splash-circle {
  position: absolute; inset: 0;
  background: linear-gradient(135deg, #1A2F47 0%, #0A1929 100%);
  border-radius: 50%;
  box-shadow: 0 0 40px rgba(212, 175, 55, 0.3);
  animation: aurea-pulse 2.5s ease-in-out infinite;
}
@keyframes aurea-pulse {
  0%, 100% { box-shadow: 0 0 30px rgba(212, 175, 55, 0.2); }
  50% { box-shadow: 0 0 60px rgba(212, 175, 55, 0.5); }
}
.aurea-splash-a {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 76px; font-weight: 700;
  color: #D4AF37;
  text-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
}
.aurea-splash-dots {
  position: absolute; bottom: 24px; left: 50%;
  transform: translateX(-50%);
  display: flex; gap: 8px;
}
.aurea-splash-dot {
  width: 7px; height: 7px;
  background: #FFD764; border-radius: 50%;
  box-shadow: 0 0 8px rgba(255, 215, 100, 0.8);
  animation: aurea-dot-pulse 1.5s ease-in-out infinite;
}
.aurea-splash-dot:nth-child(2) { animation-delay: 0.2s; }
.aurea-splash-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes aurea-dot-pulse {
  0%, 100% { transform: scale(1); opacity: 0.6; }
  50% { transform: scale(1.4); opacity: 1; }
}
.aurea-splash-text {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 44px; font-weight: 700;
  background: linear-gradient(135deg, #FFD764 0%, #D4AF37 50%, #B8860B 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 11px;
  margin: 0 0 0 11px;
  animation: aurea-text-reveal 1s ease-out 0.6s both;
}
@keyframes aurea-text-reveal {
  0% { opacity: 0; letter-spacing: 28px; filter: blur(10px); }
  100% { opacity: 1; letter-spacing: 11px; filter: blur(0); }
}
.aurea-splash-divider {
  width: 0; height: 2px;
  background: linear-gradient(90deg, transparent 0%, #D4AF37 50%, transparent 100%);
  margin: 12px 0;
  animation: aurea-divider-expand 0.8s ease-out 1.2s forwards;
}
@keyframes aurea-divider-expand { 0% { width: 0; } 100% { width: 280px; } }
.aurea-splash-tagline {
  font-family: Georgia, serif;
  font-size: 12px;
  color: var(--aurea-gold-300);
  letter-spacing: 5px;
  margin: 0 0 0 5px;
  opacity: 0;
  animation: aurea-tagline-fade 1s ease-out 1.5s forwards;
}
@keyframes aurea-tagline-fade {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
.aurea-splash-loader {
  margin-top: 24px; width: 160px; height: 2px;
  background: rgba(212, 175, 55, 0.2);
  border-radius: 2px; overflow: hidden; position: relative;
  opacity: 0;
  animation: aurea-loader-show 0.3s ease-out 2s forwards;
}
@keyframes aurea-loader-show { to { opacity: 1; } }
.aurea-splash-loader::before {
  content: '';
  position: absolute; top: 0; left: -50%; width: 50%; height: 100%;
  background: linear-gradient(90deg, transparent, #D4AF37, transparent);
  border-radius: 2px;
  animation: aurea-loader-slide 1.8s ease-in-out infinite;
}
@keyframes aurea-loader-slide { 0% { left: -50%; } 100% { left: 100%; } }
.aurea-splash-hint {
  position: absolute; bottom: -80px;
  font-size: 11px; color: var(--aurea-navy-300);
  letter-spacing: 2px;
  opacity: 0;
  animation: aurea-loader-show 0.3s ease-out 2.5s forwards;
}
.splash-fade-leave-active { transition: opacity 0.5s ease; }
.splash-fade-leave-to { opacity: 0; }

/* ============================================
   AUREA APP SHELL
   ============================================ */
.aurea-app-shell {
  display: flex;
  min-height: 100vh;
  background: #F8F9FA;
}

/* AUREA Sidebar (Navy + Gold) */
.aurea-sidebar {
  width: 240px;
  background: linear-gradient(180deg, #0A1929 0%, #1A2F47 100%);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; bottom: 0; left: 0;
  z-index: 50;
  box-shadow: 4px 0 16px rgba(10, 25, 41, 0.1);
  transition: transform 0.3s ease;
  border-right: 1px solid rgba(212, 175, 55, 0.2);
}
.aurea-sidebar-logo {
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.15);
}
.aurea-sidebar-icon {
  width: 36px; height: 36px;
  filter: drop-shadow(0 0 8px rgba(212, 175, 55, 0.4));
}
.aurea-sidebar-title {
  font-family: Georgia, serif;
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, #FFD764 0%, #D4AF37 50%, #B8860B 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 4px;
  line-height: 1.1;
}
.aurea-sidebar-subtitle {
  font-size: 9px;
  color: var(--aurea-navy-200);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 2px;
}

.aurea-sidebar-menu {
  flex: 1;
  overflow-y: auto;
  padding: 12px 0;
}
.aurea-menu-section {
  padding: 12px 20px 6px;
  font-size: 10px;
  font-weight: 700;
  color: var(--aurea-gold-300);
  text-transform: uppercase;
  letter-spacing: 2px;
}
.aurea-menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  position: relative;
}
.aurea-menu-item:hover {
  background: rgba(212, 175, 55, 0.1);
  color: var(--aurea-gold-300);
}
.aurea-menu-item.active {
  background: linear-gradient(90deg, rgba(212, 175, 55, 0.2) 0%, transparent 100%);
  color: var(--aurea-gold-300);
  font-weight: 600;
}
.aurea-menu-item.active::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, #FFD764 0%, #B8860B 100%);
}
.aurea-menu-icon { font-size: 16px; flex-shrink: 0; }

.aurea-sidebar-footer {
  padding: 12px 20px;
  border-top: 1px solid rgba(212, 175, 55, 0.15);
  text-align: center;
}
.aurea-version {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--aurea-gold-300);
  font-weight: 600;
}
.aurea-tagline-mini {
  font-size: 8px;
  color: var(--aurea-navy-300);
  letter-spacing: 2px;
  margin-top: 2px;
}

/* Main content */
.aurea-main-content {
  flex: 1;
  margin-left: 240px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.aurea-top-bar {
  background: white;
  border-bottom: 2px solid var(--aurea-gold-500);
  height: 64px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 40;
  box-shadow: 0 2px 8px rgba(10, 25, 41, 0.04);
}
.aurea-top-bar-left { display: flex; align-items: center; gap: 16px; }
.aurea-hamburger {
  display: none;
  background: transparent;
  border: 0;
  cursor: pointer;
  padding: 8px;
  flex-direction: column;
  gap: 4px;
}
.aurea-hamburger span {
  display: block;
  width: 20px;
  height: 2px;
  background: var(--aurea-navy-600);
  border-radius: 2px;
}
.aurea-page-title-wrapper { display: flex; align-items: center; gap: 12px; }
.aurea-page-title {
  font-family: Georgia, serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--aurea-navy-600);
  margin: 0;
  letter-spacing: 0.5px;
}
.aurea-page-badge {
  display: inline-block;
  padding: 2px 8px;
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  color: var(--aurea-navy-600);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
  border-radius: 4px;
}
.aurea-top-bar-right { display: flex; align-items: center; gap: 16px; }

.aurea-search-box { position: relative; width: 320px; }
.aurea-search-box input {
  width: 100%;
  padding: 8px 36px 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}
.aurea-search-box input:focus {
  border-color: var(--aurea-gold-500);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.15);
}
.aurea-search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

.aurea-icon-btn {
  position: relative;
  background: transparent;
  border: 0;
  padding: 8px;
  cursor: pointer;
  font-size: 18px;
  border-radius: 8px;
  transition: all 0.2s;
}
.aurea-icon-btn:hover { background: rgba(212, 175, 55, 0.1); }
.aurea-badge {
  position: absolute;
  top: 4px; right: 4px;
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  color: var(--aurea-navy-600);
  font-size: 10px;
  font-weight: 700;
  padding: 2px 5px;
  border-radius: 9999px;
  min-width: 16px;
  text-align: center;
}

.aurea-user-menu {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 4px 8px 4px 4px;
  border-radius: 8px;
  transition: background 0.2s;
}
.aurea-user-menu:hover { background: rgba(212, 175, 55, 0.1); }
.aurea-user-avatar {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  color: var(--aurea-navy-600);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700;
  font-size: 13px;
}
.aurea-user-info { display: flex; flex-direction: column; }
.aurea-user-name { font-size: 14px; font-weight: 600; color: var(--aurea-navy-600); line-height: 1.2; }
.aurea-user-role { font-size: 11px; color: #6b7280; }

.aurea-user-dropdown {
  position: absolute;
  right: 0; top: calc(100% + 8px);
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.2);
  min-width: 220px;
  z-index: 1000;
  padding: 8px 0;
}
.aurea-dropdown-header { padding: 12px 16px; }
.aurea-dropdown-header .aurea-user-name { font-size: 14px; }
.aurea-user-email { font-size: 12px; color: #6b7280; }
.aurea-dropdown-item {
  display: block;
  width: 100%;
  text-align: left;
  background: transparent;
  border: 0;
  padding: 10px 16px;
  font-size: 14px;
  color: var(--aurea-navy-600);
  cursor: pointer;
  text-decoration: none;
  transition: background 0.15s;
}
.aurea-dropdown-item:hover { background: rgba(212, 175, 55, 0.1); }
hr { margin: 4px 0; border: 0; border-top: 1px solid #e5e7eb; }

.aurea-page-content { flex: 1; padding: 24px; }

.fade-in { animation: aurea-fade-in 0.3s ease; }
@keyframes aurea-fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-enter-active, .dropdown-leave-active { transition: all 0.2s ease; }
.dropdown-enter-from { opacity: 0; transform: translateY(-10px); }
.dropdown-leave-to { opacity: 0; transform: translateY(-10px); }

@media (max-width: 1024px) {
  .aurea-sidebar { transform: translateX(-100%); }
  .aurea-sidebar.open { transform: translateX(0); }
  .aurea-main-content { margin-left: 0; }
  .aurea-hamburger { display: flex; }
  .aurea-search-box { width: 180px; }
  .aurea-user-info { display: none; }
}
</style>
