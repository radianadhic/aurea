# Multi-stage build for API Gateway
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /build
COPY pom.xml .
COPY src ./src
RUN apk add --no-cache maven && mvn clean package -DskipTests

FROM eclipse-temurin:21-jre-alpine
LABEL maintainer="MDM Team <mdm-team@bankxyz.co.id>"
LABEL version="1.0.0"
LABEL description="MDM API Gateway (Spring Cloud Gateway)"

RUN apk add --no-cache curl tini
RUN addgroup -g 1001 -S mdm && adduser -u 1001 -S mdm -G mdm

WORKDIR /app
COPY --from=builder /build/target/api-gateway.jar /app/api-gateway.jar

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health/liveness || exit 1

USER mdm
EXPOSE 8080

# Tune for gateway: higher heap, more threads
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+UseG1GC -Dreactor.netty.http.server.accessLogEnabled=true"

ENTRYPOINT ["/sbin/tini", "--", "sh", "-c", "exec java $JAVA_OPTS -jar /app/api-gateway.jar"]
