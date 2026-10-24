WITH source AS (
    SELECT
        TRIM(provider_id) AS provider_id,
        NULLIF(TRIM(npi), '') AS npi,
        NULLIF(TRIM(first_name), '') AS first_name,
        NULLIF(TRIM(last_name), '') AS last_name,
        NULLIF(TRIM(specialty), '') AS specialty,
        NULLIF(TRIM(role), '') AS role,
        NULLIF(TRIM(effective_date), '') AS effective_date,
        NULLIF(TRIM(location), '') AS location
    FROM {{ source('source', 'providers') }}
),

transformed AS (
    SELECT DISTINCT
        provider_id,
        npi,
        first_name,
        last_name,
        specialty,
        role,
        {{ standardize_date('effective_date') }} AS effective_date,
        location
    FROM source
)

SELECT *
FROM transformed