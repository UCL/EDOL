-- ENUMS --
CREATE TYPE commodity_type AS ENUM ('elec', 'gas');
CREATE TYPE data_source_type AS ENUM ('cad', 'dcc', 'amr');
CREATE TYPE period_type AS ENUM ('day', 'week', 'month');
CREATE TYPE sensor_type AS ENUM ('temp', 'humidity');
CREATE TYPE sensor_units_type AS ENUM ('degc', 'percent');
CREATE TYPE ambient_type AS ENUM ('none', 'red', 'amber', 'green');
-- TABLES --
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