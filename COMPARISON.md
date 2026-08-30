# AUREA vs Aplikasi MDM Indonesia — Analisis Komparatif

> Perbandingan fitur, modul, menu, dan form antara **AUREA** dengan aplikasi **Master Data Management** yang beredar di pasar Indonesia.

---

## 📊 Executive Summary

**AUREA** adalah aplikasi MDM **demo / portfolio** dengan 209KB single-file SPA, dirancang sebagai showcase kemampuan platform. **Bukan produk komersial** yang siap dipakai enterprise Indonesia. Namun, AUREA menunjukkan visi lengkap dari sebuah platform MDM modern dengan 4 AI engine yang umumnya hanya ada di produk enterprise tier-1.

| Aspek | AUREA | MDM Enterprise (Informatica/Talend/Pimcore) | MDM Lokal Indonesia |
|---|---|---|---|
| **Harga** | Gratis (open source) | $50K–$500K+/tahun | Rp 100jt–Rp 1M+ |
| **Target** | Demo / portfolio | Enterprise (bank, telco) | SME/mid-market |
| **Deployment** | Single HTML, no install | Cloud + on-prem | Cloud + on-prem |
| **AI/ML** | 4 engines built-in | Plugin-based (tambah mahal) | Terbatas |
| **Bahasa** | English | English | English + Indonesia |
| **Compliance** | Demo only | GDPR, HIPAA, OJK, BI | OJK, BI, ISO 27001 |
| **Support** | Community | 24/7 enterprise | 8×5 lokal |

---

## 🏗️ Perbandingan Modul Inti

Modul inti MDM (berdasarkan **Informatica MDM**, **Talend MDM**, **Pimcore**, **IBM InfoSphere**):

| Modul | AUREA | Informatica | Talend | Pimcore | MDM Lokal |
|---|:---:|:---:|:---:|:---:|:---:|
| **Customer Master** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Product Master** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Supplier/Vendor Master** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Employee Master** | ❌ | ✅ | ❌ | ✅ | ⚠️ |
| **Location/Asset Master** | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Financial Master** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Reference Data** | ❌ | ✅ | ✅ | ✅ | ⚠️ |

### 📌 Positioning AUREA

**AUREA fokus 100% di Customer MDM** — bukan multi-domain enterprise MDM. Ini sengaja, karena:
- Customer data adalah domain paling kompleks (nama, alamat, perilaku)
- AI engines (Churn, Fraud, Segmentation) fokus pada customer intelligence
- Cocok untuk B2C company: bank retail, telco, e-commerce, fintech

> **Rekomendasi positioning:** "AI-Powered Customer Intelligence Platform" — bukan "MDM Platform" generic.

---

## 🧠 Perbandingan AI / Analytics Engines

Inilah kekuatan utama AUREA yang **jarang ada** di MDM Indonesia:

| AI Engine | AUREA | MDM Enterprise | MDM Lokal | CDP (Segment, mParticle) |
|---|:---:|:---:|:---:|:---:|
| **Auto-Insights (anomaly detection)** | ✅ Built-in | ⚠️ Add-on ($$$) | ❌ | ⚠️ Limited |
| **Customer Segmentation (RFM)** | ✅ Built-in | ⚠️ Add-on | ❌ | ✅ Core |
| **Churn Prediction** | ✅ Built-in | ⚠️ Add-on ($$$) | ❌ | ⚠️ Limited |
| **Fraud Detection (multi-signal)** | ✅ Built-in | ⚠️ Separate product | ❌ | ❌ |
| **CLV Prediction** | ✅ Built-in | ⚠️ Add-on | ❌ | ✅ |
| **Real-time scoring** | ✅ WebSocket | ✅ (enterprise) | ❌ | ✅ |

### 💡 Insight
AUREA memiliki **4 AI engines** yang sudah integrated dalam 1 platform. Vendor MDM enterprise menjual ini sebagai modul terpisah dengan biaya **$50K–$200K per engine per tahun**.

---

## 📋 Perbandingan Menu & Halaman

### AUREA — 11 Halaman

```
┌─ Main
│   ├─ 📊 Dashboard
│   └─ 📈 Monitoring (alias)
│
├─ AI Intelligence
│   ├─ 🧠 Auto-Insights
│   ├─ 🎯 Smart Segmentation
│   ├─ 🚨 Churn Watch
│   └─ 🛡️ Fraud Detection
│
├─ Management
│   ├─ 👥 Customers
│   ├─ ⚙️ Configuration (alias)
│   └─ 📑 Reports
│
└─ Operations
    ├─ 💚 System Health
    └─ 🔧 Settings
```

### Informatica MDM — Typical Menu Structure

```
┌─ Home Dashboard
├─ Data Domains
│   ├─ Customer 360
│   ├─ Product
│   ├─ Supplier
│   ├─ Account
│   └─ Reference Data
├─ Data Quality
│   ├─ Data Profiling
│   ├─ Data Validation Rules
│   ├─ Cleansing & Standardization
│   └─ Match & Merge
├─ Data Governance
│   ├─ Stewardship Workflow
│   ├─ Approval Process
│   ├─ Data Lineage
│   └─ Audit Trail
├─ Data Integration
│   ├─ Source Connectors
│   ├─ ETL Pipelines
│   ├─ Real-time Sync
│   └─ Batch Jobs
├─ Data Security
│   ├─ Access Control
│   ├─ Data Masking
│   ├─ Encryption
│   └─ Privacy Rules
├─ Reports & Analytics
├─ Administration
│   ├─ User Management
│   ├─ Role & Permission
│   ├─ System Config
│   └─ Monitoring
└─ Help & Documentation
```

**Total: 40-50 menu items** (vs AUREA 11)

### Pimcore MDM — Typical Menu

```
┌─ Dashboard
├─ Data Objects
│   ├─ Classes
│   ├─ Field Collections
│   └─ Object bricks
├─ Data Quality
│   ├─ Quality Reports
│   └─ Validation
├─ Workflows
├─ Roles & Permissions
├─ Users
├─ Tags
├─ Classification Store
├─ Data Sources
├─ Import/Export
├─ API
└─ Settings
```

### MDM Lokal Indonesia (Contoh: Banking/Fintech)

```
┌─ Dashboard
├─ Master Data
│   ├─ Customer
│   ├─ Rekening
│   ├─ Produk
│   └─ Cabang
├─ Verifikasi Data
│   ├─ KTP/NIK Validation
│   ├─ NPWP Check
│   └─ Dukcapil Integration
├─ Reporting OJK/BI
├─ Audit & Compliance
├─ User Management
└─ Settings
```

### 📊 Coverage Analysis

| Area | AUREA | Enterprise MDM | Coverage % |
|---|---|---|---|
| **Customer domain** | 100% | 100% | ✅ Same |
| **Product/Supplier** | 0% | 100% | ❌ Missing |
| **Data Quality** | 30% | 100% | ⚠️ Partial |
| **Data Governance** | 20% | 100% | ⚠️ Partial |
| **Data Integration** | 0% | 100% | ❌ Missing |
| **AI/Analytics** | 100% | 60% | ✅ Ahead |
| **Reporting** | 80% | 100% | ⚠️ Good |
| **Mobile** | Yes (RN) | Yes | ✅ Same |
| **Offline/PWA** | Yes | No | ✅ Ahead |

**Kesimpulan:** AUREA lebih dalam di AI, tapi kurang luas di governance. Cocok untuk demo/pilot, belum untuk production enterprise.

---

## 📝 Perbandingan Form & Input

### AUREA — Customer Detail Modal

```
┌─────────────────────────────────────────────┐
│  CUST-007 - Budi Santoso                    │
├─────────────────────────────────────────────┤
│  Segment    │ RFM                            │
│  Champions  │ 555                            │
│                                             │
│  CLV (12m)  │ Churn Risk                     │
│  Rp 89.5M   │ LOW  15%                       │
├─────────────────────────────────────────────┤
│  💡 Next Best Action                        │
│  Upgrade to VIP tier · Cross-sell premium   │
└─────────────────────────────────────────────┘
```

**Form fields:** Segment, RFM, CLV, Churn Risk, Next Best Action (read-only — derived dari AI)

### Enterprise MDM — Customer Master Form (contoh)

```
┌─────────────────────────────────────────────────────┐
│  Customer: PT Maju Jaya                             │
├─────────────────────────────────────────────────────┤
│  IDENTITAS                                         │
│  ├─ Customer ID: [CUST-2024-0001]                   │
│  ├─ Customer Type: [Individual ▼]                   │
│  ├─ Title: [Mr/Mrs/PT/CV]                           │
│  ├─ Full Name: [____________________] *              │
│  ├─ Alias:    [____________________]                │
│  ├─ Birth Date: [____-__-__]  POB: [____________]   │
│  ├─ Gender: [M/F]  Marital: [Single/Married]        │
│  └─ Nationality: [Indonesian ▼]                     │
│                                                     │
│  IDENTITAS RESMI (KYC)                              │
│  ├─ KTP Number: [____________________] *            │
│  ├─ NPWP:       [____________________]              │
│  ├─ Passport:   [____________________]              │
│  └─ [✓] Verified Dukcapil  [✓] Verified BI          │
│                                                     │
│  KONTAK                                             │
│  ├─ Phone (HP):   [+62____________] *               │
│  ├─ Phone (Rumah):[______________]                  │
│  ├─ Email:        [____________________] *          │
│  └─ Preferred:    [☐ HP  ☐ Email  ☐ WA]            │
│                                                     │
│  ALAMAT (bisa multiple)                             │
│  ├─ [+] Add Address                                  │
│  ├─ Type: [KTP ▼]  Address: [_______________]       │
│  ├─ RT/RW: [__/__]  Kel: [___________]               │
│  ├─ Kec: [___________]  Kota: [___________]         │
│  └─ Provinsi: [___________]  Postal: [_____]         │
│                                                     │
│  KEUANGAN                                           │
│  ├─ Monthly Income: [Rp ____________]               │
│  ├─ Source of Funds: [Salary/Business/Other]        │
│  ├─ Risk Profile:   [Conservative/Moderate/Aggressive]│
│  └─ PEP Status:     [☐ Yes  ☐ No]                   │
│                                                     │
│  TAX & COMPLIANCE                                   │
│  ├─ NPWP Status: [Registered/Unregistered]          │
│  ├─ Tax Resident: [Indonesia / Other]               │
│  └─ [✓] FATCA Compliant  [✓] CRS Compliant          │
│                                                     │
│  RELATIONSHIPS                                       │
│  ├─ Account: [ACC-001, ACC-002, ...]                │
│  ├─ Family: [Spouse, Children]                       │
│  └─ Employer: [PT XYZ]                              │
│                                                     │
│  AUDIT TRAIL                                         │
│  ├─ Created: 2024-01-15 by admin@bank                │
│  ├─ Modified: 2024-08-20 by staff@bank              │
│  └─ Source: CIF System, CRM, Onboarding             │
│                                                     │
│  [Save]  [Save & Approve]  [Cancel]                  │
└─────────────────────────────────────────────────────┘
```

**Field count:** 50-100+ fields (vs AUREA ~5-10 derived fields)

### 📊 Form Analysis

| Tipe | AUREA | Enterprise MDM | Catatan |
|---|---|---|---|
| **Read-only detail** | ✅ | ✅ | AUREA lebih fokus |
| **Create form** | ❌ | ✅ | AUREA tidak ada create UI |
| **Edit form** | ❌ | ✅ | AUREA tidak ada edit UI |
| **Search/filter** | ✅ Simple | ✅ Advanced | AUREA basic |
| **Bulk import** | ❌ | ✅ | AUREA missing |
| **Bulk edit** | ❌ | ✅ | AUREA missing |
| **Workflow approval** | ❌ | ✅ | AUREA missing |
| **Audit trail per field** | ❌ | ✅ | AUREA missing |
| **Version history** | ❌ | ✅ | AUREA missing |

**Insight:** AUREA adalah **read-only analytics tool**, bukan CRUD application. Untuk production MDM, butuh tambah create/edit/bulk/workflow.

---

## 🆚 AUREA vs Produk Sejenis (Detail)

### 1. AUREA vs Informatica MDM

| Aspek | AUREA | Informatica |
|---|---|---|
| **Harga** | Gratis | $500K+/tahun |
| **Customer 360** | ✅ Basic | ✅ Advanced (golden record) |
| **Match & Merge** | ❌ | ✅ Probabilistic + AI |
| **Data Lineage** | ❌ | ✅ Full graph |
| **Workflow** | ❌ | ✅ Multi-step approval |
| **Stewardship** | ❌ | ✅ Role-based UI |
| **AI Engines** | ✅ 4 built-in | ⚠️ Add-on ($$) |
| **Multi-domain** | ❌ | ✅ Customer + Product + Supplier |
| **Deployment** | 1 file | Enterprise install |
| **Time to demo** | 5 menit | 3-6 bulan |

**AUREA advantage:** Speed to demo, AI included, price
**AUREA gap:** No stewardship, no multi-domain, no lineage

### 2. AUREA vs Talend Open Studio (free alternative)

| Aspek | AUREA | Talend Open Studio |
|---|---|---|
| **Harga** | Gratis | Gratis (open source) |
| **UI Type** | Web SPA | Desktop (Eclipse-based) |
| **AI Engines** | ✅ 4 built-in | ❌ (perlu coding) |
| **PWA/Offline** | ✅ | ❌ |
| **Mobile** | ✅ (RN) | ❌ |
| **Match & Merge** | ❌ | ✅ Visual tMatchGroup |
| **ETL Jobs** | ❌ | ✅ 1000+ components |
| **Visual Mapper** | ❌ | ✅ Drag & drop |
| **Learning curve** | Rendah | Tinggi |
| **Code required** | Tidak | Java/SQL |

**AUREA advantage:** Modern UI, no coding, AI, mobile
**Talend advantage:** Mature ETL, huge ecosystem, visual design

### 3. AUREA vs Pimcore (open source MDM)

| Aspek | AUREA | Pimcore |
|---|---|---|
| **Harga** | Gratis | Community Edition free |
| **Multi-domain** | ❌ (customer only) | ✅ Customer + Product + Supplier + Asset + Location |
| **PIM** | ❌ | ✅ Best-in-class (Product Info Mgmt) |
| **DAM** | ❌ | ✅ Digital Asset Management built-in |
| **CDP** | ❌ | ✅ Customer Data Platform |
| **E-commerce** | ❌ | ✅ Built-in |
| **Workflow** | ❌ | ✅ Visual workflow editor |
| **API** | Manual | ✅ REST + GraphQL |
| **Modern UI** | ✅ | ⚠️ Bootstrap-style |
| **AI** | ✅ | ❌ |

**Pimcore advantage:** Full MDM, multi-domain, mature
**AUREA advantage:** Modern, AI-first, easier to demo

### 4. AUREA vs Salesforce CDP / Segment

| Aspek | AUREA | Segment / Salesforce CDP |
|---|---|---|
| **Real-time** | ✅ WebSocket | ✅ |
| **Customer 360** | ✅ | ✅ |
| **Identity Resolution** | ❌ | ✅ Advanced |
| **Marketing activation** | ❌ | ✅ Email, SMS, push |
| **AI Predictive** | ✅ | ✅ (Einstein/AI) |
| **Data warehouses** | ❌ | ✅ Snowflake, BigQuery sync |
| **Integrations** | ❌ | ✅ 300+ |
| **Price** | Gratis | $120K+/tahun |
| **Setup time** | 5 menit | 1-3 bulan |

**AUREA = Customer analytics + AI demo**
**Segment/CDP = Marketing activation platform**

---

## 🇮🇩 Konteks Indonesia — Compliance & Regulasi

MDM di Indonesia harus comply dengan regulasi berikut. **AUREA belum cover** ini (demo only):

| Regulasi | Diterapkan Oleh | AUREA | Enterprise MDM |
|---|---|:---:|:---:|
| **OJK** (POJK 1/2013, 75/2016) | Bank, multifinance | ❌ | ✅ |
| **BI** (PADG 19/2017) | Perbankan | ❌ | ✅ |
| **UU PDP** (Pelindungan Data Pribadi) | Semua | ❌ | ✅ |
| **Dukcapil** (NIK validation) | Semua | ❌ | ✅ |
| **NPWP** (DJP validation) | Semua | ❌ | ✅ |
| **OJK SLIK** (credit checking) | Fintech | ❌ | ✅ |
| **Bank Indonesia FAST** | Payment | ❌ | ✅ |
| **ISO 27001** | Enterprise | ❌ | ✅ |
| **PCI-DSS** | Payment | ❌ | ✅ |
| **GDPR-equivalent (UU PDP)** | Semua | ❌ | ✅ |

### Kebutuhan Khusus Indonesia

| Fitur | AUREA | MDM Enterprise | MDM Lokal |
|---|:---:|:---:|:---:|
| **NIK/KTP validation (Dukcapil)** | ❌ | ✅ | ✅ |
| **NPWP validation (DJP)** | ❌ | ✅ | ✅ |
| **e-KYC (face match, liveness)** | ❌ | ⚠️ Add-on | ✅ |
| **BI FAST payment integration** | ❌ | ✅ | ✅ |
| **OJK reporting format** | ❌ | ✅ | ✅ |
| **Bahasa Indonesia full** | ⚠️ Partial | ⚠️ | ✅ |
| **Rupiah formatting (Rp 1.000.000)** | ✅ | ✅ | ✅ |
| **Indonesian address structure (RT/RW, Kel, Kec, Kab, Prov)** | ❌ | ✅ | ✅ |
| **Local holiday calendar** | ❌ | ✅ | ✅ |
| **Indonesian name parsing (Budi Santoso, S.T., M.M.)** | ❌ | ✅ | ✅ |

---

## 🏆 Keunggulan Unik AUREA

Yang **tidak bisa ditiru** MDM manapun di Indonesia:

| Fitur | Deskripsi |
|---|---|
| **Single 209KB file** | Tidak ada install, tidak ada build, tidak ada framework |
| **100% offline-capable** | PWA + IndexedDB 24h cache + mutation queue |
| **Zero dependencies** | Pure HTML/CSS/JS — tidak ada npm, tidak ada webpack |
| **Install sebagai PWA** | Di Android/iOS/Desktop via browser |
| **Live demo di GitHub Pages** | radianadhic.github.io/aurea — bisa langsung dipakai |
| **Open source** | Bisa dipelajari, dimodifikasi, di-fork |
| **Bahasa Indonesia untuk summary** | User-facing text bilingual |
| **WebSocket + simulation fallback** | Live update tetap jalan tanpa backend |
| **Multi-page PDF dengan TOC** | Report enterprise-grade, print-ready |
| **20 sample notifications** | Demo out-of-the-box |

---

## ⚠️ Yang Belum Ada di AUREA (untuk jadi production MDM)

Kalau mau serius masuk pasar enterprise Indonesia, AUREA butuh:

### Must-have
- [ ] Create/Edit/Delete form untuk customer (CRUD lengkap)
- [ ] Stewardship workflow (approval process)
- [ ] Data quality rules (validation engine)
- [ ] Match & merge algorithm (fuzzy matching)
- [ ] NIK validation via Dukcapil API
- [ ] NPWP validation via DJP API
- [ ] Audit trail per field
- [ ] Multi-tenancy (multi-customer deployment)
- [ ] Role-based access control (RBAC)
- [ ] Bahasa Indonesia 100%

### Nice-to-have
- [ ] Product master (multi-domain)
- [ ] Supplier master
- [ ] GraphQL API
- [ ] ETL connector ke bank core system
- [ ] BI dashboard embedded (Tableau/Power BI)
- [ ] Mobile app production-ready (Play Store / App Store)
- [ ] SSO via Keycloak/SAML
- [ ] ISO 27001 documentation

### Phase 2 (jika mau jadi SaaS)
- [ ] Subscription billing (Stripe/Xendit)
- [ ] Self-service onboarding
- [ ] Multi-tenant database
- [ ] Per-customer AI model training
- [ ] White-label theming
- [ ] Marketplace integrations

---

## 🎯 Rekomendasi Strategi Positioning

### Opsi A: AI-Powered Customer Analytics (B2C-focused)
- **Target:** Bank retail, e-commerce, fintech, telco
- **Harga:** Rp 50-200 juta/tahun (jauh di bawah Informatica)
- **Value prop:** "Customer intelligence 4 AI engines dalam 1 platform, 1/10 harga Informatica"
- **Waktu ke market:** 3-6 bulan

### Opsi B: Demo & Training Tool
- **Target:** Consultant, system integrator, training provider
- **Harga:** Free / freemium
- **Value prop:** "Demo MDM dengan AI untuk sales pitch & training, tanpa install"
- **Waktu ke market:** 1 bulan (sudah jadi)

### Opsi C: Open Source MDM Indonesia
- **Target:** Komunitas developer, contributor
- **Harga:** Free + donasi + consulting
- **Value prop:** "Satu-satunya MDM Indonesia open source, modern, AI-first"
- **Waktu ke market:** 2-3 bulan (perlu governance & docs)

### Opsi D: POC/MVP untuk Bank/Fintech
- **Target:** Enterprise Indonesia yang mau evaluate MDM
- **Harga:** Rp 200-500 juta untuk 3 bulan POC
- **Value prop:** "POC MDM dengan AI, customize sesuai requirement, integrate ke core system"
- **Waktu ke market:** 2 minggu untuk demo, 3 bulan untuk POC

---

## 📊 Kesimpulan Akhir

### AUREA dalam 1 kalimat:
> **"Showcase modernisasi MDM Indonesia — 4 AI engines dalam 209KB single file, gratis, open source, tapi belum lengkap untuk production enterprise."**

### Market position:
```
High Cost │  ┌─────────────────┐
$500K+    │  │  Informatica    │  ← Target: bank besar, telco
          │  │  IBM MDM        │
          │  │  SAP MDG        │
          │  └─────────────────┘
          │  
          │  ┌─────────────────┐
$100K+    │  │  Talend         │  ← Target: enterprise
          │  │  Reltio         │
          │  │  Profisee       │
          │  └─────────────────┘
          │  
          │  ┌─────────────────┐
          │  │  AUREA   ⭐     │  ← Posisi ideal:
$0-50K    │  │  Pimcore        │     - Affordable
          │  │  MDM Lokal      │     - AI-first
          │  │  Talend OS      │     - Indonesian-ready
          │  └─────────────────┘     - Open source
          └────────────────────────────
            Less Features    More Features
```

### Rekomendasi:
1. **Jual sebagai "AI Customer Intelligence"** — bukan "MDM Platform"
2. **Bandrol dengan harga** yang undercut Talend/Informatica 5-10x
3. **Target bank BUKU 1-2, multifinance, fintech** yang butuh analytics tapi budget terbatas
4. **Open source sebagai marketing** — biar developer Indonesia kontribusi
5. **Tambah Dukcapil/NPWP integration** dulu sebelum masuk pasar regulated

---

## 📎 Referensi

- **Informatica MDM** — [informatica.com](https://www.informatica.com)
- **Talend Open Studio** — [talend.com](https://www.talend.com)
- **Pimcore Community** — [pimcore.com](https://pimcore.com)
- **IBM InfoSphere MDM** — [ibm.com](https://www.ibm.com)
- **Reltio Cloud** — [reltio.com](https://www.reltio.com)
- **Profisee** — [profisee.com](https://www.profisee.com)
- **OJK POJK 1/2013** — [ojk.go.id](https://www.ojk.go.id)
- **UU PDP No. 27/2022** — Perlindungan Data Pribadi

---

*Document generated 2026-08-30 · AUREA Platform · radianadhic/aurea*
