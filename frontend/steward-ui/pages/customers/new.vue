<template>
  <div class="new-customer">
    <PageHeader
      :back="true"
      title="Nasabah Baru"
      subtitle="Lengkapi data nasabah baru. Field bertanda * wajib diisi."
      @back="navigateTo('/customers')"
    >
      <template #actions>
        <el-button @click="resetForm">Reset</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ submitting ? 'Menyimpan...' : 'Simpan' }}
        </el-button>
      </template>
    </PageHeader>

    <div class="form-content">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        class="customer-form"
      >
        <!-- Tipe Nasabah -->
        <div class="form-section">
          <h3 class="section-title">1. Tipe Nasabah</h3>
          <el-radio-group v-model="form.customerType" class="type-selector">
            <el-radio-button value="INDIVIDUAL">👤 Individual</el-radio-button>
            <el-radio-button value="CORPORATE">🏢 Corporate</el-radio-button>
            <el-radio-button value="SYARIAH">☪️ Syariah</el-radio-button>
          </el-radio-group>
        </div>

        <!-- Informasi Pribadi -->
        <div class="form-section">
          <h3 class="section-title">2. Informasi Pribadi</h3>
          <div class="form-grid">
            <FormField label="Nama Lengkap" required :error="errors.fullName">
              <el-input v-model="form.fullName" placeholder="Sesuai KTP" />
            </FormField>
            <FormField label="Nama Legal" :error="errors.legalName">
              <el-input v-model="form.legalName" placeholder="Untuk badan usaha" />
            </FormField>
            <FormField label="Tempat Lahir" :error="errors.placeOfBirth">
              <el-input v-model="form.placeOfBirth" placeholder="Kota tempat lahir" />
            </FormField>
            <FormField label="Tanggal Lahir" :error="errors.dateOfBirth">
              <DatePicker v-model="form.dateOfBirth" :max-date="new Date()" />
            </FormField>
            <FormField label="Jenis Kelamin" :error="errors.gender">
              <el-radio-group v-model="form.gender">
                <el-radio value="MALE">Laki-laki</el-radio>
                <el-radio value="FEMALE">Perempuan</el-radio>
              </el-radio-group>
            </FormField>
            <FormField label="Kewarganegaraan">
              <el-select v-model="form.nationality" placeholder="Pilih" filterable>
                <el-option label="🇮🇩 Indonesia" value="ID" />
                <el-option label="🇲🇾 Malaysia" value="MY" />
                <el-option label="🇸🇬 Singapura" value="SG" />
                <el-option label="🇯🇵 Jepang" value="JP" />
                <el-option label="🇰🇷 Korea Selatan" value="KR" />
                <el-option label="🇺🇸 Amerika Serikat" value="US" />
              </el-select>
            </FormField>
            <FormField label="Status Pernikahan">
              <el-select v-model="form.maritalStatus" placeholder="Pilih">
                <el-option label="Belum Menikah" value="SINGLE" />
                <el-option label="Menikah" value="MARRIED" />
                <el-option label="Cerai" value="DIVORCED" />
                <el-option label="Duda/Janda" value="WIDOWED" />
              </el-select>
            </FormField>
            <FormField label="Agama">
              <el-select v-model="form.religion" placeholder="Pilih">
                <el-option v-for="r in religions" :key="r" :value="r" :label="r" />
              </el-select>
            </FormField>
            <FormField label="Pekerjaan">
              <el-input v-model="form.occupation" placeholder="Pekerjaan saat ini" />
            </FormField>
            <FormField label="Pendapatan/Bulan">
              <el-input-number
                v-model="form.monthlyIncome"
                :min="0"
                :step="1000000"
                placeholder="0"
                style="width: 100%"
              />
            </FormField>
          </div>
        </div>

        <!-- Identitas -->
        <div class="form-section">
          <h3 class="section-title">3. Identitas</h3>
          <div class="form-grid">
            <FormField label="NIK" :error="errors.nik">
              <el-input
                v-model="form.nik"
                placeholder="16 digit NIK"
                maxlength="16"
                show-word-limit
              />
            </FormField>
            <FormField label="NPWP">
              <el-input v-model="form.npwp" placeholder="15 digit NPWP" maxlength="15" />
            </FormField>
            <FormField label="No. Paspor">
              <el-input v-model="form.passport" placeholder="Jika ada" />
            </FormField>
            <FormField label="Email">
              <el-input v-model="form.email" type="email" placeholder="email@example.com" />
            </FormField>
            <FormField label="No. HP" :error="errors.mobilePhone">
              <el-input v-model="form.mobilePhone" placeholder="08xxxxxxxxxx" />
            </FormField>
            <FormField label="Cabang">
              <el-select v-model="form.branchId" placeholder="Pilih cabang" filterable>
                <el-option label="KCP Jakarta Pusat" value="JKT-001" />
                <el-option label="KCP Jakarta Selatan" value="JKT-002" />
                <el-option label="KCP Bandung" value="BDG-001" />
                <el-option label="KCP Surabaya" value="SBY-001" />
              </el-select>
            </FormField>
          </div>
        </div>

        <!-- Alamat -->
        <div class="form-section">
          <h3 class="section-title">4. Alamat</h3>
          <div class="form-grid">
            <FormField label="Alamat Lengkap" class="full-width">
              <el-input
                v-model="form.address"
                type="textarea"
                :rows="3"
                placeholder="Jalan, nomor rumah, RT/RW, kelurahan, kecamatan"
              />
            </FormField>
            <FormField label="Provinsi">
              <el-select v-model="form.province" placeholder="Pilih provinsi" filterable>
                <el-option label="DKI Jakarta" value="DKI" />
                <el-option label="Jawa Barat" value="JBR" />
                <el-option label="Jawa Tengah" value="JTG" />
                <el-option label="Jawa Timur" value="JTM" />
                <el-option label="Banten" value="BTN" />
              </el-select>
            </FormField>
            <FormField label="Kota">
              <el-input v-model="form.city" placeholder="Kota" />
            </FormField>
            <FormField label="Kode Pos">
              <el-input v-model="form.postalCode" maxlength="5" placeholder="12345" />
            </FormField>
          </div>
        </div>

        <!-- Risk Profile -->
        <div class="form-section">
          <h3 class="section-title">5. Risk Assessment</h3>
          <div class="form-grid">
            <FormField label="Risk Profile (Auto)">
              <div class="risk-display" :class="`risk-${autoRisk.toLowerCase()}`">
                <span class="risk-dot"></span>
                {{ autoRisk }} Risk
                <small>(auto-calculated)</small>
              </div>
            </FormField>
            <FormField label="Status PEP">
              <el-switch v-model="form.pepStatus" active-text="Ya" inactive-text="Tidak" />
              <small class="hint">Politically Exposed Person</small>
            </FormField>
            <FormField label="Tags" class="full-width">
              <el-select
                v-model="form.tags"
                multiple
                filterable
                allow-create
                placeholder="Tambah tag"
              >
                <el-option label="VIP" value="VIP" />
                <el-option label="Nasabah Prioritas" value="PRIORITAS" />
                <el-option label="Blacklist Watch" value="WATCH" />
                <el-option label="Korporat" value="KORPORAT" />
              </el-select>
            </FormField>
          </div>
        </div>

        <!-- Submit -->
        <div class="form-actions">
          <el-button @click="navigateTo('/customers')">Batal</el-button>
          <el-button @click="resetForm">Reset</el-button>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            💾 Simpan Customer
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { useCustomerStore } from '~/stores/customer';
import { useNotificationStore } from '~/stores/notification';

definePageMeta({
  layout: 'default',
  middleware: 'auth',
  roles: ['STEWARD_CIF', 'ADMIN', 'SUPER_ADMIN'],
});

const customerStore = useCustomerStore();
const notificationStore = useNotificationStore();

const formRef = ref();
const submitting = ref(false);
const errors = reactive<Record<string, string>>({});

const form = reactive({
  customerType: 'INDIVIDUAL',
  fullName: '',
  legalName: '',
  placeOfBirth: '',
  dateOfBirth: '',
  gender: '',
  nationality: 'ID',
  maritalStatus: '',
  religion: '',
  occupation: '',
  monthlyIncome: undefined as number | undefined,
  nik: '',
  npwp: '',
  passport: '',
  email: '',
  mobilePhone: '',
  branchId: '',
  address: '',
  province: '',
  city: '',
  postalCode: '',
  pepStatus: false,
  tags: [] as string[],
});

const religions = ['ISLAM', 'KRISTEN', 'KATOLIK', 'HINDU', 'BUDDHA', 'KONGHUCU', 'LAINNYA'];

const rules = {
  fullName: [
    { required: true, message: 'Nama lengkap wajib diisi', trigger: 'blur' },
    { min: 3, message: 'Minimal 3 karakter', trigger: 'blur' },
  ],
  customerType: [
    { required: true, message: 'Pilih tipe nasabah', trigger: 'change' },
  ],
  dateOfBirth: [
    {
      validator: (_: any, value: string, callback: any) => {
        if (!value) {
          callback(new Error('Tanggal lahir wajib diisi'));
        } else {
          const age = new Date().getFullYear() - new Date(value).getFullYear();
          if (age < 17) callback(new Error('Usia minimal 17 tahun'));
          else if (age > 120) callback(new Error('Tanggal lahir tidak valid'));
          else callback();
        }
      },
      trigger: 'change',
    },
  ],
  nik: [
    {
      validator: (_: any, value: string, callback: any) => {
        if (value && !/^[0-9]{16}$/.test(value)) {
          callback(new Error('NIK harus 16 digit angka'));
        } else {
          callback();
        }
      },
      trigger: 'blur',
    },
  ],
  mobilePhone: [
    {
      validator: (_: any, value: string, callback: any) => {
        if (value && !/^(\+62|62|0)[0-9]{8,13}$/.test(value)) {
          callback(new Error('Nomor telepon tidak valid'));
        } else {
          callback();
        }
      },
      trigger: 'blur',
    },
  ],
  email: [
    {
      validator: (_: any, value: string, callback: any) => {
        if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          callback(new Error('Format email tidak valid'));
        } else {
          callback();
        }
      },
      trigger: 'blur',
    },
  ],
};

const autoRisk = computed(() => {
  let score = 0;
  if (form.monthlyIncome && form.monthlyIncome > 50_000_000) score -= 1;
  if (form.pepStatus) score += 3;
  if (form.nationality && form.nationality !== 'ID') score += 1;
  if (form.dateOfBirth) {
    const age = new Date().getFullYear() - new Date(form.dateOfBirth).getFullYear();
    if (age < 21) score += 1;
    if (age > 65) score += 1;
  }
  if (score >= 2) return 'HIGH';
  if (score >= 1) return 'MEDIUM';
  return 'LOW';
});

function resetForm() {
  Object.assign(form, {
    customerType: 'INDIVIDUAL',
    fullName: '',
    legalName: '',
    placeOfBirth: '',
    dateOfBirth: '',
    gender: '',
    nationality: 'ID',
    maritalStatus: '',
    religion: '',
    occupation: '',
    monthlyIncome: undefined,
    nik: '',
    npwp: '',
    passport: '',
    email: '',
    mobilePhone: '',
    branchId: '',
    address: '',
    province: '',
    city: '',
    postalCode: '',
    pepStatus: false,
    tags: [],
  });
  Object.keys(errors).forEach((k) => delete errors[k]);
  formRef.value?.clearValidate();
}

async function handleSubmit() {
  if (!formRef.value) return;
  try {
    await formRef.value.validate();
    submitting.value = true;
    const created = await customerStore.create(form);
    notificationStore.showSuccess(`Customer ${created.cifNumber} berhasil dibuat`);
    navigateTo(`/customers/${created.id}`);
  } catch (e: any) {
    if (e?.errors) {
      Object.assign(errors, e.errors);
    } else {
      notificationStore.showError('Gagal membuat customer');
    }
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.new-customer {
  min-height: 100vh;
}

.form-content {
  padding: 24px 32px;
  max-width: 1100px;
  margin: 0 auto;
}

.customer-form {
  background: white;
  border-radius: 12px;
  padding: 32px;
  border: 1px solid #e5e7eb;
}

.form-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f3f4f6;
}

.form-section:last-of-type {
  border-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px;
}

.type-selector {
  display: flex;
  gap: 12px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-grid :deep(.full-width) {
  grid-column: 1 / -1;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

.risk-display {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 500;
}

.risk-display small {
  color: #6b7280;
  font-size: 11px;
  font-weight: 400;
}

.risk-display.risk-low {
  background: rgba(22, 163, 74, 0.1);
  color: #15803d;
}

.risk-display.risk-medium {
  background: rgba(234, 88, 12, 0.1);
  color: #c2410c;
}

.risk-display.risk-high {
  background: rgba(220, 38, 38, 0.1);
  color: #b91c1c;
}

.risk-display .risk-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.hint {
  display: block;
  margin-top: 4px;
  color: #6b7280;
  font-size: 11px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding-top: 24px;
  margin-top: 24px;
  border-top: 1px solid #e5e7eb;
}
</style>
