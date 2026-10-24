{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='referral_id',
    )
}}

SELECT
    referral_id,
    patient_id,
    referring_provider_id,
    receiving_provider_id,
    referral_date
FROM {{ ref('fact_referrals') }}

{% if is_incremental() %}

WHERE referral_id NOT IN (
    SELECT referral_id
    FROM {{ this }}
)

{% endif %}