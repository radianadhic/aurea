package com.bankxyz.mdm.customer.service;

import com.bankxyz.mdm.common.dto.PageResponse;
import com.bankxyz.mdm.common.exception.BusinessException;
import com.bankxyz.mdm.common.exception.ResourceNotFoundException;
import com.bankxyz.mdm.common.security.JwtAuthContext;
import com.bankxyz.mdm.customer.domain.Customer;
import com.bankxyz.mdm.customer.dto.CustomerCreateRequest;
import com.bankxyz.mdm.customer.dto.CustomerResponse;
import com.bankxyz.mdm.customer.dto.CustomerUpdateRequest;
import com.bankxyz.mdm.customer.mapper.CustomerMapper;
import com.bankxyz.mdm.customer.repository.CustomerRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Customer (CIF) service.
 * Core business logic for customer lifecycle management.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class CustomerService {

    private final CustomerRepository customerRepository;
    private final CustomerMapper customerMapper;
    private final CustomerEventPublisher eventPublisher;

    private static final AtomicLong CIF_SEQUENCE = new AtomicLong(0);

    /**
     * Create a new customer.
     * Generates CIF number, validates, saves, publishes event.
     */
    @Transactional
    @CacheEvict(value = "customers", allEntries = true)
    public CustomerResponse createCustomer(CustomerCreateRequest request) {
        log.info("Creating customer: {} ({})", request.fullName(), request.customerType());

        // 1. Validate business rules
        validateCustomerCreation(request);

        // 2. Map to entity
        Customer customer = customerMapper.toEntity(request);
        customer.setCifNumber(generateCifNumber());
        customer.setCreatedBy(JwtAuthContext.getCurrentUsername().orElse("system"));

        // 3. Save
        Customer saved = customerRepository.save(customer);

        // 4. Publish event
        eventPublisher.publishCustomerCreated(saved);

        log.info("Customer created: {} (CIF: {})", saved.getId(), saved.getCifNumber());
        return customerMapper.toResponse(saved);
    }

    /**
     * Get customer by ID.
     */
    @Transactional(readOnly = true)
    @Cacheable(value = "customer-by-cif", key = "#id")
    public CustomerResponse getCustomerById(UUID id) {
        log.debug("Getting customer by ID: {}", id);
        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> ResourceNotFoundException.forResource("Customer", id));
        return customerMapper.toResponse(customer);
    }

    /**
     * Get customer by CIF number.
     */
    @Transactional(readOnly = true)
    @Cacheable(value = "customer-by-cif", key = "#cifNumber")
    public CustomerResponse getCustomerByCif(String cifNumber) {
        log.debug("Getting customer by CIF: {}", cifNumber);
        Customer customer = customerRepository.findByCifNumber(cifNumber)
                .orElseThrow(() -> new ResourceNotFoundException(
                        String.format("Customer with CIF '%s' not found", cifNumber)));
        return customerMapper.toResponse(customer);
    }

    /**
     * Update customer.
     */
    @Transactional
    @CacheEvict(value = {"customers", "customer-by-cif"}, allEntries = true)
    public CustomerResponse updateCustomer(UUID id, CustomerUpdateRequest request) {
        log.info("Updating customer: {}", id);

        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> ResourceNotFoundException.forResource("Customer", id));

        customerMapper.updateEntity(customer, request);
        customer.setUpdatedBy(JwtAuthContext.getCurrentUsername().orElse("system"));

        Customer saved = customerRepository.save(customer);
        eventPublisher.publishCustomerUpdated(saved);

        log.info("Customer updated: {}", id);
        return customerMapper.toResponse(saved);
    }

    /**
     * Soft delete customer.
     */
    @Transactional
    @CacheEvict(value = {"customers", "customer-by-cif"}, allEntries = true)
    public void deleteCustomer(UUID id, String reason) {
        log.info("Deleting customer: {} (reason: {})", id, reason);

        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> ResourceNotFoundException.forResource("Customer", id));

        // Only super_admin can delete
        if (!JwtAuthContext.hasRole("SUPER_ADMIN")) {
            throw BusinessException.forbidden("Only SUPER_ADMIN can delete customers");
        }

        customer.markDeleted();
        customer.setUpdatedBy(JwtAuthContext.getCurrentUsername().orElse("system"));
        customerRepository.save(customer);

        eventPublisher.publishCustomerDeleted(customer);
        log.info("Customer soft-deleted: {}", id);
    }

    /**
     * Search customers by name (paginated).
     */
    @Transactional(readOnly = true)
    public PageResponse<CustomerResponse> searchByName(String name, Pageable pageable) {
        log.debug("Searching customers by name: {}", name);
        Page<Customer> page = customerRepository.searchByName(name, pageable);
        List<CustomerResponse> content = page.getContent().stream()
                .map(customerMapper::toResponse)
                .toList();
        return PageResponse.<CustomerResponse>builder()
                .content(content)
                .page(page.getNumber())
                .size(page.getSize())
                .totalElements(page.getTotalElements())
                .totalPages(page.getTotalPages())
                .first(page.isFirst())
                .last(page.isLast())
                .build();
    }

    /**
     * Get customers with expiring KYC.
     */
    @Transactional(readOnly = true)
    public List<CustomerResponse> getCustomersWithExpiringKyc(int daysAhead) {
        LocalDate expiryThreshold = LocalDate.now().plusDays(daysAhead);
        return customerRepository.findCustomersWithExpiringKyc(expiryThreshold)
                .stream()
                .map(customerMapper::toResponse)
                .toList();
    }

    // ============================================================
    // PRIVATE HELPERS
    // ============================================================

    private void validateCustomerCreation(CustomerCreateRequest request) {
        // Age validation (must be >= 17)
        if (request.dateOfBirth() != null) {
            int age = LocalDate.now().getYear() - request.dateOfBirth().getYear();
            if (age < 17) {
                throw BusinessException.unprocessable("AGE_TOO_YOUNG",
                        "Customer must be at least 17 years old");
            }
            if (age > 120) {
                throw BusinessException.unprocessable("AGE_INVALID",
                        "Customer age is invalid");
            }
        }
        // Email format validation
        if (request.email() != null && !request.email().matches("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")) {
            throw BusinessException.unprocessable("EMAIL_INVALID",
                    "Email format is invalid");
        }
    }

    private String generateCifNumber() {
        long seq = CIF_SEQUENCE.incrementAndGet();
        String year = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy"));
        return String.format("CIF-%s-%08d", year, seq);
    }
}
