# Nuxt 3 Steward UI Starter

Starter template untuk steward-ui project (Sprint 9 Phase 1B).

## Quick Start

```bash
# Use this template
npx nuxi init my-app -t gh:bankxyz/mdm/steward-ui-template

# Or copy manually
cp -r templates/vue3/nuxt/* my-new-app/
cd my-new-app

# Install
npm install

# Development
npm run dev

# Build
npm run build
```

## What's Included

- ✅ Nuxt 3.11 + Vue 3.4 + TypeScript strict
- ✅ Element Plus 2.5 (dengan auto-import)
- ✅ Pinia 2.1 (state management)
- ✅ vue-i18n 9.9 (id/en)
- ✅ Axios 1.6 (HTTP client dengan auth interceptor)
- ✅ ECharts 5.5 (charts)
- ✅ VeeValidate 4.12 (forms)
- ✅ Vitest 1.2 + Playwright 1.41 (testing)
- ✅ MSW 2.2 (API mocking)
- ✅ Storybook 7.6 (component explorer)
- ✅ SCSS preprocessor dengan design tokens
- ✅ Security headers (CSP, X-Frame-Options, dll)
- ✅ Runtime config (API, WS, Keycloak)
- ✅ Auth middleware global
- ✅ Layouts: default + auth
- ✅ i18n default Indonesian

## File Structure

```
my-app/
├── app.vue                      # Root component
├── error.vue                    # Error page
├── nuxt.config.ts               # Nuxt config
├── package.json
├── tsconfig.json
├── vitest.config.ts
├── playwright.config.ts
├── i18n.config.ts
├── app/
│   ├── assets/scss/
│   │   ├── _variables.scss     # Design tokens
│   │   ├── _mixins.scss
│   │   └── main.scss           # Global styles
│   ├── components/              # Auto-imported
│   │   ├── foundation/         # StatCard, PageHeader, dll
│   │   ├── form/                # FormField, DatePicker, dll
│   │   ├── data/                # DataTable, SearchBar, dll
│   │   ├── navigation/          # Tabs, Breadcrumb
│   │   ├── feedback/            # Modal, Toast, Wizard
│   │   ├── business/            # CustomerCard, KycCaseCard
│   │   └── charts/              # LineChart, BarChart, PieChart
│   ├── composables/             # Auto-imported
│   │   ├── useApi.ts
│   │   ├── useAuth.ts
│   │   ├── useFormat.ts
│   │   ├── usePermissions.ts
│   │   ├── useForm.ts
│   │   ├── useTable.ts
│   │   └── useWebSocket.ts
│   ├── stores/                  # Pinia stores
│   │   ├── auth.ts
│   │   ├── notification.ts
│   │   ├── customer.ts
│   │   ├── matching.ts
│   │   ├── kyc.ts
│   │   └── audit.ts
│   ├── middleware/              # Route middleware
│   │   └── auth.global.ts
│   ├── layouts/
│   │   ├── default.vue
│   │   └── auth.vue
│   ├── pages/                   # File-based routing
│   │   ├── index.vue
│   │   ├── dashboard.vue
│   │   ├── customers/
│   │   ├── matching/
│   │   ├── kyc/
│   │   ├── audit/
│   │   ├── exceptions/
│   │   ├── auth/
│   │   │   └── login.vue
│   │   ├── profile.vue
│   │   └── settings.vue
│   ├── locales/
│   │   ├── id.json              # Indonesian
│   │   └── en.json              # English
│   ├── types/
│   │   ├── customer.ts
│   │   ├── matching.ts
│   │   ├── kyc.ts
│   │   └── audit.ts
│   └── utils/                   # Utilities
├── tests/
│   ├── unit/
│   ├── e2e/
│   ├── integration/
│   ├── mocks/                   # MSW handlers
│   └── setup.ts
├── .storybook/
│   ├── main.ts
│   └── preview.ts
├── public/                      # Static files
└── README.md
```

## Customization

### 1. Branding

Edit `app/assets/scss/_variables.scss`:
- Primary colors
- Typography
- Spacing scale
- Element Plus theme overrides

### 2. API Configuration

Edit `nuxt.config.ts` runtimeConfig:
```typescript
runtimeConfig: {
  public: {
    apiGatewayUrl: process.env.NUXT_API_GATEWAY_URL || 'http://localhost:8080',
    keycloakUrl: process.env.NUXT_KEYCLOAK_URL || 'http://localhost:8180',
    realm: 'mdm-dev',
    clientId: 'mdm-steward-ui',
    wsUrl: process.env.NUXT_WS_URL || 'ws://localhost:8080/ws',
  }
}
```

### 3. New Page

```bash
# Create a new page
touch app/pages/my-feature/index.vue
```

Page is auto-routed at `/my-feature`.

### 4. New Component

```bash
# Component is auto-imported (no manual import needed)
touch app/components/foundation/MyComponent.vue
```

Use in any page:
```vue
<template>
  <MyComponent title="Hello" />
</template>
```

### 5. New Store

```bash
touch app/stores/myFeature.ts
```

```typescript
import { defineStore } from 'pinia';

export const useMyFeatureStore = defineStore('myFeature', {
  state: () => ({ items: [] }),
  actions: {
    async fetchItems() { /* ... */ }
  }
});
```

### 6. New Composable

```bash
touch app/composables/useMyFeature.ts
```

```typescript
export function useMyFeature() {
  // ...
  return { /* ... */ };
}
```

Auto-imported, no manual import needed.

## Scripts

| Script | Description |
|---|---|
| `npm run dev` | Start dev server (http://localhost:3000) |
| `npm run build` | Production build |
| `npm run generate` | Static site generation |
| `npm run preview` | Preview production build |
| `npm run test` | Run unit tests |
| `npm run test:cov` | Unit tests with coverage |
| `npm run test:e2e` | Run E2E tests |
| `npm run test:e2e:ui` | E2E with Playwright UI |
| `npm run typecheck` | TypeScript check |
| `npm run lint` | ESLint |
| `npm run format` | Prettier |
| `npm run generate:api` | Generate API client from OpenAPI |
| `npm run storybook` | Component explorer |
| `npm run build-storybook` | Build Storybook static |

## Keycloak Setup

This template assumes Keycloak is running at `localhost:8180` with:
- Realm: `mdm-dev` (configurable)
- Client: `mdm-steward-ui`
- Users in realm config (see `keycloak/realm-config-dev.json` in main project)

Login flow uses `authorization_code` grant with PKCE.

## OpenAPI Client Generation

```bash
# Generate from openapi.yaml in project root
npm run generate:api

# Or specify custom path
npx tsx scripts/generate-api-client.ts path/to/openapi.yaml
```

Generates:
- `app/api-client/types.ts` - All TypeScript types
- `app/api-client/client.ts` - Service classes
- `app/api-client/common.ts` - Common types (PageResponse, etc.)
- `app/api-client/index.ts` - Barrel export

## Testing

### Unit Tests (Vitest)

```bash
npm run test
```

Located in `tests/unit/**`. Example:

```typescript
import { describe, it, expect } from 'vitest';
import { useFormat } from '~/composables/useFormat';

describe('useFormat', () => {
  it('formats currency', () => {
    const { formatCurrency } = useFormat();
    expect(formatCurrency(1500000)).toContain('1.500.000');
  });
});
```

### E2E Tests (Playwright)

```bash
npm run test:e2e
```

Located in `tests/e2e/**`. Example:

```typescript
import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
  await page.goto('/auth/login');
  await page.getByPlaceholder('Username').fill('admin');
  await page.getByPlaceholder('Password').fill('admin');
  await page.getByRole('button', { name: 'Masuk' }).click();
  await expect(page).toHaveURL('/dashboard');
});
```

### API Mocking (MSW)

Located in `tests/mocks/handlers.ts`:

```typescript
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/v1/customers', () => {
    return HttpResponse.json({ content: [], totalElements: 0 });
  }),
];
```

## Deployment

### Build for Production

```bash
npm run build
```

Output: `.output/` directory

### Run Production

```bash
node .output/server/index.mjs
```

Or use Docker:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY .output .output
COPY package.json .
RUN npm ci --omit=dev
EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]
```

### Kubernetes

See `infrastructure/k8s/steward-ui.yaml` in main project.

## License

Internal use only - Bank XYZ.
