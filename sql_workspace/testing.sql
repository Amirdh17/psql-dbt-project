SELECT 
	ref.referral_id, ref.referral_date, app.status, app.appointment_date 
FROM publish.pub_fact_referrals ref 
LEFT JOIN publish.pub_fact_appointments app 
ON ref.patient_id = app.patient_id 
	and ref.receiving_provider_id = app.provider_id 
WHERE ref.referral_id = 'R000645';