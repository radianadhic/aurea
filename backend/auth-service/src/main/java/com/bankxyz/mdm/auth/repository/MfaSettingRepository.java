package com.bankxyz.mdm.auth.repository;

import com.bankxyz.mdm.auth.domain.MfaSetting;
import com.bankxyz.mdm.common.repository.BaseRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface MfaSettingRepository extends BaseRepository<MfaSetting, UUID> {

    Optional<MfaSetting> findByUserIdAndDeletedAtIsNull(UUID userId);

    Optional<MfaSetting> findByUsernameAndDeletedAtIsNull(String username);
}
