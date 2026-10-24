WITH source AS (

    SELECT
        TRIM(patient_id) AS patient_id,
        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,
        NULLIF(TRIM(date_of_birth), '') AS date_of_birth,
        NULLIF(TRIM(phone), '') AS phone,
        NULLIF(TRIM(zip), '') AS zip,
        NULLIF(TRIM(created_date), '') AS created_date

    FROM {{ source('stage', 'patients') }}

),

transformed AS (

    SELECT
        patient_id,
        first_name,
        last_name,
        {{ standardize_date('date_of_birth') }} AS date_of_birth,
        phone,
        zip,
        {{ standardize_date('created_date') }} AS created_date

    FROM source

)

SELECT *
FROM transformed