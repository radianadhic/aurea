# Multi-stage build for Admin Dashboard
FROM node:20-alpine AS builder
WORKDIR /build

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy source
COPY . .

# Build for production
RUN npm run build

# Runtime
FROM nginx:1.25-alpine

LABEL maintainer="MDM Team <mdm-team@bankxyz.co.id>"
LABEL version="1.0.0"
LABEL description="MDM Admin Dashboard (HTML5 + Tailwind + HTMX)"

# Copy built assets
COPY --from=builder /build/dist/admin-dashboard /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
