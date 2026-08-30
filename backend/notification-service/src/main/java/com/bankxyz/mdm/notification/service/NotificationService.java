package com.bankxyz.mdm.notification.service;

import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.common.exception.BusinessException;
import com.bankxyz.mdm.common.exception.ResourceNotFoundException;
import com.bankxyz.mdm.notification.domain.Notification;
import com.bankxyz.mdm.notification.domain.NotificationChannel;
import com.bankxyz.mdm.notification.domain.NotificationStatus;
import com.bankxyz.mdm.notification.dto.*;
import com.bankxyz.mdm.notification.repository.NotificationRepository;
import com.bankxyz.mdm.notification.repository.NotificationTemplateRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationService {

    private final NotificationRepository notificationRepository;
    private final NotificationTemplateRepository templateRepository;
    private final EmailNotificationProvider emailProvider;
    private final SmsNotificationProvider smsProvider;

    /**
     * Send a single notification through the appropriate channel.
     */
    @Transactional
    public NotificationDto send(SendNotificationRequest request) {
        log.info("Sending notification: channel={}, recipient={}",
            request.channel(), request.recipientAddress());

        Notification notification = Notification.builder()
            .channel(request.channel())
            .templateCode(request.templateCode())
            .subject(request.subject())
            .body(request.body())
            .recipientId(request.recipientId())
            .recipientAddress(request.recipientAddress())
            .recipientName(request.recipientName())
            .locale(request.locale() != null ? request.locale() : "id")
            .variables(request.variables() != null ? request.variables() : new HashMap<>())
            .priority(request.priority() != null ? request.priority()
                : com.bankxyz.mdm.notification.domain.NotificationPriority.NORMAL)
            .scheduledAt(request.scheduledAt())
            .correlationId(request.correlationId())
            .sourceService(request.sourceService() != null ? request.sourceService() : "manual")
            .status(NotificationStatus.QUEUED)
            .build();

        Notification saved = notificationRepository.save(notification);

        // If not scheduled, dispatch immediately
        if (request.scheduledAt() == null || request.scheduledAt().isBefore(Instant.now())) {
            dispatch(saved);
        }

        return NotificationDto.from(saved);
    }

    /**
     * Send bulk notifications (e.g. batch customer onboarding).
     */
    @Transactional
    public List<NotificationDto> sendBulk(List<SendNotificationRequest> requests) {
        log.info("Sending bulk notifications: count={}", requests.size());
        return requests.stream()
            .map(this::send)
            .toList();
    }

    /**
     * Dispatch a notification to the appropriate provider.
     */
    private void dispatch(Notification notification) {
        try {
            switch (notification.getChannel()) {
                case EMAIL -> emailProvider.send(notification);
                case SMS -> smsProvider.send(notification);
                case WHATSAPP -> log.info("WhatsApp not yet implemented, falling back to SMS");
                case PUSH -> log.info("Push notification - would use FCM");
                case IN_APP -> {
                    notification.setStatus(NotificationStatus.DELIVERED);
                    notification.setSentAt(Instant.now());
                    notificationRepository.save(notification);
                }
                default -> throw new BusinessException("UNSUPPORTED_CHANNEL",
                    "Channel not supported: " + notification.getChannel());
            }
        } catch (Exception e) {
            log.error("Dispatch failed for notification: {}", notification.getId(), e);
            notification.setStatus(NotificationStatus.FAILED);
            notification.setErrorMessage(e.getMessage());
            notificationRepository.save(notification);
        }
    }

    /**
     * Scheduled task - process pending scheduled notifications.
     */
    @Scheduled(fixedDelay = 30000) // every 30 seconds
    @Transactional
    public void processScheduledNotifications() {
        List<Notification> scheduled = notificationRepository
            .findByStatusAndScheduledAtBefore(NotificationStatus.QUEUED, Instant.now());
        if (!scheduled.isEmpty()) {
            log.info("Processing {} scheduled notifications", scheduled.size());
            scheduled.forEach(this::dispatch);
        }
    }

    /**
     * Retry failed notifications.
     */
    @Scheduled(fixedDelay = 60000) // every minute
    @Transactional
    public void retryFailedNotifications() {
        Instant since = Instant.now().minus(5, ChronoUnit.MINUTES);
        Page<Notification> failed = notificationRepository.search(
            null, null, NotificationStatus.FAILED, since, Instant.now(),
            PageRequest.of(0, 100));
        int retried = 0;
        for (Notification n : failed.getContent()) {
            if (n.canRetry()) {
                n.setStatus(NotificationStatus.QUEUED);
                n.setErrorMessage(null);
                notificationRepository.save(n);
                dispatch(n);
                retried++;
            }
        }
        if (retried > 0) log.info("Retried {} failed notifications", retried);
    }

    /**
     * Search notifications.
     */
    @Transactional(readOnly = true)
    public PageResponse<NotificationDto> search(NotificationSearchRequest request) {
        Pageable pageable = PageRequest.of(
            request.page() != null ? request.page() : 0,
            request.size() != null ? request.size() : 20);
        Page<Notification> page = notificationRepository.search(
            request.recipientId(),
            request.channel(),
            request.status(),
            request.fromDate(),
            request.toDate(),
            pageable);
        List<NotificationDto> content = page.getContent().stream()
            .map(NotificationDto::from).toList();
        return PageResponse.<NotificationDto>builder()
            .content(content)
            .page(page.getNumber())
            .size(page.getSize())
            .totalElements(page.getTotalElements())
            .totalPages(page.getTotalPages())
            .first(page.isFirst())
            .last(page.isLast())
            .numberOfElements(page.getNumberOfElements())
            .empty(page.isEmpty())
            .build();
    }

    @Transactional(readOnly = true)
    public NotificationDto getById(UUID id) {
        Notification n = notificationRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Notification not found: " + id));
        return NotificationDto.from(n);
    }

    /**
     * Mark as read (for IN_APP).
     */
    @Transactional
    public NotificationDto markAsRead(UUID id) {
        Notification n = notificationRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Notification not found: " + id));
        if (n.getReadAt() == null) {
            n.setReadAt(Instant.now());
            n.setStatus(NotificationStatus.READ);
            n = notificationRepository.save(n);
        }
        return NotificationDto.from(n);
    }

    /**
     * Get statistics.
     */
    @Transactional(readOnly = true)
    public NotificationStatsResponse getStats() {
        Instant last24h = Instant.now().minus(24, ChronoUnit.HOURS);
        Map<String, Long> byChannel = new HashMap<>();
        notificationRepository.countByChannelSince(last24h).forEach(row ->
            byChannel.put(((NotificationChannel) row[0]).name(), (Long) row[1]));
        Map<String, Long> byStatus = new HashMap<>();
        notificationRepository.countByStatusSince(last24h).forEach(row ->
            byStatus.put(((NotificationStatus) row[0]).name(), (Long) row[1]));
        return new NotificationStatsResponse(
            notificationRepository.count(),
            byChannel,
            byStatus
        );
    }
}
