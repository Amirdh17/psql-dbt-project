-- Load Referrals dimensional tables 

-- Copy statement to load raw data from csv file
COPY stage.referrals (
    referral_id,
    patient_id,
    referring_provider_id,
    receiving_provider_id,
    referral_date
) 
FROM '/tmp/referrals.csv' 
WITH (FORMAT CSV, HEADER TRUE);
