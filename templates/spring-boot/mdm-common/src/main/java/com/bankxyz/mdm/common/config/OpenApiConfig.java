package com.bankxyz.mdm.common.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.ExternalDocumentation;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.servers.Server;
import io.swagger.v3.oas.models.tags.Tag;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

/**
 * OpenAPI 3.0 configuration.
 * Provides:
 * - API metadata (title, version, description, contact)
 * - Multiple server URLs (dev, staging, prod)
 * - OAuth2 security scheme (Keycloak JWT)
 * - Common tags
 */
@Configuration
public class OpenApiConfig {

    @Value("${spring.application.name}")
    private String serviceName;

    @Value("${spring.application.name:default-service}")
    private String applicationName;

    @Value("${server.port:8080}")
    private String serverPort;

    @Bean
    public OpenAPI customOpenAPI() {
        final String securitySchemeName = "bearerAuth";

        return new OpenAPI()
                .info(new Info()
                        .title(toTitleCase(serviceName) + " API")
                        .description("MDM Bank XYZ - " + toTitleCase(serviceName) + " REST API. " +
                                "All endpoints require OAuth2 JWT authentication via Keycloak.")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("MDM Bank XYZ Team")
                                .email("mdm-team@bankxyz.co.id")
                                .url("https://mdm.bankxyz.co.id"))
                        .license(new License()
                                .name("Bank XYZ Internal License")
                                .url("https://bankxyz.co.id/license")))
                .externalDocs(new ExternalDocumentation()
                        .description("MDM Bank XYZ Documentation")
                        .url("https://docs.mdm.bankxyz.co.id"))
                .servers(List.of(
                        new Server().url("http://localhost:" + serverPort).description("Local development"),
                        new Server().url("https://dev-api.mdm.bankxyz.co.id").description("Development"),
                        new Server().url("https://stg-api.mdm.bankxyz.co.id").description("Staging"),
                        new Server().url("https://api.mdm.bankxyz.co.id").description("Production")))
                .components(new Components()
                        .addSecuritySchemes(securitySchemeName, new SecurityScheme()
                                .name(securitySchemeName)
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("bearer")
                                .bearerFormat("JWT")
                                .description("JWT token from Keycloak (Authorization: Bearer <token>)"))
                        .addSecuritySchemes("oauth2", new SecurityScheme()
                                .type(SecurityScheme.Type.OAUTH2)
                                .description("OAuth2 authentication via Keycloak")
                                .flows(new io.swagger.v3.oas.models.security.OAuthFlows()
                                        .authorizationCode(new io.swagger.v3.oas.models.security.OAuthFlow()
                                                .authorizationUrl("https://keycloak.mdm.bankxyz.co.id/realms/mdm-dev/protocol/openid-connect/auth")
                                                .tokenUrl("https://keycloak.mdm.bankxyz.co.id/realms/mdm-dev/protocol/openid-connect/token")
                                                .refreshUrl("https://keycloak.mdm.bankxyz.co.id/realms/mdm-dev/protocol/openid-connect/token")
                                                .scopes(new io.swagger.v3.oas.models.security.Scopes()
                                                        .addString("openid", "OpenID Connect")
                                                        .addString("email", "Email scope")
                                                        .addString("profile", "Profile scope")
                                                        .addString("roles", "Realm roles"))))))
                .addSecurityItem(new SecurityRequirement().addList(securitySchemeName).addList("oauth2"))
                .tags(List.of(
                        new Tag().name("Authentication").description("Login, logout, token operations"),
                        new Tag().name("Customers").description("CIF (Customer Information File) management"),
                        new Tag().name("Workflows").description("Approval workflow & task management"),
                        new Tag().name("Audit").description("Audit log & compliance"),
                        new Tag().name("Admin").description("User, role, permission management")));
    }

    private String toTitleCase(String camelCase) {
        if (camelCase == null || camelCase.isEmpty()) return "";
        StringBuilder result = new StringBuilder();
        result.append(Character.toUpperCase(camelCase.charAt(0)));
        for (int i = 1; i < camelCase.length(); i++) {
            char c = camelCase.charAt(i);
            if (Character.isUpperCase(c)) {
                result.append(' ');
            }
            result.append(c);
        }
        return result.toString();
    }
}
