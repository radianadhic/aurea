package com.bankxyz.mdm.audit;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.cache.annotation.EnableCaching;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;

/**
 * Audit Service - Immutable audit trail for all MDM operations.
 *
 * Listens to Kafka events from all other services and persists
 * immutable audit records. Supports compliance reporting (OJK, BI, PPATK).
 */
@SpringBootApplication(scanBasePackages = {
    "com.bankxyz.mdm.audit",
    "com.bankxyz.mdm.common"
})
@EnableJpaAuditing
@EnableJpaRepositories(basePackages = "com.bankxyz.mdm.audit.repository")
@EnableKafka
@EnableAsync
@EnableCaching
@OpenAPIDefinition(
    info = @Info(
        title = "MDM Audit Service API",
        version = "1.0.0",
        description = "Immutable audit trail for MDM operations",
        contact = @Contact(name = "MDM Team", email = "mdm@bankxyz.co.id")
    )
)
public class AuditServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(AuditServiceApplication.class, args);
    }
}
