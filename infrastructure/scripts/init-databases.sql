-- =============================================
-- Init all 13 service databases
-- =============================================
-- This script runs on first postgres startup
-- Created automatically via docker-entrypoint-initdb.d

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create database user with limited privileges
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_user WHERE usename = 'mdm_user') THEN
    CREATE USER mdm_user WITH PASSWORD 'mdm_dev_password';
  END IF;
END$$;

-- Create all 13 service databases
SELECT 'CREATE DATABASE mdm_auth OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_auth')\gexec
SELECT 'CREATE DATABASE mdm_customer OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_customer')\gexec
SELECT 'CREATE DATABASE mdm_matching OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_matching')\gexec
SELECT 'CREATE DATABASE mdm_audit OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_audit')\gexec
SELECT 'CREATE DATABASE mdm_notification OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_notification')\gexec
SELECT 'CREATE DATABASE mdm_workflow OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_workflow')\gexec
SELECT 'CREATE DATABASE mdm_product OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_product')\gexec
SELECT 'CREATE DATABASE mdm_branch OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_branch')\gexec
SELECT 'CREATE DATABASE mdm_report OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_report')\gexec
SELECT 'CREATE DATABASE mdm_ml OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_ml')\gexec
SELECT 'CREATE DATABASE mdm_integration OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_integration')\gexec
SELECT 'CREATE DATABASE mdm_document OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_document')\gexec
SELECT 'CREATE DATABASE mdm_admin OWNER mdm_admin' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mdm_admin')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mdm_auth TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_customer TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_matching TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_audit TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_notification TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_workflow TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_product TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_branch TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_report TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_ml TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_integration TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_document TO mdm_user;
GRANT ALL PRIVILEGES ON DATABASE mdm_admin TO mdm_user;

-- Add comment
COMMENT ON DATABASE mdm_customer IS 'CIF (Customer Information File) database - core MDM data';
COMMENT ON DATABASE mdm_auth IS 'Authentication, session, MFA database';
COMMENT ON DATABASE mdm_audit IS 'Immutable audit log database (UU PDP compliance)';
