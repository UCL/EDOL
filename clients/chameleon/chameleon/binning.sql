COPY (
    WITH power_data AS (
        SELECT time_bucket(INTERVAL '{interval}', reading_timestamp) AS bucket,
            cad_id,
            ROUND(AVG(reading), 3) AS power_avg,
            COUNT(*) AS power_event_count,
            MIN(reading) AS power_min,
            MAX(reading) AS power_max
        FROM power_events
        WHERE reading_timestamp >= '{start_time}'
            AND reading_timestamp < '{end_time}'
            AND commodity = 'elec'
        GROUP BY bucket,
            cad_id
    ),
    temperature_data AS (
        SELECT time_bucket(INTERVAL '{interval}', meter_update_timestamp) AS bucket,
            cad_id,
            ROUND(AVG(reading), 3) AS temperature_avg,
            COUNT(*) AS temperature_event_count,
            MIN(reading) AS temperature_min,
            MAX(reading) AS temperature_max
        FROM temperature_events
        WHERE meter_update_timestamp >= '{start_time}'
            AND meter_update_timestamp < '{end_time}'
        GROUP BY bucket,
            cad_id
    ),
    humidity_data AS (
        SELECT time_bucket(INTERVAL '{interval}', meter_update_timestamp) AS bucket,
            cad_id,
            ROUND(AVG(reading), 3) AS humidity_avg,
            COUNT(*) AS humidity_event_count,
            MIN(reading) AS humidity_min,
            MAX(reading) AS humidity_max
        FROM humidity_events
        WHERE meter_update_timestamp >= '{start_time}'
            AND meter_update_timestamp < '{end_time}'
        GROUP BY bucket,
            cad_id
    )
    SELECT power_data.bucket AS bucket,
        power_data.cad_id AS cad_id,
        power_avg,
        temperature_avg,
        humidity_avg,
        power_event_count,
        temperature_event_count,
        humidity_event_count,
        power_min,
        temperature_min,
        humidity_min,
        power_max,
        temperature_max,
        humidity_max
    FROM power_data
        LEFT JOIN temperature_data ON power_data.bucket = temperature_data.bucket
        AND power_data.cad_id = temperature_data.cad_id
        LEFT JOIN humidity_data ON power_data.bucket = humidity_data.bucket
        AND power_data.cad_id = humidity_data.cad_id
    ORDER BY bucket,
        cad_id
) TO '{output_file}' WITH CSV HEADER;
