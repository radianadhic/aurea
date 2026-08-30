package com.bankxyz.mdm.customer.mapper;

import com.bankxyz.mdm.customer.domain.Customer;
import com.bankxyz.mdm.customer.dto.CustomerCreateRequest;
import com.bankxyz.mdm.customer.dto.CustomerResponse;
import com.bankxyz.mdm.customer.dto.CustomerUpdateRequest;
import org.springframework.stereotype.Component;

import java.util.UUID;

/**
 * Mapper between Customer entity and DTOs.
 * Manual mapping (vs MapStruct) for clarity and type safety.
 */
@Component
public class CustomerMapper {

    public Customer toEntity(CustomerCreateRequest request) {
        return Customer.builder()
                .id(UUID.randomUUID())
                .customerType(request.customerType())
                .fullName(request.fullName())
                .legalName(request.legalName())
                .dateOfBirth(request.dateOfBirth())
                .placeOfBirth(request.placeOfBirth())
                .gender(request.gender())
                .nationality(request.nationality() != null ? request.nationality() : "ID")
                .maritalStatus(request.maritalStatus())
                .religion(request.religion())
                .occupation(request.occupation())
                .monthlyIncome(request.monthlyIncome())
                .branchId(request.branchId())
                .kycStatus(Customer.KycStatus.PENDING)
                .cifStatus(Customer.CustomerStatus.ACTIVE)
                .pepStatus(false)
                .tags(request.tags())
                .customFields(request.customFields())
                .build();
    }

    public CustomerResponse toResponse(Customer customer) {
        return new CustomerResponse(
                customer.getId(),
                customer.getCifNumber(),
                customer.getCustomerType(),
                customer.getFullName(),
                customer.getLegalName(),
                customer.getDateOfBirth(),
                customer.getPlaceOfBirth(),
                customer.getGender(),
                customer.getNationality(),
                customer.getMaritalStatus(),
                customer.getReligion(),
                customer.getOccupation(),
                customer.getMonthlyIncome(),
                customer.getKycStatus(),
                customer.getKycExpiryDate(),
                customer.getRiskProfile(),
                customer.getPepStatus(),
                customer.getCifStatus(),
                customer.getBranchId(),
                customer.getRegionCode(),
                customer.getTags(),
                customer.getCustomFields(),
                customer.getCreatedAt(),
                customer.getCreatedBy(),
                customer.getUpdatedAt(),
                customer.getUpdatedBy(),
                customer.getVersion()
        );
    }

    public void updateEntity(Customer customer, CustomerUpdateRequest request) {
        if (request.fullName() != null) customer.setFullName(request.fullName());
        if (request.legalName() != null) customer.setLegalName(request.legalName());
        if (request.dateOfBirth() != null) customer.setDateOfBirth(request.dateOfBirth());
        if (request.placeOfBirth() != null) customer.setPlaceOfBirth(request.placeOfBirth());
        if (request.gender() != null) customer.setGender(request.gender());
        if (request.nationality() != null) customer.setNationality(request.nationality());
        if (request.maritalStatus() != null) customer.setMaritalStatus(request.maritalStatus());
        if (request.religion() != null) customer.setReligion(request.religion());
        if (request.occupation() != null) customer.setOccupation(request.occupation());
        if (request.monthlyIncome() != null) customer.setMonthlyIncome(request.monthlyIncome());
        if (request.kycStatus() != null) customer.setKycStatus(request.kycStatus());
        if (request.kycExpiryDate() != null) customer.setKycExpiryDate(request.kycExpiryDate());
        if (request.riskProfile() != null) customer.setRiskProfile(request.riskProfile());
        if (request.pepStatus() != null) customer.setPepStatus(request.pepStatus());
        if (request.cifStatus() != null) customer.setCifStatus(request.cifStatus());
        if (request.branchId() != null) customer.setBranchId(request.branchId());
        if (request.tags() != null) customer.setTags(request.tags());
        if (request.customFields() != null) customer.setCustomFields(request.customFields());
    }
}
