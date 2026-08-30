package com.bankxyz.mdm.notification.service;

import com.bankxyz.mdm.notification.domain.Notification;
import com.bankxyz.mdm.notification.domain.NotificationChannel;
import com.bankxyz.mdm.notification.domain.NotificationStatus;
import com.bankxyz.mdm.notification.domain.NotificationTemplate;
import com.bankxyz.mdm.notification.repository.NotificationRepository;
import com.bankxyz.mdm.notification.repository.NotificationTemplateRepository;
import com.bankxyz.mdm.common.exception.BusinessException;
import com.bankxyz.mdm.common.exception.ResourceNotFoundException;
import freemarker.template.Configuration;
import freemarker.template.Template;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.Optional;

/**
 * Email notification provider using JavaMailSender + FreeMarker templates.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class EmailNotificationProvider {

    private final JavaMailSender mailSender;
    private final NotificationRepository notificationRepository;
    private final NotificationTemplateRepository templateRepository;
    private final Configuration freemarkerConfig;

    @Value("${spring.mail.username:noreply@bankxyz.co.id}")
    private String fromAddress;

    @Value("${spring.mail.properties.mail.smtp.from.name:Bank XYZ}")
    private String fromName;

    @Async
    @Transactional
    public void send(Notification notification) {
        log.info("Sending email notification: {} to {}", notification.getId(), notification.getRecipientAddress());

        try {
            String subject = notification.getSubject();
            String body = notification.getBody();

            // Render template if template code is provided
            if (notification.getTemplateCode() != null) {
                Optional<NotificationTemplate> templateOpt = templateRepository
                    .findByCodeAndLocale(notification.getTemplateCode(), notification.getLocale());
                if (templateOpt.isPresent()) {
                    NotificationTemplate template = templateOpt.get();
                    if (template.getSubject() != null) {
                        subject = renderTemplate(template.getSubject(), notification.getVariables());
                    }
                    body = renderTemplate(template.getBody(), notification.getVariables());
                } else {
                    log.warn("Template not found: {}/{}", notification.getTemplateCode(), notification.getLocale());
                }
            }

            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, StandardCharsets.UTF_8.name());
            helper.setFrom(fromAddress, fromName);
            helper.setTo(notification.getRecipientAddress());
            helper.setSubject(subject);
            helper.setText(body, true);

            mailSender.send(message);

            notification.setStatus(NotificationStatus.SENT);
            notification.setSentAt(java.time.Instant.now());
            notification.setProviderMessageId(message.getMessageID());
            notificationRepository.save(notification);

            log.info("Email sent: {}", notification.getId());
        } catch (Exception e) {
            log.error("Failed to send email: {}", notification.getId(), e);
            notification.setStatus(NotificationStatus.FAILED);
            notification.setErrorMessage(e.getMessage());
            notification.setRetryCount(notification.getRetryCount() + 1);
            notificationRepository.save(notification);
        }
    }

    private String renderTemplate(String templateBody, Map<String, Object> variables) {
        try {
            Template template = new Template("inline", templateBody, freemarkerConfig);
            StringWriter writer = new StringWriter();
            template.process(variables != null ? variables : Map.of(), writer);
            return writer.toString();
        } catch (Exception e) {
            log.error("Template rendering failed", e);
            return templateBody;
        }
    }
}
