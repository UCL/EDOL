-- ENUMS --
CREATE TYPE commodity_type AS ENUM ('elec', 'gas');
CREATE TYPE data_source_type AS ENUM ('cad', 'dcc', 'amr');
CREATE TYPE period_type AS ENUM ('day', 'week', 'month');
CREATE TYPE sensor_type AS ENUM ('temp', 'humidity');
CREATE TYPE sensor_units_type AS ENUM ('degc', 'percent');
CREATE TYPE ambient_type AS ENUM ('none', 'red', 'amber', 'green');
-- TABLES --
CREATE TABLE IF NOT EXISTS power_events (
    event_id UUID PRIMARY KEY,
    received TIMESTAMP_MS,
    cad_id STRING,
    commodity commodity_type,
    reading_timestamp TIMESTAMP,
    source data_source_type,
    reading FLOAT,
    ambient ambient_type,
    event_metadata JSON
);
CREATE TABLE IF NOT EXISTS temperature_events (
    event_id UUID PRIMARY KEY,
    cloud_received_timestamp TIMESTAMP,
    cad_id STRING,
    meter_update_timestamp TIMESTAMP,
    source data_source_type,
    reading INTEGER,
    units sensor_units_type,
    event_metadata JSON
);
CREATE TABLE IF NOT EXISTS humidity_events (
    event_id UUID PRIMARY KEY,
    cloud_received_timestamp TIMESTAMP,
    cad_id STRING,
    meter_update_timestamp TIMESTAMP,
    source data_source_type,
    reading INTEGER,
    units sensor_units_type,
    event_metadata JSON
);