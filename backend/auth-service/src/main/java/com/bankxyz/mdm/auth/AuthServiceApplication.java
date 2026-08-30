package com.bankxyz.mdm.auth;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * Authentication Service.
 * Handles:
 * - User authentication (delegate to Keycloak)
 * - Session management
 * - MFA verification
 * - Password reset tokens
 * - Login attempt tracking
 *
 * @author MDM Bank XYZ Team
 * @version 1.0.0
 * @since 1.0.0
 */
@SpringBootApplication(scanBasePackages = {"com.bankxyz.mdm.auth", "com.bankxyz.mdm.common"})
@EnableDiscoveryClient
@EnableJpaAuditing
@EnableJpaRepositories(basePackages = {"com.bankxyz.mdm.auth.repository", "com.bankxyz.mdm.common.repository"})
@EntityScan(basePackages = {"com.bankxyz.mdm.auth.domain", "com.bankxyz.mdm.common.entity"})
@EnableKafka
@EnableAsync
@EnableScheduling
public class AuthServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(AuthServiceApplication.class, args);
    }
}
