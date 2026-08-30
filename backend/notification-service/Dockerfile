FROM eclipse-temurin:21-jdk-jammy AS build
WORKDIR /workspace
COPY pom.xml .
COPY src src
RUN mvn clean package -DskipTests -B

FROM eclipse-temurin:21-jre-jammy
RUN groupadd -r mdm && useradd -r -g mdm mdm
WORKDIR /app
COPY --from=build /workspace/target/*.jar app.jar
USER mdm
EXPOSE 8085
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:8085/actuator/health/liveness || exit 1
ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-jar", "app.jar"]
