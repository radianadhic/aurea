# mdm-common - Shared Library

This is the shared library for all 13 MDM microservices. It provides:

## Components

### 1. **Entity** (`com.bankxyz.mdm.common.entity`)
- `BaseEntity` - Base JPA entity with:
  - UUID primary key
  - Audit fields (createdAt, updatedAt, createdBy, updatedBy)
  - Optimistic locking via @Version
  - Soft delete via deletedAt

### 2. **DTOs** (`com.bankxyz.mdm.common.dto`)
- `ApiError` - Standard API error response (RFC 7807 inspired)
- `PageResponse<T>` - Paginated response wrapper

### 3. **Exceptions** (`com.bankxyz.mdm.common.exception`)
- `BusinessException` - Base for business exceptions
- `ResourceNotFoundException` - 404 Not Found
- `GlobalExceptionHandler` - @RestControllerAdvice that converts all exceptions to ApiError

### 4. **Security** (`com.bankxyz.mdm.common.security`)
- `SecurityConfig` - OAuth2 Resource Server with Keycloak JWT
- `JwtAuthContext` - Utility to extract user info from JWT

### 5. **Filters** (`com.bankxyz.mdm.common.filter`)
- `CorrelationIdFilter` - Adds correlation ID, request ID, user ID to MDC

### 6. **Repository** (`com.bankxyz.mdm.common.repository`)
- `BaseRepository<T, ID>` - Base JPA repository with:
  - Soft delete query methods
  - Soft delete operations (softDeleteById, restoreById)
  - Count including/excluding soft-deleted

### 7. **Configuration** (`com.bankxyz.mdm.common.config`)
- `KafkaConfig` - Producer/Consumer factories, 5 standard topics
- `RedisConfig` - Cache manager with per-cache TTL
- `OpenApiConfig` - OpenAPI 3.0 metadata, OAuth2 security scheme

## How to Use in a Service

### 1. Add dependency

In your service's `pom.xml`:
```xml
<dependency>
    <groupId>com.bankxyz.mdm</groupId>
    <artifactId>mdm-common</artifactId>
    <version>1.0.0-SNAPSHOT</version>
</dependency>
```

### 2. Annotate main class

```java
@SpringBootApplication(scanBasePackages = {"com.bankxyz.mdm.myservice", "com.bankxyz.mdm.common"})
@EnableJpaAuditing
@EnableJpaRepositories(basePackages = {"com.bankxyz.mdm.myservice.repository", "com.bankxyz.mdm.common.repository"})
@EntityScan(basePackages = {"com.bankxyz.mdm.myservice.domain", "com.bankxyz.mdm.common.entity"})
public class MyServiceApplication { ... }
```

### 3. Extend BaseEntity

```java
@Entity
public class MyEntity extends BaseEntity {
    @Column private String name;
    // ... other fields
}
```

### 4. Extend BaseRepository

```java
public interface MyRepository extends BaseRepository<MyEntity, UUID> {
    // Custom queries here
}
```

### 5. Use JwtAuthContext

```java
import com.bankxyz.mdm.common.security.JwtAuthContext;

String userId = JwtAuthContext.getCurrentUserId().orElse("system");
if (JwtAuthContext.hasRole("ADMIN")) { ... }
```

### 6. Throw BusinessException

```java
import com.bankxyz.mdm.common.exception.BusinessException;

throw BusinessException.notFound("Customer", customerId);
throw BusinessException.unprocessable("NIK_INVALID", "NIK must be 16 digits");
throw BusinessException.forbidden("Access denied");
```

## Build

```bash
mvn clean install
```

This installs the library to your local Maven repository (~/.m2/repository).
All other services can then depend on it.
