package com.bankxyz.mdm.notification.kafka;

import com.bankxyz.mdm.notification.dto.NotificationDtos.SendNotificationRequest;
import com.bankxyz.mdm.notification.service.NotificationService;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * Listens to MDM events and sends appropriate notifications.
 *
 * Example: customer-service publishes "customer.created" → notification-service
 * sends welcome email + WhatsApp.
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class NotificationEventConsumer {

    private final NotificationService notificationService;
    private final ObjectMapper objectMapper;

    @KafkaListener(
        topics = {
            "${mdm.kafka.topics.customer:mdm.customer.events}",
            "${mdm.kafka.topics.match:mdm.match.events}",
            "${mdm.kafka.topics.kyc:mdm.kyc.events}",
            "${mdm.kafka.topics.workflow:mdm.workflow.events}"
        },
        groupId = "notification-service"
    )
    public void onEvent(Map<String, Object> event) {
        try {
            log.debug("Received event for notification: {}", event);

            String eventType = (String) event.get("eventType");
            if (eventType == null) return;

            // Convert event to SendNotificationRequest based on type
            SendNotificationRequest request = buildNotificationRequest(eventType, event);
            if (request != null) {
                notificationService.send(request);
            }
        } catch (Exception e) {
            log.error("Failed to process notification event: {}", e.getMessage(), e);
        }
    }

    private SendNotificationRequest buildNotificationRequest(String eventType, Map<String, Object> event) {
        return switch (eventType) {
            case "customer.created" -> new SendNotificationRequest(
                com.bankxyz.mdm.notification.domain.NotificationChannel.EMAIL,
                "WELCOME_NEW_CUSTOMER",
                "Selamat Datang di Bank XYZ",
                null,
                (String) event.get("userId"),
                (String) event.get("email"),
                (String) event.get("fullName"),
                "id",
                Map.of("name", event.getOrDefault("fullName", "")),
                com.bankxyz.mdm.notification.domain.NotificationPriority.NORMAL,
                null,
                (String) event.get("correlationId"),
                "auto-event"
            );
            case "kyc.approved" -> new SendNotificationRequest(
                com.bankxyz.mdm.notification.domain.NotificationChannel.EMAIL,
                "KYC_APPROVED",
                "KYC Anda Telah Disetujui",
                null,
                (String) event.get("userId"),
                (String) event.get("email"),
                (String) event.get("fullName"),
                "id",
                Map.of("name", event.getOrDefault("fullName", "")),
                com.bankxyz.mdm.notification.domain.NotificationPriority.HIGH,
                null,
                (String) event.get("correlationId"),
                "auto-event"
            );
            case "kyc.rejected" -> new SendNotificationRequest(
                com.bankxyz.mdm.notification.domain.NotificationChannel.EMAIL,
                "KYC_REJECTED",
                "KYC Anda Ditolak",
                null,
                (String) event.get("userId"),
                (String) event.get("email"),
                (String) event.get("fullName"),
                "id",
                Map.of("reason", event.getOrDefault("reason", "")),
                com.bankxyz.mdm.notification.domain.NotificationPriority.HIGH,
                null,
                (String) event.get("correlationId"),
                "auto-event"
            );
            case "match.merged" -> new SendNotificationRequest(
                com.bankxyz.mdm.notification.domain.NotificationChannel.IN_APP,
                "MATCH_MERGED",
                "Data nasabah berhasil di-merge",
                null,
                (String) event.get("userId"),
                (String) event.get("userId"),
                (String) event.get("userFullName"),
                "id",
                Map.of("matchGroupId", event.getOrDefault("matchGroupId", "")),
                com.bankxyz.mdm.notification.domain.NotificationPriority.NORMAL,
                null,
                (String) event.get("correlationId"),
                "auto-event"
            );
            default -> null;
        };
    }
}
