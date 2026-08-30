package com.bankxyz.mdm.customer.dto;

import com.bankxyz.mdm.customer.domain.Customer;
import io.swagger.v3.oas.annotations.media.Schema;

import java.math.BigDecimal;
import java.time.Instant;
import java.time.LocalDate;
import java.util.Map;
import java.util.UUID;

@Schema(description = "Customer (CIF) response")
public record CustomerResponse(
    @Schema(description = "Customer UUID")
    UUID id,

    @Schema(description = "CIF number", example = "CIF-2026-00000001")
    String cifNumber,

    @Schema(description = "Customer type")
    Customer.CustomerType customerType,

    @Schema(description = "Full name (individuals)")
    String fullName,

    @Schema(description = "Legal name (corporates)")
    String legalName,

    @Schema(description = "Date of birth")
    LocalDate dateOfBirth,

    @Schema(description = "Place of birth")
    String placeOfBirth,

    @Schema(description = "Gender")
    Customer.Gender gender,

    @Schema(description = "Nationality")
    String nationality,

    @Schema(description = "Marital status")
    Customer.MaritalStatus maritalStatus,

    @Schema(description = "Religion")
    String religion,

    @Schema(description = "Occupation")
    String occupation,

    @Schema(description = "Monthly income")
    BigDecimal monthlyIncome,

    @Schema(description = "KYC status")
    Customer.KycStatus kycStatus,

    @Schema(description = "KYC expiry date")
    LocalDate kycExpiryDate,

    @Schema(description = "Risk profile")
    Customer.RiskProfile riskProfile,

    @Schema(description = "PEP status")
    Boolean pepStatus,

    @Schema(description = "CIF status")
    Customer.CustomerStatus cifStatus,

    @Schema(description = "Branch ID")
    String branchId,

    @Schema(description = "Region code")
    String regionCode,

    @Schema(description = "Custom tags")
    String[] tags,

    @Schema(description = "Custom fields")
    Map<String, Object> customFields,

    @Schema(description = "Created timestamp")
    Instant createdAt,

    @Schema(description = "Created by")
    String createdBy,

    @Schema(description = "Last updated timestamp")
    Instant updatedAt,

    @Schema(description = "Last updated by")
    String updatedBy,

    @Schema(description = "Version (optimistic locking)")
    Long version
) {}
