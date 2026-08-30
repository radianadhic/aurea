<template>
  <div class="login-page">
    <h2 class="login-title">Selamat Datang Kembali</h2>
    <p class="login-subtitle">Masuk untuk melanjutkan ke MDM Steward</p>

    <div v-if="mfaRequired" class="mfa-section">
      <div class="mfa-icon">🔐</div>
      <h3 class="mfa-title">Verifikasi Dua Faktor</h3>
      <p class="mfa-desc">
        Masukkan kode 6 digit dari aplikasi authenticator Anda
      </p>
      <el-input
        v-model="mfaCode"
        placeholder="000000"
        size="large"
        maxlength="6"
        style="text-align: center; font-size: 20px; letter-spacing: 6px;"
        @keyup.enter="handleMfaSubmit"
      />
      <el-button
        type="primary"
        size="large"
        :loading="loading"
        :disabled="mfaCode.length !== 6"
        @click="handleMfaSubmit"
        style="width: 100%; margin-top: 16px;"
      >
        Verifikasi
      </el-button>
      <button class="link-btn" @click="cancelMfa">← Kembali ke login</button>
    </div>

    <el-form
      v-else
      ref="loginFormRef"
      :model="form"
      :rules="rules"
      class="login-form"
      @submit.prevent="handleLogin"
    >
      <FormField
        label="Username"
        :error="errors.username"
        required
      >
        <el-input
          v-model="form.username"
          placeholder="Masukkan username"
          size="large"
          :prefix-icon="User"
          autocomplete="username"
        />
      </FormField>

      <FormField
        label="Password"
        :error="errors.password"
        required
      >
        <el-input
          v-model="form.password"
          type="password"
          placeholder="Masukkan password"
          size="large"
          :prefix-icon="Lock"
          show-password
          autocomplete="current-password"
        />
      </FormField>

      <div class="form-options">
        <el-checkbox v-model="form.rememberMe">Ingat saya</el-checkbox>
        <a href="#" class="forgot-link">Lupa password?</a>
      </div>

      <el-alert
        v-if="loginError"
        :title="loginError"
        type="error"
        show-icon
        :closable="false"
        style="margin-bottom: 16px;"
      />

      <el-button
        type="primary"
        size="large"
        :loading="loading"
        @click="handleLogin"
        style="width: 100%;"
      >
        {{ loading ? 'Memproses...' : 'Masuk' }}
      </el-button>

      <div class="login-divider">
        <span>atau</span>
      </div>

      <el-button size="large" @click="handleSsoLogin" style="width: 100%;">
        🔐 Masuk dengan SSO Bank XYZ
      </el-button>

      <p class="login-help">
        Butuh bantuan? Hubungi <a href="mailto:mdm-support@bankxyz.co.id">mdm-support@bankxyz.co.id</a>
      </p>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { User, Lock } from '@element-plus/icons-vue';
import { useAuthStore } from '~/stores/auth';
import { useNotificationStore } from '~/stores/notification';

definePageMeta({
  layout: 'auth',
  auth: false,
});

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

const form = reactive({
  username: '',
  password: '',
  rememberMe: false,
});

const mfaCode = ref('');
const mfaRequired = ref(false);
const loading = ref(false);
const loginError = ref('');
const errors = reactive<Record<string, string>>({});

const rules = {
  username: [{ required: true, message: 'Username wajib diisi', trigger: 'blur' }],
  password: [{ required: true, message: 'Password wajib diisi', trigger: 'blur' }],
};

async function handleLogin() {
  if (!form.username || !form.password) {
    if (!form.username) errors.username = 'Username wajib diisi';
    if (!form.password) errors.password = 'Password wajib diisi';
    return;
  }

  Object.keys(errors).forEach((k) => delete errors[k]);
  loading.value = true;
  loginError.value = '';

  try {
    const result = await authStore.login(form.username, form.password);

    if ('mfaRequired' in result && result.mfaRequired) {
      mfaRequired.value = true;
      notificationStore.showInfo('Masukkan kode MFA Anda');
      return;
    }

    notificationStore.showSuccess(`Selamat datang, ${authStore.fullName}!`);
    const redirect = (route.query.redirect as string) || '/dashboard';
    await router.push(redirect);
  } catch (e: any) {
    loginError.value = e.response?.data?.message || e.message || 'Login gagal. Periksa kembali kredensial Anda.';
  } finally {
    loading.value = false;
  }
}

async function handleMfaSubmit() {
  if (mfaCode.value.length !== 6) return;
  loading.value = true;
  try {
    await authStore.login(form.username, form.password, mfaCode.value);
    notificationStore.showSuccess(`Selamat datang, ${authStore.fullName}!`);
    const redirect = (route.query.redirect as string) || '/dashboard';
    await router.push(redirect);
  } catch (e: any) {
    loginError.value = e.response?.data?.message || 'Kode MFA salah';
  } finally {
    loading.value = false;
  }
}

function cancelMfa() {
  mfaRequired.value = false;
  mfaCode.value = '';
  loginError.value = '';
}

function handleSsoLogin() {
  notificationStore.showInfo('Redirecting to SSO...');
  // In real app, redirect to Keycloak
  setTimeout(() => {
    window.location.href = `${useRuntimeConfig().public.keycloakUrl}/realms/mdm-dev/protocol/openid-connect/auth?client_id=mdm-steward-ui&redirect_uri=${window.location.origin}/auth/callback`;
  }, 500);
}
</script>

<style scoped>
.login-page {
  width: 100%;
}

.login-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px;
  text-align: center;
}

.login-subtitle {
  font-size: 14px;
  color: #6b7280;
  text-align: center;
  margin: 0 0 24px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
}

.forgot-link {
  color: #1e40af;
  text-decoration: none;
}

.forgot-link:hover {
  text-decoration: underline;
}

.login-divider {
  text-align: center;
  position: relative;
  margin: 8px 0;
}

.login-divider::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  background: #e5e7eb;
}

.login-divider span {
  background: white;
  padding: 0 12px;
  font-size: 13px;
  color: #6b7280;
  position: relative;
}

.login-help {
  text-align: center;
  font-size: 12px;
  color: #6b7280;
  margin: 16px 0 0;
}

.login-help a {
  color: #1e40af;
  text-decoration: none;
}

.mfa-section {
  text-align: center;
}

.mfa-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.mfa-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px;
}

.mfa-desc {
  font-size: 13px;
  color: #6b7280;
  margin: 0 0 24px;
}

.link-btn {
  background: transparent;
  border: 0;
  color: #1e40af;
  cursor: pointer;
  font-size: 13px;
  margin-top: 12px;
  padding: 4px 8px;
}
</style>
