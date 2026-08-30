# Multi-stage build for customer-service
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /build
COPY pom.xml .
COPY src ./src
RUN apk add --no-cache maven && mvn clean package -DskipTests

FROM eclipse-temurin:21-jre-alpine
LABEL maintainer="MDM Team <mdm-team@bankxyz.co.id>"
LABEL version="1.0.0"
LABEL description="MDM Customer Service"

RUN apk add --no-cache curl tini
RUN addgroup -g 1001 -S mdm && adduser -u 1001 -S mdm -G mdm

WORKDIR /app
COPY --from=builder /build/target/customer-service.jar /app/customer-service.jar

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8082/actuator/health/liveness || exit 1

USER mdm
EXPOSE 8082

ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+UseG1GC"

ENTRYPOINT ["/sbin/tini", "--", "sh", "-c", "exec java $JAVA_OPTS -jar /app/customer-service.jar"]
