package com.bankxyz.mdm.notification.service;

import com.bankxyz.mdm.notification.domain.Notification;
import com.bankxyz.mdm.notification.domain.NotificationStatus;
import com.bankxyz.mdm.notification.repository.NotificationRepository;
import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Slf4j
public class SmsNotificationProvider {

    private final NotificationRepository notificationRepository;

    @Value("${mdm.notification.sms.account-sid:}")
    private String accountSid;

    @Value("${mdm.notification.sms.auth-token:}")
    private String authToken;

    @Value("${mdm.notification.sms.from-number:+6281234567890}")
    private String fromNumber;

    public SmsNotificationProvider(NotificationRepository notificationRepository) {
        this.notificationRepository = notificationRepository;
    }

    @PostConstruct
    public void init() {
        if (accountSid != null && !accountSid.isBlank()) {
            Twilio.init(accountSid, authToken);
            log.info("Twilio SMS provider initialized");
        } else {
            log.warn("Twilio SMS credentials not configured - SMS will be in mock mode");
        }
    }

    @Async
    @Transactional
    public void send(Notification notification) {
        log.info("Sending SMS to {}", notification.getRecipientAddress());

        try {
            if (accountSid == null || accountSid.isBlank()) {
                // Mock mode for development
                notification.setStatus(NotificationStatus.SENT);
                notification.setSentAt(java.time.Instant.now());
                notification.setProviderMessageId("MOCK-" + System.currentTimeMillis());
                log.info("[MOCK SMS] to {}: {}", notification.getRecipientAddress(), notification.getBody());
            } else {
                Message message = Message.creator(
                    new PhoneNumber(notification.getRecipientAddress()),
                    new PhoneNumber(fromNumber),
                    notification.getBody()
                ).create();

                notification.setStatus(NotificationStatus.SENT);
                notification.setSentAt(java.time.Instant.now());
                notification.setProviderMessageId(message.getSid());
            }
            notificationRepository.save(notification);
        } catch (Exception e) {
            log.error("Failed to send SMS", e);
            notification.setStatus(NotificationStatus.FAILED);
            notification.setErrorMessage(e.getMessage());
            notification.setRetryCount(notification.getRetryCount() + 1);
            notificationRepository.save(notification);
        }
    }
}
