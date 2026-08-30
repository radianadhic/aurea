package com.bankxyz.mdm.notification.domain;

import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Notification - Multi-channel notification record.
 * Channels: EMAIL, SMS, WHATSAPP, PUSH, IN_APP
 */
@Entity
@Table(name = "notifications", indexes = {
    @Index(name = "idx_notif_recipient", columnList = "recipient_id"),
    @Index(name = "idx_notif_status", columnList = "status"),
    @Index(name = "idx_notif_channel", columnList = "channel"),
    @Index(name = "idx_notif_created", columnList = "created_at"),
    @Index(name = "idx_notif_correlation", columnList = "correlation_id")
})
@EntityListeners(AuditingEntityListener.class)
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Notification {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Enumerated(EnumType.STRING)
    @Column(name = "channel", nullable = false, length = 20)
    private NotificationChannel channel;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 20)
    @Builder.Default
    private NotificationStatus status = NotificationStatus.PENDING;

    @Column(name = "template_code", length = 100)
    private String templateCode;

    @Column(name = "subject", length = 500)
    private String subject;

    @Column(name = "body", columnDefinition = "TEXT")
    private String body;

    /** Recipient (userId, email, phone, dll depending on channel) */
    @Column(name = "recipient_id", length = 100)
    private String recipientId;

    @Column(name = "recipient_address", length = 200)
    private String recipientAddress;

    @Column(name = "recipient_name", length = 200)
    private String recipientName;

    /** Locale for template rendering */
    @Column(name = "locale", length = 10)
    @Builder.Default
    private String locale = "id";

    /** Template variables */
    @jakarta.persistence.Convert(converter = JsonStringConverter.class)
    @Column(name = "variables", columnDefinition = "TEXT")
    @Builder.Default
    private Map<String, Object> variables = new HashMap<>();

    /** Priority: HIGH, NORMAL, LOW */
    @Enumerated(EnumType.STRING)
    @Column(name = "priority", length = 20)
    @Builder.Default
    private NotificationPriority priority = NotificationPriority.NORMAL;

    /** Scheduled send time (for delayed notifications) */
    @Column(name = "scheduled_at")
    private Instant scheduledAt;

    /** When actually sent */
    @Column(name = "sent_at")
    private Instant sentAt;

    /** When delivered (provider callback) */
    @Column(name = "delivered_at")
    private Instant deliveredAt;

    /** When read (for IN_APP) */
    @Column(name = "read_at")
    private Instant readAt;

    /** Provider message ID (for tracking) */
    @Column(name = "provider_message_id", length = 200)
    private String providerMessageId;

    @Column(name = "error_message", length = 2000)
    private String errorMessage;

    @Column(name = "retry_count", nullable = false)
    @Builder.Default
    private Integer retryCount = 0;

    @Column(name = "max_retries", nullable = false)
    @Builder.Default
    private Integer maxRetries = 3;

    @Column(name = "correlation_id", length = 50)
    private String correlationId;

    @Column(name = "source_service", length = 50)
    private String sourceService;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    @Column(name = "deleted_at")
    private Instant deletedAt;

    public boolean canRetry() {
        return retryCount < maxRetries && status == NotificationStatus.FAILED;
    }

    public void markSent(String providerMessageId) {
        this.status = NotificationStatus.SENT;
        this.sentAt = Instant.now();
        this.providerMessageId = providerMessageId;
    }

    public void markDelivered() {
        this.status = NotificationStatus.DELIVERED;
        this.deliveredAt = Instant.now();
    }

    public void markFailed(String error) {
        this.status = NotificationStatus.FAILED;
        this.errorMessage = error;
        this.retryCount++;
    }
}
