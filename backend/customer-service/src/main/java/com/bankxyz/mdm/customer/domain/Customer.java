package com.bankxyz.mdm.customer.domain;

import com.bankxyz.mdm.common.entity.BaseEntity;
import io.hypersistence.utils.hibernate.type.json.JsonBinaryType;
import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;
import org.hibernate.annotations.Type;

import java.time.LocalDate;
import java.util.Map;
import java.util.UUID;

/**
 * Customer (CIF - Customer Information File) entity.
 * Core entity that represents a single customer in the system.
 *
 * Customer types:
 * - INDIVIDUAL: Natural person (personal banking)
 * - CORPORATE: Legal entity (business banking)
 * - SYARIAH: Sharia-compliant banking customer
 */
@Entity
@Table(name = "customers", indexes = {
    @Index(name = "idx_customers_cif_number", columnList = "cif_number", unique = true),
    @Index(name = "idx_customers_full_name", columnList = "full_name"),
    @Index(name = "idx_customers_status", columnList = "cif_status"),
    @Index(name = "idx_customers_branch", columnList = "branch_id"),
    @Index(name = "idx_customers_kyc_status", columnList = "kyc_status, kyc_expiry_date"),
    @Index(name = "idx_customers_risk", columnList = "risk_profile"),
    @Index(name = "idx_customers_created", columnList = "created_at DESC")
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@SuperBuilder
public class Customer extends BaseEntity {

    @Column(name = "cif_number", nullable = false, unique = true, length = 30)
    private String cifNumber;

    @Enumerated(EnumType.STRING)
    @Column(name = "customer_type", nullable = false, length = 20)
    private CustomerType customerType;

    // For individuals
    @Column(name = "full_name", length = 200)
    private String fullName;

    @Column(name = "legal_name", length = 300)
    private String legalName;

    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;

    @Column(name = "place_of_birth", length = 100)
    private String placeOfBirth;

    @Enumerated(EnumType.STRING)
    @Column(name = "gender", length = 10)
    private Gender gender;

    @Column(name = "nationality", length = 3)
    private String nationality;  // ISO 3166-1 alpha-3 (ID, SG, MY, etc)

    @Enumerated(EnumType.STRING)
    @Column(name = "marital_status", length = 20)
    private MaritalStatus maritalStatus;

    @Column(name = "religion", length = 20)
    private String religion;

    @Column(name = "occupation", length = 100)
    private String occupation;

    @Column(name = "monthly_income", precision = 18, scale = 2)
    private java.math.BigDecimal monthlyIncome;

    // KYC
    @Enumerated(EnumType.STRING)
    @Column(name = "kyc_status", nullable = false, length = 20)
    private KycStatus kycStatus;

    @Column(name = "kyc_expiry_date")
    private LocalDate kycExpiryDate;

    @Enumerated(EnumType.STRING)
    @Column(name = "risk_profile", length = 10)
    private RiskProfile riskProfile;

    @Column(name = "pep_status", nullable = false)
    private Boolean pepStatus;  // Politically Exposed Person

    // Status
    @Enumerated(EnumType.STRING)
    @Column(name = "cif_status", nullable = false, length = 20)
    private CustomerStatus cifStatus;

    // Location
    @Column(name = "branch_id", length = 20)
    private String branchId;

    @Column(name = "region_code", length = 20)
    private String regionCode;

    // Metadata
    @Type(JsonBinaryType.class)
    @Column(name = "tags", columnDefinition = "jsonb")
    private String[] tags;  // Custom tags (PREMIUM, VIP, etc)

    @Type(JsonBinaryType.class)
    @Column(name = "custom_fields", columnDefinition = "jsonb")
    private Map<String, Object> customFields;

    @PrePersist
    public void prePersist() {
        if (kycStatus == null) kycStatus = KycStatus.PENDING;
        if (cifStatus == null) cifStatus = CustomerStatus.ACTIVE;
        if (pepStatus == null) pepStatus = false;
    }

    public enum CustomerType { INDIVIDUAL, CORPORATE, SYARIAH }
    public enum Gender { MALE, FEMALE }
    public enum MaritalStatus { SINGLE, MARRIED, DIVORCED, WIDOWED }
    public enum KycStatus { PENDING, IN_REVIEW, APPROVED, REJECTED, EXPIRED, FAILED }
    public enum RiskProfile { LOW, MEDIUM, HIGH }
    public enum CustomerStatus { ACTIVE, DORMANT, CLOSED, BLACKLIST, DECEASED, SUSPENDED }
}
