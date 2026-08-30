package com.bankxyz.mdm.customer.repository;

import com.bankxyz.mdm.common.repository.BaseRepository;
import com.bankxyz.mdm.customer.domain.Customer;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface CustomerRepository extends BaseRepository<Customer, UUID> {

    @Query("SELECT c FROM Customer c WHERE c.cifNumber = :cifNumber AND c.deletedAt IS NULL")
    Optional<Customer> findByCifNumber(@Param("cifNumber") String cifNumber);

    @Query("SELECT c FROM Customer c WHERE c.fullName ILIKE %:name% AND c.deletedAt IS NULL ORDER BY c.fullName")
    Page<Customer> searchByName(@Param("name") String name, Pageable pageable);

    @Query("SELECT c FROM Customer c WHERE c.cifStatus = :status AND c.deletedAt IS NULL ORDER BY c.createdAt DESC")
    Page<Customer> findByStatus(@Param("status") Customer.CustomerStatus status, Pageable pageable);

    @Query("SELECT c FROM Customer c WHERE c.branchId = :branchId AND c.deletedAt IS NULL ORDER BY c.fullName")
    Page<Customer> findByBranchId(@Param("branchId") String branchId, Pageable pageable);

    @Query("SELECT c FROM Customer c WHERE c.kycStatus = 'APPROVED' AND c.kycExpiryDate < :now AND c.deletedAt IS NULL")
    List<Customer> findCustomersWithExpiringKyc(@Param("now") LocalDate now);

    @Query("SELECT count(c) FROM Customer c WHERE c.branchId = :branchId AND c.deletedAt IS NULL")
    long countByBranchId(@Param("branchId") String branchId);

    @Query("SELECT count(c) FROM Customer c WHERE c.riskProfile = :risk AND c.deletedAt IS NULL")
    long countByRiskProfile(@Param("risk") Customer.RiskProfile risk);

    @Query("SELECT count(c) FROM Customer c WHERE c.kycStatus = :status AND c.deletedAt IS NULL")
    long countByKycStatus(@Param("status") Customer.KycStatus status);
}
