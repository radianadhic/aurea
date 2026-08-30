package com.bankxyz.mdm.notification;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;

@SpringBootApplication(scanBasePackages = {
    "com.bankxyz.mdm.notification",
    "com.bankxyz.mdm.common"
})
@EnableJpaAuditing
@EnableKafka
@EnableAsync
@EnableScheduling
@OpenAPIDefinition(
    info = @Info(
        title = "MDM Notification Service API",
        version = "1.0.0",
        description = "Multi-channel notifications (email, SMS, WhatsApp, push, in-app)",
        contact = @Contact(name = "MDM Team", email = "mdm@bankxyz.co.id")
    )
)
public class NotificationServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(NotificationServiceApplication.class, args);
    }
}
