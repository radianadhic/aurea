<template>
  <div class="aurea-360">
    <!-- AUREA SPLASH SCREEN -->
    <Transition name="splash">
      <div v-if="showSplash" class="aurea-splash-overlay">
        <div class="aurea-splash-bg">
          <div v-for="i in 6" :key="i" class="aurea-particle"
               :style="`left: ${i*15}%; --drift: ${(i%2===0?30:-30)}px; animation-delay: ${i*0.4}s;`"></div>
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
          <p class="aurea-splash-tagline">CUSTOMER 360</p>
          <div class="aurea-splash-loader"></div>
        </div>
      </div>
    </Transition>

    <header class="aurea-header">
      <div class="aurea-header-content">
        <div class="aurea-brand">
          <img src="/logo-mark.svg" alt="AUREA" class="aurea-brand-logo" />
          <div>
            <h1 class="aurea-brand-title">AUREA 360</h1>
            <p class="aurea-brand-subtitle">Customer Intelligence</p>
          </div>
        </div>
        <nav class="aurea-nav">
          <NuxtLink to="/" exact-active-class="active">Dashboard</NuxtLink>
          <NuxtLink to="/customers" active-class="active">Customers</NuxtLink>
          <NuxtLink to="/analytics" active-class="active">Analytics</NuxtLink>
          <NuxtLink to="/segments" active-class="active">Segments</NuxtLink>
        </nav>
        <div class="aurea-user-area">
          <div class="aurea-status-dot"></div>
          <span class="aurea-user-name">Budi Santoso</span>
          <div class="aurea-avatar">BS</div>
        </div>
      </div>
    </header>

    <main class="aurea-main">
      <!-- KPI Cards (MD3G-themed) -->
      <section class="aurea-kpi-grid">
        <div class="aurea-kpi-card aurea-kpi-golden-customer">
          <div class="aurea-kpi-icon">👥</div>
          <div class="aurea-kpi-body">
            <p class="aurea-kpi-label">Total Customers</p>
            <h2 class="aurea-kpi-value">{{ formatNumber(kpis.totalCustomers) }}</h2>
            <span class="aurea-kpi-trend trend-up">↑ 8.2%</span>
          </div>
          <div class="aurea-kpi-accent"></div>
        </div>

        <div class="aurea-kpi-card aurea-kpi-golden-account">
          <div class="aurea-kpi-icon">✅</div>
          <div class="aurea-kpi-body">
            <p class="aurea-kpi-label">Active (30d)</p>
            <h2 class="aurea-kpi-value">{{ formatNumber(kpis.active30d) }}</h2>
            <span class="aurea-kpi-trend trend-up">↑ 3.1%</span>
          </div>
          <div class="aurea-kpi-accent"></div>
        </div>

        <div class="aurea-kpi-card aurea-kpi-golden-product">
          <div class="aurea-kpi-icon">🆕</div>
          <div class="aurea-kpi-body">
            <p class="aurea-kpi-label">New This Month</p>
            <h2 class="aurea-kpi-value">{{ formatNumber(kpis.newThisMonth) }}</h2>
            <span class="aurea-kpi-trend trend-up">↑ 12.4%</span>
          </div>
          <div class="aurea-kpi-accent"></div>
        </div>

        <div class="aurea-kpi-card">
          <div class="aurea-kpi-icon">⚠️</div>
          <div class="aurea-kpi-body">
            <p class="aurea-kpi-label">Churn Risk</p>
            <h2 class="aurea-kpi-value">{{ formatNumber(kpis.churnRisk) }}</h2>
            <span class="aurea-kpi-trend trend-down">↓ 2.1%</span>
          </div>
          <div class="aurea-kpi-accent"></div>
        </div>

        <div class="aurea-kpi-card">
          <div class="aurea-kpi-icon">💎</div>
          <div class="aurea-kpi-body">
            <p class="aurea-kpi-label">Avg CLV</p>
            <h2 class="aurea-kpi-value">{{ formatCurrency(kpis.avgClv) }}</h2>
            <span class="aurea-kpi-trend trend-up">↑ 5.6%</span>
          </div>
          <div class="aurea-kpi-accent"></div>
        </div>

        <div class="aurea-kpi-card">
          <div class="aurea-kpi-icon">⭐</div>
          <div class="aurea-kpi-body">
            <p class="aurea-kpi-label">NPS Score</p>
            <h2 class="aurea-kpi-value">{{ kpis.nps }}<span class="aurea-kpi-unit">/100</span></h2>
            <span class="aurea-kpi-trend trend-up">↑ 1.2%</span>
          </div>
          <div class="aurea-kpi-accent"></div>
        </div>
      </section>

      <!-- Main Charts -->
      <section class="aurea-charts-grid">
        <div class="aurea-card aurea-chart-large">
          <h2>Customer Growth</h2>
          <LineChart
            :categories="growthData.categories"
            :series="growthData.series"
            :height="320"
          />
        </div>

        <div class="aurea-card">
          <h2>Segment Distribution</h2>
          <PieChart
            :data="segmentData"
            :height="320"
            :donut="true"
          />
        </div>
      </section>

      <section class="aurea-charts-grid">
        <div class="aurea-card">
          <h2>Risk Distribution</h2>
          <BarChart
            :categories="riskData.categories"
            :series="riskData.series"
            :height="280"
          />
        </div>

        <div class="aurea-card">
          <h2>Top Performing Segments</h2>
          <table class="aurea-leaderboard">
            <thead>
              <tr>
                <th>Segment</th>
                <th>Customers</th>
                <th>CLV</th>
                <th>Trend</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="seg in topSegments" :key="seg.name">
                <td><strong>{{ seg.name }}</strong></td>
                <td>{{ formatNumber(seg.count) }}</td>
                <td>{{ formatCurrency(seg.clv) }}</td>
                <td>
                  <span :class="seg.trend > 0 ? 'aurea-trend-up' : 'aurea-trend-down'">
                    {{ seg.trend > 0 ? '↑' : '↓' }} {{ Math.abs(seg.trend) }}%
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- AUREA ML Insights -->
      <section class="aurea-insights-section">
        <h2 class="aurea-section-title">🧠 AUREA ML Insights</h2>
        <div class="aurea-insights-grid">
          <div class="aurea-insight-card aurea-insight-warning">
            <div class="aurea-insight-icon">⚠️</div>
            <div class="aurea-insight-body">
              <h3>High Churn Risk Segment</h3>
              <p>156 customers in "Young Professional" segment predicted to churn in 30 days. Recommended action: targeted retention campaign with product bundling offer.</p>
              <button class="aurea-action-btn">View Customers →</button>
            </div>
          </div>
          <div class="aurea-insight-card aurea-insight-info">
            <div class="aurea-insight-icon">💎</div>
            <div class="aurea-insight-body">
              <h3>High CLV Opportunity</h3>
              <p>23 customers in "Mass Affluent" segment have high predicted CLV (avg Rp 250M). Cross-sell wealth management products.</p>
              <button class="aurea-action-btn">View Opportunities →</button>
            </div>
          </div>
          <div class="aurea-insight-card aurea-insight-success">
            <div class="aurea-insight-icon">📈</div>
            <div class="aurea-insight-body">
              <h3>Anomaly Detected</h3>
              <p>5 customers showed unusual transaction patterns in last 7 days. Review recommended for AML compliance.</p>
              <button class="aurea-action-btn">Review →</button>
            </div>
          </div>
        </div>
      </section>

      <!-- AUREA Footer -->
      <footer class="aurea-footer">
        <div class="aurea-footer-brand">
          <img src="/logo-mark.svg" alt="AUREA" class="aurea-footer-logo" />
          <div>
            <p class="aurea-footer-title">AUREA 360</p>
            <p class="aurea-footer-tagline">The Gold Standard of Data</p>
          </div>
        </div>
        <p class="aurea-footer-version">v1.0.0 · © 2026 Bank XYZ</p>
      </footer>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';

definePageMeta({ layout: false });

const showSplash = ref(true);

const kpis = reactive({
  totalCustomers: 1_245_872,
  active30d: 892_341,
  newThisMonth: 18_294,
  churnRisk: 12_456,
  avgClv: 8_500_000,
  nps: 67,
});

const growthData = reactive({
  categories: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
  series: [
    { name: 'New', data: [1240, 1340, 1580, 1420, 1690, 1820, 1950, 2110, 2280, 2420, 2610, 2890] },
    { name: 'Churned', data: [120, 180, 220, 190, 240, 280, 310, 290, 340, 380, 410, 430] },
  ],
});

const segmentData = ref([
  { name: 'VIP', value: 45_280 },
  { name: 'Mass Affluent', value: 187_540 },
  { name: 'Mass Market', value: 698_120 },
  { name: 'Student', value: 156_320 },
  { name: 'Senior', value: 89_120 },
  { name: 'Dormant', value: 69_492 },
]);

const riskData = reactive({
  categories: ['LOW', 'MEDIUM', 'HIGH'],
  series: [
    { name: 'Count', data: [985_320, 198_400, 62_152] },
  ],
});

const topSegments = ref([
  { name: 'VIP', count: 45_280, clv: 25_400_000, trend: 12.3 },
  { name: 'Mass Affluent', count: 187_540, clv: 12_800_000, trend: 8.5 },
  { name: 'Senior', count: 89_120, clv: 9_500_000, trend: 4.2 },
  { name: 'Mass Market', count: 698_120, clv: 3_200_000, trend: -1.1 },
  { name: 'Student', count: 156_320, clv: 850_000, trend: 6.7 },
]);

function formatNumber(value: number): string {
  return new Intl.NumberFormat('id-ID').format(value);
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(amount);
}

onMounted(() => {
  // Auto-hide splash after 3.5s
  setTimeout(() => {
    showSplash.value = false;
  }, 3500);
});
</script>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }

/* ============================================
   AUREA BRAND VARIABLES
   ============================================ */
.aurea-360 {
  --aurea-gold-500: #D4AF37;
  --aurea-gold-300: #FFD764;
  --aurea-gold-700: #B8860B;
  --aurea-navy-600: #0A1929;
  --aurea-navy-500: #1A2F47;
  --aurea-navy-200: #B3C2D2;

  min-height: 100vh;
  background: linear-gradient(180deg, #F8F9FA 0%, #FFFFFF 100%);
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--aurea-navy-600);
}

/* ============================================
   AUREA SPLASH (in-component)
   ============================================ */
.aurea-splash-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0A1929 0%, #1A2F47 100%);
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
  width: 140px; height: 140px;
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
  font-size: 70px; font-weight: 700;
  color: #D4AF37;
  text-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
}
.aurea-splash-dots {
  position: absolute; bottom: 22px; left: 50%;
  transform: translateX(-50%);
  display: flex; gap: 8px;
}
.aurea-splash-dot {
  width: 6px; height: 6px;
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
  font-size: 42px; font-weight: 700;
  background: linear-gradient(135deg, #FFD764 0%, #D4AF37 50%, #B8860B 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 10px;
  margin: 0 0 0 10px;
  animation: aurea-text-reveal 1s ease-out 0.6s both;
}
@keyframes aurea-text-reveal {
  0% { opacity: 0; letter-spacing: 25px; filter: blur(10px); }
  100% { opacity: 1; letter-spacing: 10px; filter: blur(0); }
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

.splash-leave-active { transition: opacity 0.5s ease; }
.splash-leave-to { opacity: 0; }

/* ============================================
   AUREA HEADER
   ============================================ */
.aurea-header {
  background: white;
  border-bottom: 2px solid var(--aurea-gold-500);
  position: sticky; top: 0; z-index: 100;
  box-shadow: 0 2px 8px rgba(10, 25, 41, 0.06);
}
.aurea-header-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  height: 64px;
  gap: 32px;
}
.aurea-brand { display: flex; align-items: center; gap: 12px; }
.aurea-brand-logo { width: 36px; height: 36px; }
.aurea-brand-title {
  font-family: Georgia, serif;
  font-size: 18px; font-weight: 700;
  background: linear-gradient(135deg, #FFD764 0%, #D4AF37 50%, #B8860B 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 3px;
  line-height: 1.1;
}
.aurea-brand-subtitle {
  font-size: 9px;
  color: var(--aurea-navy-500);
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-top: 2px;
}

.aurea-nav { display: flex; gap: 4px; flex: 1; }
.aurea-nav a {
  padding: 8px 16px;
  border-radius: 8px;
  color: #6b7280;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.2s;
}
.aurea-nav a:hover {
  background: rgba(212, 175, 55, 0.1);
  color: var(--aurea-gold-700);
}
.aurea-nav a.active {
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  color: var(--aurea-navy-600);
  font-weight: 600;
}

.aurea-user-area { display: flex; align-items: center; gap: 12px; }
.aurea-status-dot {
  width: 8px; height: 8px;
  background: var(--aurea-gold-500);
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(212, 175, 55, 0.6);
  animation: aurea-pulse 2s ease-in-out infinite;
}
.aurea-user-name {
  font-size: 14px;
  color: var(--aurea-navy-600);
  font-weight: 500;
}
.aurea-avatar {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  color: var(--aurea-navy-600);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
}

/* ============================================
   AUREA MAIN CONTENT
   ============================================ */
.aurea-main {
  max-width: 1600px;
  margin: 0 auto;
  padding: 32px;
}

/* ============================================
   AUREA KPI CARDS
   ============================================ */
.aurea-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.aurea-kpi-card {
  position: relative;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(10, 25, 41, 0.06);
  display: flex;
  gap: 16px;
  align-items: flex-start;
  overflow: hidden;
  transition: all 0.3s;
  border: 1px solid rgba(212, 175, 55, 0.15);
}
.aurea-kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.15);
  border-color: var(--aurea-gold-500);
}
.aurea-kpi-icon {
  font-size: 32px;
  flex-shrink: 0;
  width: 48px; height: 48px;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(255, 215, 100, 0.1) 100%);
  border-radius: 12px;
}
.aurea-kpi-body { flex: 1; }
.aurea-kpi-label {
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 4px;
}
.aurea-kpi-value {
  font-family: Georgia, serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--aurea-navy-600);
  line-height: 1.2;
}
.aurea-kpi-unit { font-size: 14px; color: #9ca3af; font-weight: 400; }
.aurea-kpi-trend {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 10px;
  margin-top: 4px;
}
.trend-up { background: rgba(22, 163, 74, 0.1); color: #16a34a; }
.trend-down { background: rgba(220, 38, 38, 0.1); color: #dc2626; }
.aurea-kpi-accent {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--aurea-gold-500) 0%, var(--aurea-gold-300) 50%, var(--aurea-gold-700) 100%);
}

/* ============================================
   AUREA CHARTS
   ============================================ */
.aurea-charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}
@media (max-width: 1024px) {
  .aurea-charts-grid { grid-template-columns: 1fr; }
}
.aurea-card {
  background: white;
  border-radius: 12px;
  border: 1px solid rgba(212, 175, 55, 0.15);
  padding: 24px;
  box-shadow: 0 2px 8px rgba(10, 25, 41, 0.04);
  transition: all 0.2s;
}
.aurea-card:hover {
  border-color: var(--aurea-gold-500);
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.1);
}
.aurea-card h2 {
  font-family: Georgia, serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--aurea-navy-600);
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}
.aurea-chart-large h2 { font-size: 18px; }

.aurea-leaderboard {
  width: 100%; border-collapse: collapse; font-size: 14px;
}
.aurea-leaderboard th {
  text-align: left; padding: 8px 4px;
  border-bottom: 2px solid var(--aurea-gold-500);
  color: var(--aurea-gold-700);
  font-weight: 700;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.aurea-leaderboard td {
  padding: 12px 4px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.1);
  color: var(--aurea-navy-600);
}
.aurea-leaderboard tr:hover td { background: rgba(212, 175, 55, 0.05); }
.aurea-trend-up { color: #16a34a; font-weight: 700; }
.aurea-trend-down { color: #dc2626; font-weight: 700; }

/* ============================================
   AUREA INSIGHTS
   ============================================ */
.aurea-insights-section { margin-top: 32px; }
.aurea-section-title {
  font-family: Georgia, serif;
  font-size: 20px; font-weight: 700;
  color: var(--aurea-navy-600);
  margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px;
}
.aurea-insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}
.aurea-insight-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(212, 175, 55, 0.15);
  display: flex; gap: 16px;
  transition: all 0.2s;
}
.aurea-insight-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.15);
}
.aurea-insight-warning { border-left: 4px solid #ea580c; }
.aurea-insight-info { border-left: 4px solid #0284c7; }
.aurea-insight-success { border-left: 4px solid #16a34a; }
.aurea-insight-icon { font-size: 32px; flex-shrink: 0; }
.aurea-insight-body h3 {
  font-size: 15px; font-weight: 700;
  color: var(--aurea-navy-600);
  margin-bottom: 4px;
}
.aurea-insight-body p {
  font-size: 13px; color: #6b7280;
  line-height: 1.5; margin-bottom: 12px;
}
.aurea-action-btn {
  background: transparent;
  border: 1.5px solid var(--aurea-gold-500);
  color: var(--aurea-gold-700);
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
.aurea-action-btn:hover {
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  color: var(--aurea-navy-600);
}

/* ============================================
   AUREA FOOTER
   ============================================ */
.aurea-footer {
  margin-top: 48px;
  padding: 24px 32px;
  border-top: 1px solid rgba(212, 175, 55, 0.2);
  display: flex; align-items: center; justify-content: space-between;
}
.aurea-footer-brand { display: flex; align-items: center; gap: 12px; }
.aurea-footer-logo { width: 28px; height: 28px; }
.aurea-footer-title {
  font-family: Georgia, serif;
  font-size: 13px;
  font-weight: 700;
  background: linear-gradient(135deg, #D4AF37, #B8860B);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}
.aurea-footer-tagline {
  font-size: 9px;
  color: #9ca3af;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}
.aurea-footer-version {
  font-size: 11px;
  color: #9ca3af;
  font-family: 'JetBrains Mono', monospace;
}
</style>
