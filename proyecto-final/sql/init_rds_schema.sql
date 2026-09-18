-- Esquema de RDS para mi Proyecto Integrador
-- Ejecutar una sola vez en DBeaver, conectado a la instancia RDS a la que se nos dio acceso.
-- Creamos la base de datos propia del proyecto y la tabla de metadata que usa
-- el notebook 06 (06_sync_metadatos_rds.ipynb) para sincronizar los JSON
-- que genera la Lambda y el backfill.
--
-- Las 7 tablas gold_* (KPIs de la capa Gold) NO se crean aqui: las genera
-- automaticamente pandas (to_sql con if_exists="replace") cada vez que
-- corre el notebook 05_export_rds.ipynb.

CREATE DATABASE IF NOT EXISTS proyecto_integrador_alan
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE proyecto_integrador_alan;

CREATE TABLE IF NOT EXISTS pipeline_metadata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    s3_bucket VARCHAR(255) NOT NULL,
    s3_key VARCHAR(500) NOT NULL,
    taxi_type VARCHAR(20) NOT NULL,
    file_year INT NOT NULL,
    file_month INT NOT NULL,
    file_size_bytes BIGINT,
    num_rows BIGINT,
    registered_by VARCHAR(100),
    registered_at DATETIME,
    UNIQUE KEY uq_s3_key (s3_key)
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id INT AUTO_INCREMENT PRIMARY KEY,
    notebook_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    started_at DATETIME,
    finished_at DATETIME,
    error_message TEXT
);
