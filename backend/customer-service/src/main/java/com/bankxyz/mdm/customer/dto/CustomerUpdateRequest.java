package com.bankxyz.mdm.customer.dto;

import com.bankxyz.mdm.customer.domain.Customer;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Map;

@Schema(description = "Customer update request")
public record CustomerUpdateRequest(
    @Size(max = 200)
    @Schema(description = "Full name (individuals)")
    String fullName,

    @Size(max = 300)
    @Schema(description = "Legal name (corporates)")
    String legalName,

    @Schema(description = "Date of birth")
    LocalDate dateOfBirth,

    @Size(max = 100)
    @Schema(description = "Place of birth")
    String placeOfBirth,

    @Schema(description = "Gender")
    Customer.Gender gender,

    @Size(max = 3)
    @Schema(description = "Nationality (ISO code)")
    String nationality,

    @Schema(description = "Marital status")
    Customer.MaritalStatus maritalStatus,

    @Size(max = 20)
    @Schema(description = "Religion")
    String religion,

    @Size(max = 100)
    @Schema(description = "Occupation")
    String occupation,

    @DecimalMin("0")
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

    @Size(max = 20)
    @Schema(description = "Branch ID")
    String branchId,

    @Email
    @Schema(description = "Email")
    String email,

    @Pattern(regexp = "^(\\+62|0)8[0-9]{8,11}$")
    @Schema(description = "Mobile phone")
    String mobilePhone,

    @Schema(description = "Custom fields")
    Map<String, Object> customFields,

    @Schema(description = "Custom tags")
    String[] tags
) {}
