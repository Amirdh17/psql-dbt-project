-- Load Appoitments fact table 

-- Copy statement to load raw data from csv file
COPY stage.appointments (
    appointment_id,
    patient_id,
    provider_id,
    appointment_date,
    status,
    updated_at
)
FROM '/tmp/appointments.csv'
WITH (FORMAT CSV, HEADER TRUE);