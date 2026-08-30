package com.bankxyz.mdm.matching.controller;

import com.bankxyz.mdm.matching.dto.*;
import com.bankxyz.mdm.matching.service.MatchingService;
import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.common.security.JwtAuthContext;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/matching")
@RequiredArgsConstructor
@Tag(name = "Match Groups", description = "Customer duplicate detection and merge")
public class MatchGroupController {

    private final MatchingService matchingService;
    private final JwtAuthContext authContext;

    @GetMapping("/groups")
    @PreAuthorize("hasAnyAuthority('customer:read', 'customer:merge', 'admin:config:read')")
    @Operation(summary = "Search match groups")
    public PageResponse<MatchGroupDto> search(MatchSearchRequest request) {
        return matchingService.search(request);
    }

    @GetMapping("/groups/{id}")
    @PreAuthorize("hasAnyAuthority('customer:read', 'customer:merge')")
    @Operation(summary = "Get match group by ID")
    public MatchGroupDto getById(@PathVariable UUID id) {
        return matchingService.getById(id);
    }

    @PostMapping("/run")
    @PreAuthorize("hasAnyAuthority('customer:merge', 'admin:config:write')")
    @Operation(summary = "Run matching for a customer")
    public ResponseEntity<List<MatchGroupDto>> findMatches(@Valid @RequestBody CustomerMatchRequest request) {
        return ResponseEntity.status(HttpStatus.OK).body(matchingService.findMatchesForCustomer(request));
    }

    @PostMapping("/batch")
    @PreAuthorize("hasAuthority('admin:config:write')")
    @Operation(summary = "Run batch matching")
    public ResponseEntity<MatchingEngine.BatchMatchResult> runBatch(@Valid @RequestBody MatchRequests.BatchMatchRequest request) {
        return ResponseEntity.status(HttpStatus.ACCEPTED).body(matchingService.runBatchMatching(request.batchSize()));
    }

    @PostMapping("/groups/{id}/assign")
    @PreAuthorize("hasAuthority('customer:merge')")
    @Operation(summary = "Assign match group to current user")
    public MatchGroupDto assignToMe(@PathVariable UUID id) {
        return matchingService.assignToMe(id, authContext.getUserId(), authContext.getFullName());
    }

    @PostMapping("/groups/{id}/merge")
    @PreAuthorize("hasAuthority('customer:merge')")
    @Operation(summary = "Merge match group")
    public MatchRequests.MergeResult merge(@PathVariable UUID id, @Valid @RequestBody MergeRequest request) {
        return matchingService.merge(id, request);
    }

    @PostMapping("/groups/{id}/reject")
    @PreAuthorize("hasAuthority('customer:merge')")
    @Operation(summary = "Reject match group")
    public MatchGroupDto reject(@PathVariable UUID id, @Valid @RequestBody RejectRequest request) {
        return matchingService.reject(id, request);
    }

    @PostMapping("/groups/{id}/escalate")
    @PreAuthorize("hasAuthority('customer:merge')")
    @Operation(summary = "Escalate match group")
    public MatchGroupDto escalate(@PathVariable UUID id, @Valid @RequestBody EscalateRequest request) {
        return matchingService.escalate(id, request);
    }

    @GetMapping("/stats")
    @PreAuthorize("hasAnyAuthority('customer:read', 'admin:config:read')")
    @Operation(summary = "Get matching statistics")
    public MatchRequests.MatchStatsResponse getStats() {
        return matchingService.getStats();
    }
}
