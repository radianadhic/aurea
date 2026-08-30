package com.bankxyz.mdm.notification.controller;

import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.notification.dto.NotificationDtos.*;
import com.bankxyz.mdm.notification.service.NotificationService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/notifications")
@RequiredArgsConstructor
@Tag(name = "Notifications", description = "Multi-channel notification management")
public class NotificationController {

    private final NotificationService notificationService;

    @PostMapping("/send")
    @PreAuthorize("isAuthenticated()")
    @Operation(summary = "Send a notification")
    public NotificationDto send(@Valid @RequestBody SendNotificationRequest request) {
        return notificationService.send(request);
    }

    @PostMapping("/send-bulk")
    @PreAuthorize("hasAnyAuthority('notification:write', 'admin:config:write')")
    @Operation(summary = "Send bulk notifications")
    public List<NotificationDto> sendBulk(@Valid @RequestBody List<SendNotificationRequest> requests) {
        return notificationService.sendBulk(requests);
    }

    @PostMapping("/search")
    @PreAuthorize("hasAnyAuthority('notification:read', 'admin:config:read')")
    @Operation(summary = "Search notifications")
    public PageResponse<NotificationDto> search(@RequestBody NotificationSearchRequest request) {
        return notificationService.search(request);
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('notification:read')")
    @Operation(summary = "Get notification by ID")
    public NotificationDto getById(@PathVariable UUID id) {
        return notificationService.getById(id);
    }

    @PostMapping("/{id}/read")
    @PreAuthorize("isAuthenticated()")
    @Operation(summary = "Mark notification as read")
    public NotificationDto markAsRead(@PathVariable UUID id) {
        return notificationService.markAsRead(id);
    }

    @GetMapping("/stats")
    @PreAuthorize("hasAnyAuthority('notification:read', 'admin:config:read')")
    @Operation(summary = "Get notification statistics")
    public NotificationStatsResponse getStats() {
        return notificationService.getStats();
    }
}
