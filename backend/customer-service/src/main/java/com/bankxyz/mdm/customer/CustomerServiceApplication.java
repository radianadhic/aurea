package com.bankxyz.mdm.customer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.kafka.annotation.EnableKafka;

/**
 * Customer Service.
 * Manages:
 * - CIF (Customer Information File) - core customer data
 * - Identifiers (NIK, NPWP, Passport, etc)
 * - Addresses, contacts
 * - Family relationships
 * - Products (accounts, cards, loans)
 * - KYC status
 * - Consent (UU PDP)
 * - Risk profile
 * - Audit trail
 *
 * @author MDM Bank XYZ Team
 * @version 1.0.0
 * @since 1.0.0
 */
@SpringBootApplication(scanBasePackages = {"com.bankxyz.mdm.customer", "com.bankxyz.mdm.common"})
@EnableDiscoveryClient
@EnableJpaAuditing
@EnableJpaRepositories(basePackages = {"com.bankxyz.mdm.customer.repository", "com.bankxyz.mdm.common.repository"})
@EntityScan(basePackages = {"com.bankxyz.mdm.customer.domain", "com.bankxyz.mdm.common.entity"})
@EnableKafka
public class CustomerServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(CustomerServiceApplication.class, args);
    }
}
