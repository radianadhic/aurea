/* eslint-env node */
const { configure } = require('quasar/wrappers');

module.exports = configure(function (ctx) {
  return {
    boot: ['axios', 'i18n', 'auth', 'pinia'],
    css: ['app.scss'],
    extras: ['capacitor'],

    build: {
      target: {
        browser: ['es2022', 'firefox115', 'chrome115', 'safari14'],
        node: 'node20',
      },
      vueRouterMode: 'history',
      env: {
        API_GATEWAY_URL: process.env.API_GATEWAY_URL || 'http://localhost:8080',
        KEYCLOAK_URL: process.env.KEYCLOAK_URL || 'http://localhost:8180',
        APP_VERSION: '1.0.0',
      },
      typescript: {
        strict: true,
        vueShim: true,
      },
    },

    devServer: {
      open: false,
      host: '0.0.0.0',
      port: 9000,
    },

    framework: {
      config: {
        brand: {
          primary: '#1e40af',
          secondary: '#d97706',
          accent: '#16a34a',
          dark: '#1f2937',
          'dark-page': '#111827',
          positive: '#16a34a',
          negative: '#dc2626',
          info: '#0284c7',
          warning: '#ea580c',
        },
        notify: {
          position: 'top',
          timeout: 3000,
        },
        loading: {
          delay: 200,
        },
      },
      iconSet: 'material-icons',
      lang: 'id',
      plugins: ['Notify', 'Dialog', 'Loading', 'LocalStorage', 'SessionStorage'],
    },

    animations: 'all',

    ssr: {
      pwa: false,
      prodPort: 3000,
      middlewares: ['render'],
    },

    pwa: {
      workboxMode: 'GenerateSW',
      injectPwaMetaTags: true,
      swFilename: 'sw.js',
      manifestFilename: 'manifest.json',
      useCredentialsForManifestTag: false,
      // disable until you're ready
      enabled: false,
      params: {
        scope: '/',
      },
    },

    cordova: {},

    capacitor: {
      hideSplashscreen: true,
      capacitorCliSettings: {
        android: {
          appId: 'co.id.bankxyz.mdm',
          appName: 'Bank XYZ',
        },
        ios: {
          appId: 'co.id.bankxyz.mdm',
          appName: 'Bank XYZ',
        },
      },
    },
  };
});
