package com.bankxyz.mdm.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

/**
 * MDM API Gateway.
 * Central entry point for all client requests.
 * Routes requests to appropriate backend microservice.
 *
 * Features:
 * - JWT validation (Keycloak)
 * - Rate limiting (Redis-based)
 * - Circuit breaker (Resilience4j)
 * - Request/response logging
 * - Distributed tracing
 * - CORS handling
 *
 * Port: 8080
 */
@SpringBootApplication
@EnableDiscoveryClient
public class GatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
}
