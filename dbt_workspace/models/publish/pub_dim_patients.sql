SELECT
    patient_id,
    first_name,
    last_name,
    date_of_birth,
    phone,
    zip,
    created_date
FROM {{ ref('dim_patients') }}