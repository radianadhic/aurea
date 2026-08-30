export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: true },
  ssr: true,

  typescript: { strict: true },

  modules: ['@pinia/nuxt', '@vueuse/nuxt', '@nuxtjs/i18n', '@element-plus/nuxt'],

  elementPlus: { importStyle: 'scss' },

  i18n: {
    strategy: 'no_prefix',
    defaultLocale: 'id',
    locales: [
      { code: 'id', name: 'Bahasa Indonesia', file: 'id.json' },
      { code: 'en', name: 'English', file: 'en.json' },
    ],
    langDir: 'locales/',
  },

  runtimeConfig: {
    public: {
      apiGatewayUrl: process.env.NUXT_API_GATEWAY_URL || 'http://localhost:8080',
      mlServiceUrl: process.env.NUXT_ML_SERVICE_URL || 'http://localhost:8087',
      keycloakUrl: process.env.NUXT_KEYCLOAK_URL || 'http://localhost:8180',
      realm: 'mdm-dev',
      clientId: 'mdm-customer360',
      wsUrl: process.env.NUXT_WS_URL || 'ws://localhost:8080/ws',
      appName: 'AUREA 360',
      appVersion: '1.0.0',
    },
  },

  app: {
    head: {
      title: 'AUREA 360 - Customer Intelligence',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'AUREA 360 - The Gold Standard of Data | Customer Intelligence Dashboard' },
        { name: 'theme-color', content: '#0A1929' },
        { property: 'og:title', content: 'AUREA 360 - The Gold Standard of Data' },
        { property: 'og:description', content: 'AUREA Customer 360 — powered by AUREA MDM Platform' },
        { property: 'og:image', content: '/logo-stacked.svg' },
      ],
      link: [
        // AUREA favicon (multi-format)
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
        { rel: 'apple-touch-icon', sizes: '128x128', href: '/favicon-128x128.png' },
      ],
    },
  },
});
