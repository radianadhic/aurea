<template>
  <div class="auth-layout">
    <div class="auth-brand">
      <div class="brand-logo">
        <svg viewBox="0 0 64 64" width="64" height="64">
          <rect width="64" height="64" rx="12" fill="white"/>
          <path d="M16 44V20h8l4 12 4-12h8v24h-6V30l-4 10h-4l-4-10v14H16z" fill="#1e40af"/>
        </svg>
      </div>
      <h1 class="brand-title">MDM Steward</h1>
      <p class="brand-tagline">Master Data Management System</p>
      <p class="brand-bank">Bank XYZ</p>
    </div>
    <div class="auth-content">
      <slot />
    </div>
    <div class="auth-footer">
      <p>© 2026 Bank XYZ. v1.0.0</p>
      <div>
        <NuxtLink to="/help">Help</NuxtLink> ·
        <NuxtLink to="/privacy">Privacy</NuxtLink> ·
        <NuxtLink to="/terms">Terms</NuxtLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  padding: 24px;
  position: relative;
}

.auth-brand {
  position: absolute;
  top: 32px;
  left: 32px;
  color: white;
}

.brand-logo {
  display: inline-block;
  background: white;
  padding: 4px;
  border-radius: 12px;
  margin-bottom: 12px;
}

.brand-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}

.brand-tagline {
  font-size: 14px;
  opacity: 0.9;
  margin: 4px 0 0;
}

.brand-bank {
  font-size: 12px;
  opacity: 0.7;
  margin: 8px 0 0;
}

.auth-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  padding: 48px;
  width: 100%;
  max-width: 440px;
}

.auth-footer {
  position: absolute;
  bottom: 16px;
  left: 0;
  right: 0;
  text-align: center;
  color: white;
  font-size: 12px;
  opacity: 0.7;
}

.auth-footer a {
  color: white;
  text-decoration: none;
  margin: 0 4px;
}

.auth-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 640px) {
  .auth-brand {
    position: static;
    text-align: center;
    margin-bottom: 24px;
  }
  .auth-layout {
    flex-direction: column;
  }
  .auth-content {
    padding: 32px 24px;
  }
}
</style>
