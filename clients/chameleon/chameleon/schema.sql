-- ENUMS --
CREATE TYPE commodity_type AS ENUM ('elec', 'gas');
CREATE TYPE data_source_type AS ENUM ('cad', 'dcc', 'amr');
CREATE TYPE period_type AS ENUM ('day', 'week', 'month');
CREATE TYPE units_type AS ENUM ('Wh', 'l');
CREATE TYPE sensor_type AS ENUM ('temp', 'humidity');
CREATE TYPE sensor_units_type AS ENUM ('degc', 'percent');
CREATE TYPE ambient_type AS ENUM ('none', 'red', 'amber', 'green');
-- TABLES --
CREATE TABLE meter_events (
    event_id UUID PRIMARY KEY,
    received TIMESTAMP_MS,
    cad_id VARCHAR,
    commodity commodity_type,
    reading_timestamp TIMESTAMP_MS,
    source data_source_type,
    units units_type,
    reading BIGINT,
    event_metadata JSON
);
CREATE TABLE power_events (
    event_id UUID PRIMARY KEY,
    received TIMESTAMP_MS,
    cad_id VARCHAR,
    commodity commodity_type,
    reading_timestamp TIMESTAMP_MS,
    source data_source_type,
    reading BIGINT,
    ambient ambient_type,
    event_metadata JSON
);
CREATE TABLE cumulative_events (
    event_id UUID PRIMARY KEY,
    cloud_received_timestamp TIMESTAMP_MS,
    cad_id VARCHAR,
    period_start_timestamp TIMESTAMP_MS,
    meter_update_timestamp TIMESTAMP_MS,
    period period_type,
    source data_source_type,
    commodity commodity_type,
    consumption INTEGER,
    consumption_units units_type,
    cost INTEGER,
    cost_exponent INTEGER,
    currency INTEGER,
    event_metadata JSON
);
CREATE TABLE sensor_events (
    event_id UUID PRIMARY KEY,
    cloud_received_timestamp TIMESTAMP_MS,
    cad_id VARCHAR,
    meter_update_timestamp TIMESTAMP_MS,
    type sensor_type,
    reading INTEGER,
    source data_source_type,
    units sensor_units_type,
    event_metadata JSON
);
CREATE TABLE half_hour_events (
    event_id UUID PRIMARY KEY,
    cloud_received_timestamp TIMESTAMP_MS,
    device_id VARCHAR,
    period_start_timestamp TIMESTAMP_MS,
    commodity commodity_type,
    source data_source_type,
    consumption INTEGER,
    consumption_units units_type,
    cost INTEGER,
    cost_exponent INTEGER,
    currency INTEGER,
    event_metadata JSON
);