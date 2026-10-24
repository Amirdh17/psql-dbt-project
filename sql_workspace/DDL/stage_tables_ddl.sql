-- stage layer DDLs

-- patients table
CREATE TABLE IF NOT EXISTS stage.patients (
    patient_id      TEXT,
    first_name      TEXT,
    last_name       TEXT,
    date_of_birth   TEXT,
    phone           TEXT,
    zip             TEXT,
    created_date    TEXT
);

-- Referrals table
CREATE TABLE IF NOT EXISTS stage.referrals (
    referral_id             TEXT,
    patient_id              TEXT,
    referring_provider_id   TEXT,
    receiving_provider_id   TEXT,
    referral_date           TEXT
);

-- providers
CREATE TABLE IF NOT EXISTS stage.providers (
    provider_id     TEXT,
    npi             TEXT,
    first_name      TEXT,
    last_name       TEXT,
    specialty       TEXT,
    role            TEXT,
    effective_date  TEXT,
    location        TEXT
);

-- Appointments table 
CREATE TABLE IF NOT EXISTS stage.appointments (
    appointment_id   TEXT,
    patient_id       TEXT,
    provider_id      TEXT,
    appointment_date TEXT,
    status           TEXT,
    updated_at       TEXT
);