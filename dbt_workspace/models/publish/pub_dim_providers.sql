SELECT
    provider_id,
    npi,
    first_name,
    last_name,
    specialty,
    role,
    effective_date,
    location
FROM {{ ref('dim_providers') }}