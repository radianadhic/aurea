import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  root: 'src',
  publicDir: '../../public',
  base: '/',
  build: {
    outDir: '../../dist/admin-dashboard',
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/index.html'),
        login: path.resolve(__dirname, 'src/pages/login.html'),
        dashboard: path.resolve(__dirname, 'src/pages/dashboard.html'),
        monitoring: path.resolve(__dirname, 'src/pages/monitoring.html'),
        config: path.resolve(__dirname, 'src/pages/config.html'),
        reports: path.resolve(__dirname, 'src/pages/reports.html'),
        health: path.resolve(__dirname, 'src/pages/health.html'),
        dr: path.resolve(__dirname, 'src/pages/dr-failover.html'),
        finops: path.resolve(__dirname, 'src/pages/finops.html'),
        'config-nifi': path.resolve(__dirname, 'src/pages/config/nifi.html'),
        'config-sources': path.resolve(__dirname, 'src/pages/config/source-systems.html'),
        'config-matching': path.resolve(__dirname, 'src/pages/config/matching.html'),
        'config-etl': path.resolve(__dirname, 'src/pages/config/etl-display.html'),
        'config-backup': path.resolve(__dirname, 'src/pages/config/backup.html'),
        'config-brm': path.resolve(__dirname, 'src/pages/config/brm.html'),
        'report-builder': path.resolve(__dirname, 'src/pages/reports/builder.html'),
        'insights': path.resolve(__dirname, 'src/pages/insights.html'),
        'segmentation': path.resolve(__dirname, 'src/pages/segmentation.html'),
        'churn': path.resolve(__dirname, 'src/pages/churn.html'),
        'fraud': path.resolve(__dirname, 'src/pages/fraud.html'),
        'report-scheduled': path.resolve(__dirname, 'src/pages/reports/scheduled.html'),
      },
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    strictPort: false,
    open: false,
    cors: true,
    allowedHosts: true,  // AUREA: allow all hosts for sandbox preview
    proxy: {
      // Proxy API requests to backend
      '/api': {
        target: process.env.VITE_API_GATEWAY_URL || 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
      },
      '/auth': {
        target: process.env.VITE_AUTH_SERVICE_URL || 'http://localhost:8081',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
  },
});
