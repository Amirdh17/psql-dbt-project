-- Load Providers dimensional tables 

-- Copy statement to load raw data from csv file
COPY stage.providers (
    provider_id,
    npi,
    first_name,
    last_name,
    specialty,
    role,
    effective_date,
    location
)
FROM '/tmp/providers.csv' 
WITH (FORMAT CSV, HEADER TRUE);