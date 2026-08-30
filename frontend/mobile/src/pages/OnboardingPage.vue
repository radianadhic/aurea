<template>
  <q-page padding>
    <div class="text-h5 q-mb-md">Onboarding Nasabah Baru</div>
    <div class="text-caption text-grey-7 q-mb-lg">Lengkapi data diri untuk membuka rekening</div>

    <q-stepper v-model="step" header-nav animated color="primary" done-color="positive" active-color="primary" inactive-color="grey-5">
      <!-- Step 1: Personal Info -->
      <q-step :name="1" title="Data Diri" icon="person" :done="step > 1">
        <div class="q-gutter-md">
          <q-input v-model="form.fullName" label="Nama Lengkap" outlined dense :rules="[required]" />
          <q-input v-model="form.nik" label="NIK" outlined dense mask="################" hint="16 digit" />
          <q-input v-model="form.placeOfBirth" label="Tempat Lahir" outlined dense />
          <q-input v-model="form.dateOfBirth" label="Tanggal Lahir" outlined dense type="date" />
          <q-select v-model="form.gender" :options="genderOptions" label="Jenis Kelamin" outlined dense emit-value map-options />
          <q-input v-model="form.email" label="Email" outlined dense type="email" />
          <q-input v-model="form.mobilePhone" label="No. HP" outlined dense mask="##############" />
        </div>
      </q-step>

      <!-- Step 2: Address -->
      <q-step :name="2" title="Alamat" icon="location_on" :done="step > 2">
        <div class="q-gutter-md">
          <q-input v-model="form.address" label="Alamat Lengkap" outlined dense type="textarea" autogrow />
          <div class="row q-gutter-md">
            <q-input v-model="form.rt" label="RT" outlined dense mask="###" class="col-2" />
            <q-input v-model="form.rw" label="RW" outlined dense mask="###" class="col-2" />
            <q-input v-model="form.postalCode" label="Kode Pos" outlined dense mask="#####" class="col-3" />
          </div>
          <q-select v-model="form.province" :options="provinceOptions" label="Provinsi" outlined dense />
          <q-select v-model="form.city" :options="cityOptions" label="Kota" outlined dense />
        </div>
      </q-step>

      <!-- Step 3: Product Selection -->
      <q-step :name="3" title="Pilih Produk" icon="account_balance" :done="step > 3">
        <div class="text-subtitle1 q-mb-md">Pilih jenis rekening:</div>
        <q-list bordered separator>
          <q-item v-for="product in products" :key="product.code" tag="label" v-ripple>
            <q-item-section avatar>
              <q-radio v-model="form.productCode" :val="product.code" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ product.name }}</q-item-label>
              <q-item-label caption>{{ product.description }}</q-item-label>
              <q-item-label caption class="text-primary text-weight-bold">{{ product.monthlyFee }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-step>

      <!-- Step 4: e-KYC (Document Upload) -->
      <q-step :name="4" title="e-KYC" icon="verified_user" :done="step > 4">
        <div class="text-subtitle1 q-mb-md">Upload dokumen identitas:</div>

        <q-card flat bordered class="q-mb-md">
          <q-card-section>
            <div class="row items-center q-gutter-md">
              <q-icon name="badge" size="40px" color="primary" />
              <div class="col">
                <div class="text-subtitle2">Foto KTP</div>
                <div class="text-caption text-grey-7" v-if="!form.ktpFile">Belum diupload</div>
                <div class="text-caption text-positive" v-else>✓ {{ form.ktpFile.name }}</div>
              </div>
              <q-btn :label="form.ktpFile ? 'Ganti' : 'Upload'" color="primary" outline @click="captureKTP" no-caps />
            </div>
          </q-card-section>
        </q-card>

        <q-card flat bordered class="q-mb-md">
          <q-card-section>
            <div class="row items-center q-gutter-md">
              <q-icon name="face" size="40px" color="primary" />
              <div class="col">
                <div class="text-subtitle2">Selfie dengan KTP</div>
                <div class="text-caption text-grey-7" v-if="!form.selfieFile">Belum diupload</div>
                <div class="text-caption text-positive" v-else>✓ {{ form.selfieFile.name }}</div>
              </div>
              <q-btn :label="form.selfieFile ? 'Ganti' : 'Capture'" color="primary" outline @click="captureSelfie" no-caps />
            </div>
          </q-card-section>
        </q-card>

        <q-card flat bordered>
          <q-card-section>
            <div class="row items-center q-gutter-md">
              <q-icon name="fingerprint" size="40px" color="primary" />
              <div class="col">
                <div class="text-subtitle2">Liveness Check</div>
                <div class="text-caption text-grey-7">Verifikasi wajah dengan kedipan & senyum</div>
              </div>
              <q-btn label="Mulai" color="primary" outline @click="startLiveness" no-caps />
            </div>
          </q-card-section>
        </q-card>
      </q-step>

      <!-- Step 5: Review & Submit -->
      <q-step :name="5" title="Review & Submit" icon="check_circle">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-h6 q-mb-md">Review Data Anda</div>
            <q-list separator>
              <q-item><q-item-section><q-item-label>Nama</q-item-label></q-item-section><q-item-section side>{{ form.fullName }}</q-item-section></q-item>
              <q-item><q-item-section><q-item-label>NIK</q-item-label></q-item-section><q-item-section side>{{ form.nik }}</q-item-section></q-item>
              <q-item><q-item-section><q-item-label>Email</q-item-label></q-item-section><q-item-section side>{{ form.email }}</q-item-section></q-item>
              <q-item><q-item-section><q-item-label>No. HP</q-item-label></q-item-section><q-item-section side>{{ form.mobilePhone }}</q-item-section></q-item>
              <q-item><q-item-section><q-item-label>Produk</q-item-label></q-item-section><q-item-section side>{{ getProductName(form.productCode) }}</q-item-section></q-item>
            </q-list>

            <q-checkbox v-model="agreedTerms" label="Saya menyetujui Syarat & Ketentuan Bank XYZ" class="q-mt-md" />

            <div class="q-mt-md">
              <q-btn label="Submit Onboarding" color="primary" :disable="!agreedTerms" :loading="submitting" @click="submit" no-caps class="full-width" />
            </div>
          </q-card-section>
        </q-card>
      </q-step>

      <template #navigation>
        <q-stepper-navigation>
          <q-btn v-if="step > 1" flat label="Sebelumnya" @click="step--" no-caps />
          <q-btn v-if="step < 5" color="primary" label="Selanjutnya" @click="step++" no-caps class="q-ml-sm" />
        </q-stepper-navigation>
      </template>
    </q-stepper>
  </q-page>
</template>

<script setup lang="import">
import { ref, reactive } from 'vue';
import { useQuasar } from 'quasar';
import { useRouter } from 'vue-router';

const $q = useQuasar();
const router = useRouter();

const step = ref(1);
const submitting = ref(false);
const agreedTerms = ref(false);

const form = reactive({
  fullName: '',
  nik: '',
  placeOfBirth: '',
  dateOfBirth: '',
  gender: '',
  email: '',
  mobilePhone: '',
  address: '',
  rt: '',
  rw: '',
  postalCode: '',
  province: '',
  city: '',
  productCode: 'TABUNGAN_REGULER',
  ktpFile: null,
  selfieFile: null,
});

const genderOptions = [
  { label: 'Laki-laki', value: 'MALE' },
  { label: 'Perempuan', value: 'FEMALE' },
];

const provinceOptions = ['DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Banten'];
const cityOptions = ['Jakarta', 'Bandung', 'Semarang', 'Surabaya', 'Tangerang'];

const products = [
  { code: 'TABUNGAN_REGULER', name: 'Tabungan Reguler', description: 'Tabungan dengan setoran minimum Rp 100.000', monthlyFee: 'Biaya admin: Rp 5.000/bulan' },
  { code: 'TABUNGAN_GOLD', name: 'Tabungan Gold', description: 'Tabungan dengan benefit lebih banyak', monthlyFee: 'Biaya admin: Rp 15.000/bulan' },
  { code: 'TABUNGAN_HAJI', name: 'Tabungan Haji', description: 'Untuk persiapan ibadah haji', monthlyFee: 'Biaya admin: Gratis' },
];

const required = (val) => !!val || 'Wajib diisi';

function captureKTP() {
  // In real app, use Capacitor Camera plugin
  $q.dialog({
    title: 'Upload KTP',
    message: 'Pilih metode upload',
    ok: { label: 'Kamera', color: 'primary' },
    cancel: { label: 'Galeri', color: 'primary', flat: true },
  }).onOk(() => {
    form.ktpFile = { name: `ktp_${Date.now()}.jpg`, size: 1024000 };
    $q.notify({ message: 'KTP berhasil diupload', color: 'positive' });
  }).onCancel(() => {
    form.ktpFile = { name: `ktp_${Date.now()}.jpg`, size: 1024000 };
    $q.notify({ message: 'KTP berhasil diupload dari galeri', color: 'positive' });
  });
}

function captureSelfie() {
  form.selfieFile = { name: `selfie_${Date.now()}.jpg`, size: 2048000 };
  $q.notify({ message: 'Selfie berhasil di-capture', color: 'positive' });
}

function startLiveness() {
  $q.dialog({
    title: 'Liveness Check',
    message: 'Ikuti instruksi: kedipkan mata 3x, lalu senyum',
    ok: { label: 'Selesai', color: 'positive' },
    cancel: { label: 'Batal', color: 'negative', flat: true },
  }).onOk(() => {
    $q.notify({ message: 'Liveness check berhasil (mock)', color: 'positive' });
  });
}

function getProductName(code) {
  return products.find(p => p.code === code)?.name || code;
}

async function submit() {
  submitting.value = true;
  try {
    await new Promise(r => setTimeout(r, 2000));
    $q.notify({
      message: 'Onboarding berhasil! Anda akan menerima notifikasi setelah KYC disetujui.',
      color: 'positive',
      icon: 'check_circle',
      timeout: 5000,
    });
    router.push('/dashboard');
  } finally {
    submitting.value = false;
  }
}
</script>
