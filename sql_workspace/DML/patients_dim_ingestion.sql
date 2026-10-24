-- Load Patients dimensional table

-- Copy statement to load raw data from csv file
COPY stage.patients (
    patient_id,
    first_name,
    last_name,
    date_of_birth,
    phone,
    zip,
    created_date
)
FROM '/tmp/patients.csv'
WITH (FORMAT CSV, HEADER TRUE);
