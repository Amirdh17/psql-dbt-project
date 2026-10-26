WITH source AS (
    SELECT
        NULLIF(TRIM(referral_id), '') AS referral_id,
        NULLIF(TRIM(patient_id), '') AS patient_id,
        NULLIF(TRIM(referring_provider_id), '') AS referring_provider_id,
        NULLIF(TRIM(receiving_provider_id), '') AS receiving_provider_id,
        NULLIF(TRIM(referral_date), '') AS referral_date
    FROM {{ source('source', 'referrals') }}
)
SELECT DISTINCT
    referral_id,
    patient_id,
    referring_provider_id,
    receiving_provider_id,
    {{ standardize_date('referral_date') }} AS referral_date
FROM source
