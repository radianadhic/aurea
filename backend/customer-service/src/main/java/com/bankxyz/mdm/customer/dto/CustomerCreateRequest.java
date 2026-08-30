package com.bankxyz.mdm.customer.dto;

import com.bankxyz.mdm.customer.domain.Customer;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Map;

@Schema(description = "Customer creation request")
public record CustomerCreateRequest(
    @NotNull
    @Schema(description = "Customer type")
    Customer.CustomerType customerType,

    @Size(max = 200)
    @Schema(description = "Full name (for individuals)", example = "Budi Setiawan")
    String fullName,

    @Size(max = 300)
    @Schema(description = "Legal name (for corporates)", example = "PT Maju Mundur Sentosa")
    String legalName,

    @Past
    @Schema(description = "Date of birth (individuals only)", example = "1985-03-15")
    LocalDate dateOfBirth,

    @Size(max = 100)
    @Schema(description = "Place of birth", example = "Jakarta")
    String placeOfBirth,

    @Schema(description = "Gender (MALE, FEMALE)")
    Customer.Gender gender,

    @Size(min = 2, max = 3)
    @Schema(description = "Nationality (ISO 3166-1 alpha-2 or alpha-3)", example = "ID")
    String nationality,

    @Schema(description = "Marital status")
    Customer.MaritalStatus maritalStatus,

    @Size(max = 20)
    @Schema(description = "Religion", example = "ISLAM")
    String religion,

    @Size(max = 100)
    @Schema(description = "Occupation", example = "Software Engineer")
    String occupation,

    @DecimalMin("0")
    @Schema(description = "Monthly income in IDR", example = "25000000")
    BigDecimal monthlyIncome,

    @Size(max = 20)
    @Schema(description = "Branch ID", example = "KCU-JKT-001")
    String branchId,

    @Email
    @Size(max = 200)
    @Schema(description = "Email", example = "budi.setiawan@example.com")
    String email,

    @Pattern(regexp = "^(\\+62|0)8[0-9]{8,11}$")
    @Schema(description = "Mobile phone", example = "+6281234567001")
    String mobilePhone,

    @Schema(description = "Custom fields (extensibility)")
    Map<String, Object> customFields,

    @Schema(description = "Custom tags")
    String[] tags
) {}
