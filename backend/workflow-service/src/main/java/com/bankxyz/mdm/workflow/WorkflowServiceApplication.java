package com.bankxyz.mdm.workflow;

import org.camunda.bpm.spring.boot.starter.annotation.EnableProcessApplication;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.scheduling.annotation.EnableAsync;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;

@SpringBootApplication(scanBasePackages = {
    "com.bankxyz.mdm.workflow",
    "com.bankxyz.mdm.common"
})
@EnableProcessApplication
@EnableJpaAuditing
@EnableKafka
@EnableAsync
@OpenAPIDefinition(
    info = @Info(
        title = "MDM Workflow Service API",
        version = "1.0.0",
        description = "BPMN workflow with 4-eyes approval, task assignment, SLAs",
        contact = @Contact(name = "MDM Team", email = "mdm@bankxyz.co.id")
    )
)
public class WorkflowServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(WorkflowServiceApplication.class, args);
    }
}
