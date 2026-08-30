# Spring Boot 3.2 Service Template

Base template for all 13 MDM microservices.

## Tech Stack

- **Java 21** (LTS, virtual threads)
- **Spring Boot 3.2** (latest)
- **PostgreSQL 16** + Flyway
- **Apache Kafka 3.7** (event streaming)
- **Redis 7.2** (cache via Valkey)
- **Keycloak 25** (OIDC auth)
- **HashiCorp Vault** (secrets)
- **Micrometer + Prometheus** (metrics)
- **OpenTelemetry** (tracing)
- **SpringDoc OpenAPI** (API docs)

## How to Use

1. Copy this template to your service directory:
   ```bash
   cp -r templates/spring-boot backend/my-service
   ```

2. Replace placeholders:
   - `{{SERVICE_NAME}}` → e.g., `customer-service`
   - `{{SERVICE_TITLE}}` → e.g., `Customer Service`
   - `{{SERVICE_DESCRIPTION}}` → Description
   - `{{PACKAGE}}` → e.g., `customer`
   - `{{MAIN_CLASS}}` → e.g., `CustomerServiceApplication`

3. Add service-specific code:
   - Domain entities in `src/main/java/com/bankxyz/mdm/{service}/domain/`
   - Repositories in `src/main/java/com/bankxyz/mdm/{service}/repository/`
   - Services in `src/main/java/com/bankxyz/mdm/{service}/service/`
   - Controllers in `src/main/java/com/bankxyz/mdm/{service}/controller/`
   - DTOs in `src/main/java/com/bankxyz/mdm/{service}/dto/`

4. Database migrations in `src/main/resources/db/migration/`:
   - `V1.0.0__init.sql` - Initial schema
   - `V1.0.1__add_indexes.sql` - Performance indexes

5. Build:
   ```bash
   mvn clean verify
   ```

6. Run:
   ```bash
   mvn spring-boot:run
   ```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SPRING_PROFILES_ACTIVE` | Spring profile | `dev` |
| `SERVER_PORT` | HTTP port | `8080` |
| `DB_URL` | PostgreSQL JDBC URL | - |
| `DB_USERNAME` | DB username | - |
| `DB_PASSWORD` | DB password (from Vault) | - |
| `REDIS_HOST` | Redis/Valkey host | `localhost` |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka brokers | `localhost:9092` |
| `KEYCLOAK_ISSUER_URI` | Keycloak realm URL | - |
| `VAULT_URI` | HashiCorp Vault URL | - |

## Health Check

- Liveness: `GET /actuator/health/liveness`
- Readiness: `GET /actuator/health/readiness`
- Metrics: `GET /actuator/prometheus`

## API Documentation

- Swagger UI: `http://localhost:${SERVER_PORT}/swagger-ui.html`
- OpenAPI JSON: `http://localhost:${SERVER_PORT}/v3/api-docs`

## Common Components

The template includes:
- ✅ `BaseEntity` (audit fields: createdAt, updatedAt, version, deletedAt)
- ✅ `GlobalExceptionHandler` (consistent error responses)
- ✅ `RequestCorrelationFilter` (correlation ID, MDC)
- ✅ `SecurityConfig` (OAuth2 resource server, RBAC)
- ✅ `OpenApiConfig` (API documentation)
- ✅ `KafkaConfig` (event publishing)
- ✅ `RedisConfig` (cache abstraction)
- ✅ `VaultConfig` (dynamic secrets)
- ✅ `ObservabilityConfig` (tracing, metrics)
