-- Create Database if not exists
CREATE DATABASE IF NOT EXISTS testouch;

-- Connect to the Database
\c testouch;

-- Create User
CREATE USER hy WITH PASSWORD 'hy';
ALTER ROLE hy SET client_encoding TO 'utf8';
ALTER ROLE hy SET default_transaction_isolation TO 'read committed';
ALTER ROLE hy SET timezone TO 'UTC';

-- Grant Privileges
GRANT ALL PRIVILEGES ON DATABASE testouch TO hy;
