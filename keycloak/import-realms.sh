#!/bin/bash
# =============================================================================
# Keycloak Realm Import Script
# =============================================================================
# Usage:
#   ./import-realms.sh [dev|prod]
#
# This script imports the realm configuration into Keycloak
# =============================================================================

set -e

ENV=${1:-dev}
REALM_FILE="realm-config-${ENV}.json"
KEYCLOAK_URL=${KEYCLOAK_URL:-http://localhost:8180}
KEYCLOAK_USER=${KEYCLOAK_ADMIN:-admin}
KEYCLOAK_PASSWORD=${KEYCLOAK_ADMIN_PASSWORD:-admin}

if [ ! -f "$REALM_FILE" ]; then
    echo "❌ Error: Realm file '$REALM_FILE' not found"
    echo ""
    echo "Available files:"
    ls -1 realm-config-*.json 2>/dev/null || echo "  (none)"
    echo ""
    echo "Usage: $0 [dev|prod]"
    exit 1
fi

echo "🔐 Importing Keycloak realm: $ENV"
echo "   Keycloak URL: $KEYCLOAK_URL"
echo "   Realm file:   $REALM_FILE"
echo ""

# Get admin token
echo "⏳ Getting admin access token..."
TOKEN=$(curl -s -X POST \
    "${KEYCLOAK_URL}/realms/master/protocol/openid-connect/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=${KEYCLOAK_USER}" \
    -d "password=${KEYCLOAK_PASSWORD}" \
    -d "grant_type=password" \
    -d "client_id=admin-cli" | jq -r .access_token)

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo "❌ Error: Failed to get admin token"
    echo "   Check KEYCLOAK_URL, KEYCLOAK_USER, KEYCLOAK_PASSWORD"
    exit 1
fi

# Check if realm already exists
REALM_NAME=$(jq -r .realm "$REALM_FILE")
echo "🔍 Checking if realm '$REALM_NAME' exists..."

REALM_EXISTS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer ${TOKEN}" \
    "${KEYCLOAK_URL}/admin/realms/${REALM_NAME}")

if [ "$REALM_EXISTS" = "200" ]; then
    echo "⚠️  Realm '$REALM_NAME' already exists. Updating..."
    
    # Update realm
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
        -X PUT \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        -d @"$REALM_FILE" \
        "${KEYCLOAK_URL}/admin/realms/${REALM_NAME}")
    
    if [ "$HTTP_CODE" = "204" ]; then
        echo "✅ Realm updated successfully"
    else
        echo "❌ Error: Realm update failed (HTTP $HTTP_CODE)"
        exit 1
    fi
else
    echo "➕ Creating new realm '$REALM_NAME'..."
    
    # Create realm
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        -d @"$REALM_FILE" \
        "${KEYCLOAK_URL}/admin/realms")
    
    if [ "$HTTP_CODE" = "201" ]; then
        echo "✅ Realm created successfully"
    else
        echo "❌ Error: Realm creation failed (HTTP $HTTP_CODE)"
        exit 1
    fi
fi

# Verify realm import
echo ""
echo "🧪 Verifying realm..."
REALM_INFO=$(curl -s -H "Authorization: Bearer ${TOKEN}" \
    "${KEYCLOAK_URL}/admin/realms/${REALM_NAME}")

if echo "$REALM_INFO" | jq -e . > /dev/null 2>&1; then
    USER_COUNT=$(echo "$REALM_INFO" | jq -r '.users | length // 0')
    CLIENT_COUNT=$(curl -s -H "Authorization: Bearer ${TOKEN}" \
        "${KEYCLOAK_URL}/admin/realms/${REALM_NAME}/clients" | jq -r 'length')
    ROLE_COUNT=$(echo "$REALM_INFO" | jq -r '.roles.realm | length')
    
    echo "✅ Realm '$REALM_NAME' is healthy"
    echo "   Clients:    $CLIENT_COUNT"
    echo "   Realm roles: $ROLE_COUNT"
else
    echo "❌ Error: Failed to verify realm"
    exit 1
fi

echo ""
echo "🎉 Realm import complete!"
echo ""
echo "Next steps:"
echo "  1. Visit Keycloak Admin Console: ${KEYCLOAK_URL}/admin"
echo "  2. Login with: ${KEYCLOAK_USER} / ${KEYCLOAK_PASSWORD}"
echo "  3. Select realm: $REALM_NAME"
echo "  4. Configure secrets (marked as REPLACE_WITH_SECURE_SECRET_FROM_VAULT)"
