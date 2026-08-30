# 🏆 AUREA — The Gold Standard of Data

> **Complete AI-Powered Master Data Management (MDM) Platform**
> Multi-app monorepo · Vanilla HTML5 + Modern JS · **Single-file SPA demo + Vue/Nuxt frontends + FastAPI ML backend**

[![Made in Indonesia](https://img.shields.io/badge/Made%20in-Indonesia%20🇮🇩-red)](https://github.com/radianadhic/aurea)
[![PWA Ready](https://img.shields.io/badge/PWA-Ready-success)](https://web.dev/progressive-web-apps/)
[![Offline First](https://img.shields.io/badge/Offline-First-blue)](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)](https://github.com/radianadhic/aurea)

---

## ✨ What is AUREA?

A complete enterprise-grade **Master Data Management** platform demonstrating:

- 🧠 **4 AI engines** for customer intelligence
- 📊 **Real-time analytics** with WebSocket live updates
- 💾 **Offline-first** PWA with IndexedDB caching
- 📄 **Multi-page PDF reports** with table of contents
- 🔔 **Push notifications** (Web Notifications API)
- 📱 **Mobile app** (React Native)
- 🎨 **Full design system** (brand assets + wireframes)

All running in a single 209 KB HTML file **or** as a full multi-app stack.

---

## 🚀 Quick Start

### 🌐 Try the Live Demo (no install)

**[👉 Open the standalone SPA →](https://radianadhic.github.io/aurea/)**

A single 209 KB HTML file with:
- Splash screen, login, 11 pages
- All 4 AI engine integrations
- WebSocket + IndexedDB + PWA
- PDF export, charts, notifications
- **Works fully offline** after first load

### 💻 Run the Full Stack Locally

```bash
# 1. Clone the repo
git clone https://github.com/radianadhic/aurea.git
cd aurea

# 2. Start the ML service (FastAPI)
cd ml-service
pip install fastapi uvicorn numpy pandas scikit-learn
uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# 3. Start the standalone SPA
cd ..
python3 -m http.server 5050

# 4. (Optional) Start the multi-file SPA
cd spa
python3 -m http.server 5000

# 5. (Optional) Start the frontends
cd ../frontend/admin-dashboard && npm run dev &     # :3000
cd ../customer360 && npm run dev &                  # :3001
cd ../steward-ui && npm run dev &                   # :3002

# 6. (Optional) Open the mockup showcase
cd ../../mockup
python3 -m http.server 4000
```

### 📱 Try the Mobile App

```bash
cd aurea-mobile
npm install
npx react-native run-android    # or run-ios
```

---

## 📁 Repository Structure

```
aurea/
├── index.html                    ⭐ Standalone SPA (209 KB) — start here!
├── README.md                     📖 You are here
├── LICENSE                       📜 MIT
│
├── spa/                          📦 Multi-file vanilla SPA (15 files)
│   ├── index.html
│   ├── css/aurea.css
│   └── js/{api,state,router,...}.js
│
├── frontend/                     🎨 Production frontends (Vue + Nuxt)
│   ├── admin-dashboard/          → AUREA Console (Vite, :3000)
│   ├── customer360/              → AUREA 360 (Nuxt, :3001)
│   └── steward-ui/               → AUREA Steward (Nuxt, :3002)
│
├── ml-service/                   🧠 FastAPI ML backend (:8000)
│   ├── api/main.py               32+ endpoints
│   ├── modules/                  4 AI engines
│   └── data/                     Sample datasets
│
├── mockup/                       🎭 Marketing showcase (:4000)
│   └── index.html
│
├── aurea-mobile/                 📱 React Native app
│   ├── src/screens/
│   └── package.json
│
├── aurea-brand/                  🎨 Brand identity (logos, colors, fonts)
├── wireframes/                   📐 UI/UX wireframes
├── aurea-techdoc-assets/         📑 Technical doc images
├── aurea-pptx-assets/            📊 Presentation assets
├── aurea-pptx-previews/          🖼️  PPT previews
├── aurea-docx-assets/            📄 Document assets
│
├── versions/                     🕐 Historical versions
│   ├── v1-baseline.html          SPA v1 (no charts, no PDF)
│   └── v2-charts-pdf.html        SPA v2 (with charts + PDF)
│
├── backend/                      🔧 Backend services (Node.js, Python)
├── infrastructure/               🏗️  IaC (Docker, K8s, Terraform)
├── database/                     🗄️  SQL schemas, migrations
├── keycloak/                     🔐 Auth config
├── templates/                    📋 Project templates
├── scripts/                      🛠️  Utility scripts
├── lampiran/                     📎 Attachments
└── uploads/                      📤 User uploads
```

---

## 🎯 Features Overview

### 🧠 4 AI Engines (in `ml-service/`)

| Engine | Endpoint | Purpose |
|---|---|---|
| 🧠 **Auto-Insights** | `/insights/*` | Detect anomalies with natural-language narratives |
| 🎯 **Smart Segmentation** | `/segments/*` | RFM-based segments + CLV prediction |
| 🚨 **Churn Watch** | `/churn/*` | Real-time churn risk scoring + interventions |
| 🛡️ **Fraud Detection** | `/fraud/*` | Multi-signal transaction scoring |

### 💎 11 Pages (in `index.html` and `spa/`)

1. **📊 Dashboard** — Top metrics, AI engine cards, live activity feed, 5+ charts
2. **📈 Monitoring** — (alias for Health)
3. **🧠 Auto-Insights** — Severity/category filters, modal detail
4. **🎯 Smart Segmentation** — 10 RFM segments, CLV, recommendations
5. **🚨 Churn Watch** — Risk levels, intervention creation
6. **🛡️ Fraud Detection** — Multi-signal breakdown, approve/block
7. **👥 Customers** — Searchable/filterable/sortable table
8. **⚙️ Configuration** — (alias for Settings)
9. **📑 Reports** — Multi-page PDF generator with TOC
10. **💚 System Health** — Module status, IndexedDB stats
11. **🔧 Settings** — Theme, connection, offline storage, PWA install

### 🆕 Modern Web Features (in `index.html`)

| Feature | Description |
|---|---|
| 📡 **WebSocket Live Updates** | Real `WebSocket` + simulated fallback (8-15s events) |
| 💾 **IndexedDB Offline Cache** | 2 stores (cache + mutations), 24h TTL, 3-tier fetch |
| 📱 **PWA Support** | Inline manifest + service worker, installable |
| 📊 **SVG Charts** | Line/bar/donut/sparkline — 13+ charts, **0 dependencies** |
| 📄 **Multi-Page PDF** | 3 templates, 9-page Full Report, TOC, audit trail |
| 🔔 **Push Notifications** | Web Notifications API + in-app toast + bell dropdown |
| 🌙 **Dark Mode** | Theme toggle, persistent via localStorage |
| 📐 **Responsive** | Breakpoints 968/480, mobile sidebar drawer |

---

## 🎨 Design System

**Colors:**
- 🟦 Navy `#0A1929` (primary)
- 🟨 Gold `#D4AF37` (accent)
- 🟩 Success `#10B981` · 🟥 Danger `#EF4444` · 🟧 Warning `#F59E0B` · 🟦 Info `#3B82F6`

**Typography:**
- `Georgia, serif` — Display & headings
- `Inter, sans-serif` — UI
- `JetBrains Mono, monospace` — Data & code

Full brand guidelines in `aurea-brand/`.

---

## 📊 Tech Stack

| Layer | Technology |
|---|---|
| **Single-file SPA** | Vanilla HTML5 + ES2022 JavaScript, no build |
| **Multi-file SPA** | Vanilla HTML5 + ES modules |
| **Admin Dashboard** | Vue 3 + Vite + Element Plus |
| **Customer 360** | Nuxt 3 + Vue 3 |
| **Steward UI** | Nuxt 3 + Vue 3 |
| **Mobile App** | React Native |
| **Backend** | FastAPI (Python 3.11+) + scikit-learn |
| **Auth** | Keycloak (optional) |
| **Database** | PostgreSQL (schemas in `database/`) |
| **Infrastructure** | Docker + Kubernetes (in `infrastructure/`) |
| **CI/CD** | (configure in `.github/workflows/`) |

---

## 🌐 All Services & Ports

| Service | Port | URL | Status |
|---|---|---|---|
| **Standalone SPA** ⭐ | 5050 | http://localhost:5050 | `index.html` |
| Multi-file SPA | 5000 | http://localhost:5000 | `spa/` |
| AUREA Console (Vue) | 3000 | http://localhost:3000 | `frontend/admin-dashboard/` |
| AUREA 360 (Nuxt) | 3001 | http://localhost:3001 | `frontend/customer360/` |
| AUREA Steward (Nuxt) | 3002 | http://localhost:3002 | `frontend/steward-ui/` |
| Mockup Showcase | 4000 | http://localhost:4000 | `mockup/` |
| ML Service (FastAPI) | 8000 | http://localhost:8000 | `ml-service/` |
| API Docs (Swagger) | 8000 | http://localhost:8000/docs | — |

---

## 📊 Code Statistics

```
Standalone SPA (index.html):
├── Size: 209 KB
├── Lines: 3,383
├── Inline CSS: ~700 lines
├── Inline JS: ~1,800 lines
├── Classes: 12 (State, IDB, API, WS, Chart, Notif, PDF, MultiPDF, Router, ...)
├── Pages: 11
├── Charts: 13+
├── Notifications: 20 sample
└── External dependencies: 0

Multi-file SPA (spa/):
├── Files: 15
├── Total: 156 KB
├── JS: 2,096 lines (12 modules)
├── CSS: 953 lines
└── Pages: 8

ML Service (ml-service/):
├── Python: ~3,000 lines
├── Endpoints: 32+
├── AI engines: 4
└── Sample data: 200 customers

Frontends (frontend/):
├── Admin (Vue): ~5,000 lines
├── Customer 360 (Nuxt): ~3,000 lines
└── Steward (Nuxt): ~3,000 lines
```

---

## 🔌 Optional: ML Service Backend

The SPA works **fully offline** with cached data. To enable live AI features, run the FastAPI ML service:

```bash
cd ml-service
pip install fastapi uvicorn numpy pandas scikit-learn
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The SPA will auto-detect the service at `http://localhost:8000` and switch from simulated to live data.

Visit API docs: **http://localhost:8000/docs**

---

## 🌐 Browser Support

| Browser | Support |
|---|---|
| Chrome 90+ | ✅ Full (PWA install, WebSocket, Notifications) |
| Edge 90+ | ✅ Full |
| Firefox 88+ | ✅ Full (PWA install behind flag) |
| Safari 14+ | ✅ Full (iOS PWA via Add to Home Screen) |
| Opera 76+ | ✅ Full |

**Required APIs:** IndexedDB · Service Worker · WebSocket · Notifications API · Web Crypto

---

## 🧪 Testing

```bash
# Validate standalone SPA JS syntax
node --check <(sed -n '/<script>/,/<\/script>/p' index.html | sed '1d;$d')

# Test offline mode
# 1. Open the file
# 2. Stop any backend service
# 3. Refresh — cached data should still display

# Test PWA install
# 1. Open in Chrome
# 2. Look for install icon in address bar
# 3. Click "Install" — app appears as standalone window

# Test multi-page PDF export
# 1. Open the standalone SPA
# 2. Click Reports in sidebar
# 3. Click "Generate Report" → choose template → new window opens
# 4. Use browser's Print → Save as PDF
```

---

## 📸 Screenshots

| Page | Description |
|---|---|
| Dashboard | 4 top stats + 4 AI cards + 5 charts + live activity feed |
| Insights | Severity/category filters + bar charts + detail modal |
| Segmentation | 10 RFM segment cards + CLV chart + customer distribution donut |
| Churn | Risk levels + top-10 chart + 6-month trend + intervention modal |
| Fraud | Decision filters + signal breakdown + approve/block |
| Reports | Template selector + section picker + live preview + PDF export |

See `wireframes/` and `aurea-pptx-previews/` for full design gallery.

---

## 🤝 Contributing

This is a **demo / portfolio piece**. Feel free to:

- ⭐ Star the repo
- 🐛 Open issues for bugs
- 💡 Suggest features
- 🍴 Fork and customize
- 📝 Submit PRs for improvements

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Credits

Built with ❤️ by [radianadhic](https://github.com/radianadhic) as a showcase of what's possible with **modern web technologies** in 2026.

**Stack:** HTML5 · CSS3 · Vanilla JavaScript (ES2022) · Vue 3 · Nuxt 3 · React Native · FastAPI · IndexedDB · WebSocket · Service Worker · Web Crypto API

**No proprietary frameworks. No build step required for the core demo.**

---

<p align="center">
  <strong>🏆 The Gold Standard of Data 🏆</strong>
</p>
