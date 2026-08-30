# Multi-stage build for auth-service
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /build
COPY pom.xml .
COPY src ./src
RUN apk add --no-cache maven && mvn clean package -DskipTests

# Runtime
FROM eclipse-temurin:21-jre-alpine
LABEL maintainer="MDM Team <mdm-team@bankxyz.co.id>"
LABEL version="1.0.0"
LABEL description="MDM Authentication Service"

# Install required tools
RUN apk add --no-cache curl tini

# Create non-root user
RUN addgroup -g 1001 -S mdm && adduser -u 1001 -S mdm -G mdm

WORKDIR /app
COPY --from=builder /build/target/auth-service.jar /app/auth-service.jar

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8081/actuator/health/liveness || exit 1

USER mdm
EXPOSE 8081

# JVM tuning for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport \
               -XX:MaxRAMPercentage=75.0 \
               -XX:+UseG1GC \
               -XX:+UseStringDeduplication \
               -XX:+OptimizeStringConcat \
               -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["/sbin/tini", "--", "sh", "-c", "exec java $JAVA_OPTS -jar /app/auth-service.jar"]
