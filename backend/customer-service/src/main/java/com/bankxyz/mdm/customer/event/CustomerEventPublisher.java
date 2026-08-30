package com.bankxyz.mdm.customer.event;

import com.bankxyz.mdm.customer.domain.Customer;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;

/**
 * Publishes customer domain events to Kafka.
 * Consumed by: audit-service, notification-service, search-service, etc.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class CustomerEventPublisher {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Value("${app.kafka.topics.customer-events:mdm.customer.events}")
    private String topic;

    public void publishCustomerCreated(Customer customer) {
        publish("CUSTOMER_CREATED", customer, Map.of(
                "cifNumber", customer.getCifNumber(),
                "customerType", customer.getCustomerType(),
                "fullName", customer.getFullName() != null ? customer.getFullName() : customer.getLegalName(),
                "branchId", customer.getBranchId() != null ? customer.getBranchId() : ""
        ));
    }

    public void publishCustomerUpdated(Customer customer) {
        publish("CUSTOMER_UPDATED", customer, Map.of(
                "cifNumber", customer.getCifNumber(),
                "version", customer.getVersion()
        ));
    }

    public void publishCustomerDeleted(Customer customer) {
        publish("CUSTOMER_DELETED", customer, Map.of(
                "cifNumber", customer.getCifNumber()
        ));
    }

    public void publishCustomerKycApproved(Customer customer) {
        publish("CUSTOMER_KYC_APPROVED", customer, Map.of(
                "cifNumber", customer.getCifNumber(),
                "kycExpiryDate", customer.getKycExpiryDate() != null ? customer.getKycExpiryDate().toString() : ""
        ));
    }

    public void publishCustomerBlacklisted(Customer customer, String reason) {
        publish("CUSTOMER_BLACKLISTED", customer, Map.of(
                "cifNumber", customer.getCifNumber(),
                "reason", reason
        ));
    }

    private void publish(String eventType, Customer customer, Map<String, Object> payload) {
        UUID customerId = customer.getId();
        Map<String, Object> event = Map.of(
                "eventId", UUID.randomUUID().toString(),
                "eventType", eventType,
                "timestamp", Instant.now().toString(),
                "customerId", customerId.toString(),
                "payload", payload
        );
        try {
            kafkaTemplate.send(topic, customerId.toString(), event);
            log.debug("Published event {} for customer {}", eventType, customerId);
        } catch (Exception e) {
            log.error("Failed to publish event {} for customer {}: {}",
                    eventType, customerId, e.getMessage(), e);
        }
    }
}
