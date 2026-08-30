package com.bankxyz.mdm.customer.controller;

import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.customer.dto.CustomerCreateRequest;
import com.bankxyz.mdm.customer.dto.CustomerResponse;
import com.bankxyz.mdm.customer.dto.CustomerUpdateRequest;
import com.bankxyz.mdm.customer.service.CustomerService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;
import java.util.List;
import java.util.UUID;

/**
 * Customer (CIF) REST controller.
 * Provides full CRUD + search operations.
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/customers")
@RequiredArgsConstructor
@Tag(name = "Customers", description = "CIF (Customer Information File) management")
@SecurityRequirement(name = "bearerAuth")
public class CustomerController {

    private final CustomerService customerService;

    @PostMapping
    @PreAuthorize("hasAnyRole('SUPER_ADMIN', 'ADMIN', 'STEWARD_CIF')")
    @Operation(summary = "Create customer", description = "Create a new customer (CIF)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Customer created"),
        @ApiResponse(responseCode = "400", description = "Invalid input"),
        @ApiResponse(responseCode = "403", description = "Access denied"),
        @ApiResponse(responseCode = "422", description = "Business rule violation (e.g., age < 17)")
    })
    public ResponseEntity<CustomerResponse> createCustomer(@Valid @RequestBody CustomerCreateRequest request) {
        log.info("POST /api/v1/customers - fullName: {}", request.fullName());
        CustomerResponse response = customerService.createCustomer(request);
        URI location = UriComponentsBuilder
                .fromPath("/api/v1/customers/{id}")
                .buildAndExpand(response.id())
                .toUri();
        return ResponseEntity.created(location).body(response);
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('SUPER_ADMIN', 'ADMIN', 'STEWARD_CIF', 'ANALYST', 'AUDITOR', 'EXECUTIVE', 'BRANCH_MANAGER')")
    @Operation(summary = "Get customer by ID")
    public ResponseEntity<CustomerResponse> getCustomerById(
            @Parameter(description = "Customer UUID") @PathVariable UUID id) {
        return ResponseEntity.ok(customerService.getCustomerById(id));
    }

    @GetMapping("/cif/{cifNumber}")
    @PreAuthorize("hasAnyRole('SUPER_ADMIN', 'ADMIN', 'STEWARD_CIF', 'ANALYST', 'AUDITOR', 'EXECUTIVE', 'BRANCH_MANAGER')")
    @Operation(summary = "Get customer by CIF number")
    public ResponseEntity<CustomerResponse> getCustomerByCif(
            @Parameter(description = "CIF number", example = "CIF-2026-00000001")
            @PathVariable String cifNumber) {
        return ResponseEntity.ok(customerService.getCustomerByCif(cifNumber));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('SUPER_ADMIN', 'ADMIN', 'STEWARD_CIF')")
    @Operation(summary = "Update customer")
    public ResponseEntity<CustomerResponse> updateCustomer(
            @PathVariable UUID id,
            @Valid @RequestBody CustomerUpdateRequest request) {
        return ResponseEntity.ok(customerService.updateCustomer(id, request));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('SUPER_ADMIN')")
    @Operation(summary = "Delete customer (soft delete)", description = "Only SUPER_ADMIN can delete")
    public ResponseEntity<Void> deleteCustomer(
            @PathVariable UUID id,
            @Parameter(description = "Reason for deletion")
            @RequestParam(required = false) String reason) {
        customerService.deleteCustomer(id, reason != null ? reason : "Not specified");
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/search")
    @PreAuthorize("hasAnyRole('SUPER_ADMIN', 'ADMIN', 'STEWARD_CIF', 'ANALYST', 'BRANCH_MANAGER')")
    @Operation(summary = "Search customers by name")
    public ResponseEntity<PageResponse<CustomerResponse>> searchByName(
            @Parameter(description = "Search term (partial name match)")
            @RequestParam String q,

            @Parameter(description = "Page number (0-indexed)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "fullName")
            @RequestParam(defaultValue = "fullName") String sort,

            @Parameter(description = "Sort direction (ASC/DESC)")
            @RequestParam(defaultValue = "ASC") String direction) {

        Sort.Direction sortDir = Sort.Direction.fromString(direction);
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortDir, sort));
        return ResponseEntity.ok(customerService.searchByName(q, pageable));
    }

    @GetMapping("/kyc/expiring")
    @PreAuthorize("hasAnyRole('SUPER_ADMIN', 'ADMIN', 'STEWARD_CIF', 'COMPLIANCE')")
    @Operation(summary = "Get customers with expiring KYC")
    public ResponseEntity<List<CustomerResponse>> getExpiringKyc(
            @Parameter(description = "Days ahead to look for expiring KYC", example = "30")
            @RequestParam(defaultValue = "30") int days) {
        return ResponseEntity.ok(customerService.getCustomersWithExpiringKyc(days));
    }

    @GetMapping("/health")
    @Operation(summary = "Health check")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("UP - customer-service");
    }
}
