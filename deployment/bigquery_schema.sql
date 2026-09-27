-- BigQuery Analytics Dataset Schema for CLEANAIR AI
CREATE SCHEMA IF NOT EXISTS `cleanair_ai_analytics`;

-- 1. Pollution Observations Table
CREATE TABLE IF NOT EXISTS `cleanair_ai_analytics.pollution_observations` (
    observation_id STRING NOT NULL,
    station_id STRING NOT NULL,
    city STRING NOT NULL,
    country STRING,
    timestamp TIMESTAMP NOT NULL,
    aqi INT64 NOT NULL,
    category STRING,
    pm25 FLOAT64,
    pm10 FLOAT64,
    no2 FLOAT64,
    o3 FLOAT64,
    so2 FLOAT64,
    co FLOAT64,
    primary_pollutant STRING,
    source STRING
)
PARTITION BY DATE(timestamp)
CLUSTER BY city, station_id;

-- 2. Alert Events Log Table
CREATE TABLE IF NOT EXISTS `cleanair_ai_analytics.alert_events` (
    alert_id STRING NOT NULL,
    user_id STRING NOT NULL,
    city STRING NOT NULL,
    severity STRING NOT NULL,
    trigger_reason STRING,
    metric_name STRING,
    measured_value FLOAT64,
    threshold_value FLOAT64,
    timestamp TIMESTAMP NOT NULL,
    recommended_action STRING
)
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, city;

-- 3. Agent Execution Audit Log
CREATE TABLE IF NOT EXISTS `cleanair_ai_analytics.agent_execution_logs` (
    session_id STRING NOT NULL,
    correlation_id STRING NOT NULL,
    agent_name STRING NOT NULL,
    task_name STRING NOT NULL,
    tool_used STRING,
    latency_ms FLOAT64,
    timestamp TIMESTAMP NOT NULL
)
PARTITION BY DATE(timestamp);
