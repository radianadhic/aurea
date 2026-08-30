// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: true },

  ssr: true,
  target: 'server',

  typescript: {
    strict: true,
    typeCheck: false, // set true in CI
  },

  modules: [
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@nuxtjs/i18n',
    '@element-plus/nuxt',
  ],

  // Element Plus auto-import
  elementPlus: {
    importStyle: 'scss',
  },

  // i18n
  i18n: {
    strategy: 'no_prefix',
    defaultLocale: 'id',
    locales: [
      { code: 'id', name: 'Bahasa Indonesia', file: 'id.json' },
      { code: 'en', name: 'English', file: 'en.json' },
    ],
    langDir: 'locales/',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root',
      alwaysRedirect: false,
    },
  },

  // SCSS
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@use "@/assets/scss/variables" as *;`,
        },
      },
    },
  },

  // Auto-import
  imports: {
    dirs: ['composables/**'],
  },

  components: {
    dirs: [
      { path: '~/components/foundation', prefix: '' },
      { path: '~/components/form', prefix: '' },
      { path: '~/components/data', prefix: '' },
      { path: '~/components/navigation', prefix: '' },
      { path: '~/components/feedback', prefix: '' },
      { path: '~/components/business', prefix: '' },
      { path: '~/components/charts', prefix: '' },
    ],
    global: true,
    pathPrefix: false,
  },

  // Runtime config
  runtimeConfig: {
    // Server-only
    keycloakAdminSecret: '',

    public: {
      apiGatewayUrl: process.env.NUXT_API_GATEWAY_URL || 'http://localhost:8080',
      keycloakUrl: process.env.NUXT_KEYCLOAK_URL || 'http://localhost:8180',
      realm: process.env.NUXT_KEYCLOAK_REALM || 'mdm-dev',
      clientId: process.env.NUXT_KEYCLOAK_CLIENT || 'mdm-steward-ui',
      wsUrl: process.env.NUXT_WS_URL || 'ws://localhost:8080/ws',
      appName: 'MDM Steward',
      appVersion: '1.0.0',
    },
  },

  // Security headers
  nitro: {
    routeRules: {
      '/**': {
        headers: {
          'X-Content-Type-Options': 'nosniff',
          'X-Frame-Options': 'DENY',
          'X-XSS-Protection': '1; mode=block',
          'Referrer-Policy': 'strict-origin-when-cross-origin',
          'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
          'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        },
      },
      '/api/**': {
        proxy: `${process.env.NUXT_API_GATEWAY_URL || 'http://localhost:8080'}/api/**`,
      },
    },
  },

  app: {
    head: {
      title: 'MDM Steward',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Master Data Management System' },
        { name: 'theme-color', content: '#1e40af' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
      ],
    },
  },

  experimental: {
    payloadExtraction: true,
  },
});
