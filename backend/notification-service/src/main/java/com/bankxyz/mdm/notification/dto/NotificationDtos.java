package com.bankxyz.mdm.notification.dto;

import com.bankxyz.mdm.notification.domain.Notification;
import com.bankxyz.mdm.notification.domain.NotificationChannel;
import com.bankxyz.mdm.notification.domain.NotificationPriority;
import com.bankxyz.mdm.notification.domain.NotificationStatus;
import jakarta.validation.constraints.*;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class NotificationDtos {

    public record NotificationDto(
        UUID id,
        NotificationChannel channel,
        NotificationStatus status,
        String templateCode,
        String subject,
        String body,
        String recipientId,
        String recipientAddress,
        String recipientName,
        String locale,
        Map<String, Object> variables,
        NotificationPriority priority,
        Instant scheduledAt,
        Instant sentAt,
        Instant deliveredAt,
        Instant readAt,
        String providerMessageId,
        String errorMessage,
        Integer retryCount,
        String correlationId,
        String sourceService,
        Instant createdAt
    ) {
        public static NotificationDto from(Notification n) {
            return new NotificationDto(
                n.getId(), n.getChannel(), n.getStatus(),
                n.getTemplateCode(), n.getSubject(), n.getBody(),
                n.getRecipientId(), n.getRecipientAddress(), n.getRecipientName(),
                n.getLocale(), n.getVariables(), n.getPriority(),
                n.getScheduledAt(), n.getSentAt(), n.getDeliveredAt(), n.getReadAt(),
                n.getProviderMessageId(), n.getErrorMessage(), n.getRetryCount(),
                n.getCorrelationId(), n.getSourceService(), n.getCreatedAt()
            );
        }
    }

    public record SendNotificationRequest(
        @NotNull NotificationChannel channel,
        String templateCode,
        @Size(max = 500) String subject,
        String body,
        String recipientId,
        @NotBlank @Size(max = 200) String recipientAddress,
        @Size(max = 200) String recipientName,
        String locale,
        Map<String, Object> variables,
        NotificationPriority priority,
        Instant scheduledAt,
        String correlationId,
        String sourceService
    ) {
        public SendNotificationRequest {
            if (locale == null) locale = "id";
            if (variables == null) variables = new HashMap<>();
        }
    }

    public record NotificationSearchRequest(
        String recipientId,
        NotificationChannel channel,
        NotificationStatus status,
        Instant fromDate,
        Instant toDate,
        Integer page,
        Integer size
    ) {}

    public record NotificationStatsResponse(
        long totalNotifications,
        Map<String, Long> byChannelLast24h,
        Map<String, Long> byStatusLast24h
    ) {}

    public record CreateTemplateRequest(
        @NotBlank @Size(max = 100) String code,
        @NotBlank @Size(max = 200) String name,
        @Size(max = 500) String description,
        @NotNull NotificationChannel channel,
        @NotBlank @Size(max = 10) String locale,
        @Size(max = 500) String subject,
        @NotBlank String body
    ) {}
}
