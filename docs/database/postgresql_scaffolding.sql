-- create database
CREATE DATABASE amy WITH OWNER postgres;

-- create database user (read/write)
CREATE USER amy WITH
    LOGIN
    PASSWORD 'secret password'
    NOSUPERUSER
    INHERIT
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION
    VALID UNTIL 'infinity';

-- create database user (read/only)
CREATE USER amy_ro WITH
    LOGIN
    PASSWORD 'secret password'
    NOSUPERUSER
    INHERIT
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION
    VALID UNTIL 'infinity';

-- roles and permissions
GRANT TEMPORARY ON DATABASE amy TO amy;
GRANT TEMPORARY ON DATABASE amy TO amy_ro;
GRANT ALL ON DATABASE amy TO postgres;
GRANT amy TO postgres;
GRANT amy_ro TO postgres;

GRANT ALL ON SCHEMA public TO amy;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES to amy;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES to amy;

GRANT USAGE ON SCHEMA public TO amy_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO amy_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO amy_ro;
