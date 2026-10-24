-- Create Schema following schemas: stage, load, transform, publish for medallion architecture

CREATE SCHEMA IF NOT EXISTS stage;
CREATE SCHEMA IF NOT EXISTS load;
CREATE SCHEMA IF NOT EXISTS transform;
CREATE SCHEMA IF NOT EXISTS publish;