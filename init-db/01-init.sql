-- Initialize dbt Analytics Database
-- This script runs automatically when PostgreSQL container starts

-- Create schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;
CREATE SCHEMA IF NOT EXISTS seeds;

-- Grant permissions to dbt user
GRANT ALL PRIVILEGES ON SCHEMA staging TO dbt_user;
GRANT ALL PRIVILEGES ON SCHEMA marts TO dbt_user;
GRANT ALL PRIVILEGES ON SCHEMA seeds TO dbt_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO dbt_user;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Log initialization
SELECT 'dbt Analytics database initialized successfully' AS status;
