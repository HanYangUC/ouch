-- Create Database if not exists
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'testouch') THEN
        CREATE DATABASE testouch;
    END IF;
END$$;


-- Connect to the Database
\c testouch;

-- Create User
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'hy') THEN
        CREATE USER hy WITH PASSWORD 'hy';
    END IF;
END$$;

ALTER ROLE hy SET client_encoding TO 'utf8';
ALTER ROLE hy SET default_transaction_isolation TO 'read committed';
ALTER ROLE hy SET timezone TO 'UTC';

-- Grant Privileges
GRANT ALL PRIVILEGES ON DATABASE testouch TO hy;
