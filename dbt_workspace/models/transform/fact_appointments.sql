WITH source AS (
    SELECT
        NULLIF(TRIM(appointment_id), '') AS appointment_id,
        NULLIF(TRIM(patient_id), '') AS patient_id,
        NULLIF(TRIM(provider_id), '') AS provider_id,
        NULLIF(TRIM(appointment_date), '') AS appointment_date,
        NULLIF(TRIM(status), '') AS status,
        NULLIF(TRIM(updated_at), '') AS updated_at
    FROM {{ source('source', 'appointments') }}
)

SELECT DISTINCT
    appointment_id,
    patient_id,
    provider_id,
    {{ standardize_date('appointment_date') }} AS appointment_date,
    {{ standardize_app_status('status') }} AS status,
    CAST(
        NULLIF(updated_at, '') AS TIMESTAMP
    ) AS updated_at
FROM source