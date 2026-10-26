SELECT a.*
FROM publish.pub_dim_patients p 
LEFT JOIN publish.pub_fact_appointments a 
ON p.patient_id = a.patient_id
WHERE p.first_name = 'Elena'
ORDER BY a.updated_at DESC
LIMIT 3;