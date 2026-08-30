package com.bankxyz.mdm.matching;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.cache.annotation.EnableCaching;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;

/**
 * Matching Service - Customer duplicate detection and merging.
 *
 * Sprint 4 deliverable: Implements 3-layer matching engine
 * (Valkey cache → Elasticsearch → Neo4j graph) for real-time
 * duplicate detection with merge workflow.
 */
@SpringBootApplication(scanBasePackages = {
    "com.bankxyz.mdm.matching",
    "com.bankxyz.mdm.common"
})
@EnableJpaAuditing
@EnableJpaRepositories(basePackages = "com.bankxyz.mdm.matching.repository")
@EnableKafka
@EnableAsync
@EnableScheduling
@EnableCaching
@OpenAPIDefinition(
    info = @Info(
        title = "MDM Matching Service API",
        version = "1.0.0",
        description = "Customer matching and duplicate detection",
        contact = @Contact(name = "MDM Team", email = "mdm@bankxyz.co.id"),
        license = @License(name = "Bank XYZ Internal")
    )
)
public class MatchingServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(MatchingServiceApplication.class, args);
    }
}
