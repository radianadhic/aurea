package com.bankxyz.mdm.common.repository;

import com.bankxyz.mdm.common.entity.BaseEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.NoRepositoryBean;
import org.springframework.data.repository.query.Param;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Base repository with common operations:
 * - Soft delete (instead of hard delete)
 * - Find including soft-deleted
 * - Bulk operations
 * - Audit trail queries
 *
 * All JPA repositories should extend this interface.
 */
@NoRepositoryBean
public interface BaseRepository<T extends BaseEntity, ID extends UUID>
        extends JpaRepository<T, ID>, JpaSpecificationExecutor<T> {

    /**
     * Find by ID, excluding soft-deleted entities
     */
    @Override
    @Query("SELECT e FROM #{#entityName} e WHERE e.id = :id AND e.deletedAt IS NULL")
    Optional<T> findById(@Param("id") ID id);

    /**
     * Find by ID, including soft-deleted entities
     */
    @Query("SELECT e FROM #{#entityName} e WHERE e.id = :id")
    Optional<T> findByIdIncludingDeleted(@Param("id") ID id);

    /**
     * Find all, excluding soft-deleted entities
     */
    @Override
    @Query("SELECT e FROM #{#entityName} e WHERE e.deletedAt IS NULL")
    List<T> findAll();

    /**
     * Find all with pagination, excluding soft-deleted entities
     */
    @Override
    @Query(value = "SELECT e FROM #{#entityName} e WHERE e.deletedAt IS NULL",
           countQuery = "SELECT count(e) FROM #{#entityName} e WHERE e.deletedAt IS NULL")
    Page<T> findAll(Pageable pageable);

    /**
     * Soft delete by ID
     */
    @Modifying
    @Query("UPDATE #{#entityName} e SET e.deletedAt = :now, e.updatedAt = :now WHERE e.id = :id AND e.deletedAt IS NULL")
    int softDeleteById(@Param("id") ID id, @Param("now") Instant now);

    /**
     * Restore soft-deleted entity
     */
    @Modifying
    @Query("UPDATE #{#entityName} e SET e.deletedAt = NULL, e.updatedAt = :now WHERE e.id = :id")
    int restoreById(@Param("id") ID id, @Param("now") Instant now);

    /**
     * Count excluding soft-deleted
     */
    @Override
    @Query("SELECT count(e) FROM #{#entityName} e WHERE e.deletedAt IS NULL")
    long count();

    /**
     * Count including soft-deleted
     */
    @Query("SELECT count(e) FROM #{#entityName} e")
    long countIncludingDeleted();

    /**
     * Check if exists and not soft-deleted
     */
    @Override
    @Query("SELECT CASE WHEN count(e) > 0 THEN true ELSE false END FROM #{#entityName} e WHERE e.id = :id AND e.deletedAt IS NULL")
    boolean existsById(@Param("id") ID id);
}
