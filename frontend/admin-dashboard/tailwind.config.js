/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js}'],
  theme: {
    extend: {
      colors: {
        // ============================================================
        // AUREA Brand Colors - The Gold Standard of Data
        // ============================================================
        aurea: {
          gold: {
            50: '#FFF9E6',
            100: '#FFF0BF',
            200: '#FFE599',
            300: '#FFD764',  // light
            400: '#E5C04A',
            500: '#D4AF37',  // PRIMARY
            600: '#C49A2A',
            700: '#B8860B',  // dark
            800: '#946B09',
            900: '#704F07',
            DEFAULT: '#D4AF37',
          },
          navy: {
            50: '#E6EBF2',
            100: '#B3C2D2',
            200: '#809AB3',
            300: '#4D7193',
            400: '#264A75',
            500: '#1A2F47',  // light
            600: '#0A1929',  // PRIMARY
            700: '#081421',
            800: '#061019',
            900: '#040B13',
            DEFAULT: '#0A1929',
          },
          accent: '#FFD764',
        },
        // Legacy Bank XYZ colors (preserved for backward compat)
        primary: {
          50: '#E6EBF2',
          100: '#B3C2D2',
          200: '#809AB3',
          300: '#4D7193',
          400: '#264A75',
          500: '#1A2F47',
          600: '#0A1929',
          700: '#081421',
          800: '#061019',
          900: '#040B13',
          DEFAULT: '#0A1929',
        },
        secondary: {
          50: '#FFF9E6',
          100: '#FFF0BF',
          200: '#FFE599',
          300: '#FFD764',
          400: '#E5C04A',
          500: '#D4AF37',
          600: '#C49A2A',
          700: '#B8860B',
          800: '#946B09',
          900: '#704F07',
          DEFAULT: '#D4AF37',
        },
        success: '#16a34a',
        warning: '#ea580c',
        danger: '#dc2626',
        info: '#0284c7',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
        brand: ['Georgia', 'Times New Roman', 'serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s linear infinite',
        'spin-slow': 'spin 2s linear infinite',
        'aurea-pulse': 'aurea-pulse 2.5s ease-in-out infinite',
        'aurea-bounce': 'aurea-bounce 1.4s ease-in-out infinite',
        'aurea-rotate': 'aurea-rotate 1.5s linear infinite',
        'aurea-shimmer': 'aurea-shimmer 1.8s ease-in-out infinite',
      },
      keyframes: {
        'aurea-pulse': {
          '0%, 100%': { boxShadow: '0 0 30px rgba(212, 175, 55, 0.2)' },
          '50%': { boxShadow: '0 0 60px rgba(212, 175, 55, 0.5)' },
        },
        'aurea-bounce': {
          '0%, 80%, 100%': { transform: 'scale(0.6)', opacity: '0.4' },
          '40%': { transform: 'scale(1.2)', opacity: '1' },
        },
        'aurea-rotate': {
          'to': { transform: 'rotate(360deg)' },
        },
        'aurea-shimmer': {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      backgroundImage: {
        'aurea-gradient': 'linear-gradient(135deg, #FFD764 0%, #D4AF37 50%, #B8860B 100%)',
        'aurea-navy': 'linear-gradient(135deg, #0A1929 0%, #1A2F47 100%)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      {
        aurea: {
          'primary': '#D4AF37',
          'primary-content': '#0A1929',
          'secondary': '#1A2F47',
          'secondary-content': '#FFD764',
          'accent': '#FFD764',
          'accent-content': '#0A1929',
          'neutral': '#0A1929',
          'neutral-content': '#FFD764',
          'base-100': '#FFFFFF',
          'base-200': '#F8F9FA',
          'base-300': '#E9ECEF',
          'base-content': '#0A1929',
          'info': '#0284c7',
          'success': '#16a34a',
          'warning': '#ea580c',
          'error': '#dc2626',
        },
        aureaDark: {
          'primary': '#D4AF37',
          'primary-content': '#0A1929',
          'secondary': '#FFD764',
          'secondary-content': '#0A1929',
          'accent': '#FFD764',
          'accent-content': '#0A1929',
          'neutral': '#0A1929',
          'neutral-content': '#FFD764',
          'base-100': '#0A1929',
          'base-200': '#081421',
          'base-300': '#061019',
          'base-content': '#FFFFFF',
          'info': '#0284c7',
          'success': '#16a34a',
          'warning': '#ea580c',
          'error': '#dc2626',
        },
      },
    ],
  },
};
