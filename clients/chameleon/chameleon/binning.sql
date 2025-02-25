COPY (
    SELECT 
        to_timestamp(FLOOR(EXTRACT(EPOCH FROM COALESCE(t.cloud_received_timestamp, h.cloud_received_timestamp, p.received)) / 300) * 300) AS time_bucket,
        AVG(t.reading) AS avg_temperature,
        AVG(h.reading) AS avg_humidity,
        AVG(p.reading) AS avg_power
    FROM temperature_events t
    FULL OUTER JOIN humidity_events h ON t.cloud_received_timestamp = h.cloud_received_timestamp
    FULL OUTER JOIN power_events p ON COALESCE(t.cloud_received_timestamp, h.cloud_received_timestamp) = p.received
    GROUP BY time_bucket
    ORDER BY time_bucket
) TO 'output.csv' (HEADER, DELIMITER ',');