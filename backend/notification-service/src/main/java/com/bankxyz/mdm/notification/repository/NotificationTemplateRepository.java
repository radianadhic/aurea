package com.bankxyz.mdm.notification.repository;

import com.bankxyz.mdm.common.repository.BaseRepository;
import com.bankxyz.mdm.notification.domain.NotificationTemplate;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface NotificationTemplateRepository extends BaseRepository<NotificationTemplate, UUID> {
    Optional<NotificationTemplate> findByCodeAndLocale(String code, String locale);
    Optional<NotificationTemplate> findByCodeAndLocaleAndActiveTrue(String code, String locale);
}
