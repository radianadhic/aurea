// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },

  // SSR enabled for better SEO and performance
  ssr: true,

  // Modules
  modules: [
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@nuxtjs/i18n',
  ],

  // CSS
  css: [
    '~/assets/scss/main.scss',
    'element-plus/dist/index.css',
    'element-plus/theme-chalk/dark/css-vars.css',
  ],

  // Element Plus
  build: {
    transpile: ['element-plus'],
  },

  // Pinia
  pinia: {
    storesDirs: ['./stores/**'],
  },

  // i18n
  i18n: {
    locales: [
      { code: 'id', name: 'Bahasa Indonesia', file: 'id.json' },
      { code: 'en', name: 'English', file: 'en.json' },
    ],
    defaultLocale: 'id',
    lazy: true,
    langDir: 'locales/',
    strategy: 'no_prefix',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root',
      alwaysRedirect: false,
    },
  },

  // Runtime config
  runtimeConfig: {
    // Server-only
    keycloakClientSecret: process.env.NUXT_KEYCLOAK_CLIENT_SECRET || '',
    vaultToken: process.env.NUXT_VAULT_TOKEN || '',

    // Public (client-side)
    public: {
      apiGatewayUrl: process.env.NUXT_PUBLIC_API_GATEWAY_URL || 'http://localhost:8080',
      keycloakUrl: process.env.NUXT_PUBLIC_KEYCLOAK_URL || 'http://localhost:8180',
      keycloakRealm: process.env.NUXT_PUBLIC_KEYCLOAK_REALM || 'mdm-dev',
      keycloakClientId: process.env.NUXT_PUBLIC_KEYCLOAK_CLIENT_ID || 'mdm-steward-ui',
      wsUrl: process.env.NUXT_PUBLIC_WS_URL || 'ws://localhost:8080/ws',
      appName: 'AUREA Steward',
      appVersion: '1.0.0',
    },
  },

  // App
  app: {
    head: {
      title: 'AUREA Steward - CIF Management',
      htmlAttrs: { lang: 'id' },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'AUREA Steward - The Gold Standard of Data | CIF Management, KYC, Matching' },
        { name: 'theme-color', content: '#0A1929' },
        { property: 'og:title', content: 'AUREA Steward - The Gold Standard of Data' },
        { property: 'og:description', content: 'AUREA Steward — powered by AUREA MDM Platform' },
        { property: 'og:image', content: '/logo-stacked.svg' },
      ],
      link: [
        // AUREA favicon (multi-format)
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
        { rel: 'apple-touch-icon', sizes: '128x128', href: '/favicon-128x128.png' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Georgia&display=swap' },
      ],
    },
  },

  // Security headers
  nitro: {
    routeRules: {
      '/**': {
        headers: {
          'X-Content-Type-Options': 'nosniff',
          'X-Frame-Options': 'SAMEORIGIN',
          'X-XSS-Protection': '1; mode=block',
          'Referrer-Policy': 'strict-origin-when-cross-origin',
          'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
        },
      },
    },
  },

  // Vite
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/scss/_variables.scss" as *;',
        },
      },
    },
    optimizeDeps: {
      include: ['element-plus', 'axios', 'dayjs'],
    },
    server: {
      port: 3002,
      host: '0.0.0.0',
      strictPort: false,
    },
  },

  // Typescript
  typescript: {
    strict: true,
    typeCheck: false, // Disabled in dev for speed
  },

  // Experimental
  experimental: {
    payloadExtraction: true,
  },
});
