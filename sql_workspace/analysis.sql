WITH providers AS (
	SELECT DISTINCT 
		provider_id,
		first_name || ' ' || last_name AS provider_name 
	FROM publish.pub_dim_providers
),
referrals AS (
	SELECT 
		ref.referral_id,
		ref.referring_provider_id,
		ref.patient_id,
		ref.receiving_provider_id,
		pro.provider_name,
		DATE_TRUNC('month', ref.referral_date)::DATE AS referral_month,
		ref.referral_date
	FROM providers pro 
	LEFT JOIN publish.pub_fact_referrals ref 
	ON ref.referring_provider_id = pro.provider_id and ref.referral_date IS NOT NULL
),
total_referrals AS (
	SELECT 
		ref.referring_provider_id,
		ref.provider_name,
		ref.referral_month,
		count(ref.referral_id) AS total_referrals
	FROM referrals ref
	GROUP BY ref.referring_provider_id, ref.provider_name, referral_month
),
completed_referrals AS ( 
SELECT 
	ref.referring_provider_id,
	ref.provider_name,
	ref.referral_month,
	COUNT(referral_id) AS completed_referrals_in_30days
	
FROM referrals ref 
LEFT JOIN publish.pub_fact_appointments app 
	ON ref.patient_id = app.patient_id
	AND ref.receiving_provider_id = app.provider_id
	AND LOWER(app.status) = 'completed'
	AND app.appointment_date >= ref.referral_date
	AND app.appointment_date <= ref.referral_date + 30
GROUP BY ref.referring_provider_id,
	ref.provider_name,
	ref.referral_month
)
SELECT 
	ref.referring_provider_id,
	ref.provider_name,
	ref.referral_month,
	referral_id,
	count(*)
FROM referrals ref 
LEFT JOIN publish.pub_fact_appointments app 
	ON ref.patient_id = app.patient_id
	AND ref.receiving_provider_id = app.provider_id
	AND LOWER(app.status) = 'completed'
	AND app.appointment_date >= ref.referral_date
	AND app.appointment_date <= ref.referral_date + 30
GROUP BY ref.referring_provider_id,
	ref.provider_name,
	ref.referral_month,
	referral_id
HAVING count(*) > 1
/*
SELECT
	t_ref.referring_provider_id,
	t_ref.provider_name,
	t_ref.referral_month,
	completed_referrals_in_30days,
	total_referrals,
	ROUND(100 * completed_referrals_in_30days / NULLIF(total_referrals, 0), 2) AS completion_percentage
FROM total_referrals t_ref
LEFT JOIN completed_referrals c_ref
ON t_ref.referring_provider_id = c_ref.referring_provider_id 
	AND t_ref.provider_name = c_ref.provider_name
	AND t_ref.referral_month = c_ref.referral_month
ORDER BY referral_month
*/


