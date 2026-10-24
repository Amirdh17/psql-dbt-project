{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='appointment_id',
    )
}}

SELECT
    appointment_id,
    patient_id,
    provider_id,
    appointment_date,
    status,
    updated_at
FROM {{ ref('fact_appointments') }}

{% if is_incremental() %}

WHERE updated_at >= (
    SELECT COALESCE(
        MAX(updated_at),
        '1900-01-01'::TIMESTAMP
    )
    FROM {{ this }}
)

{% endif %}