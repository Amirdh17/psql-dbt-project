import llm_model

# Database schema provided to the LLM
SCHEMA = """
Table: publish.pub_dim_patients
description: contains patient information

Columns:
- patient_id (VARCHAR(20), Not Null, Unique)
- first_name (VARCHAR(200)): Patient's first name.
- last_name (VARCHAR(200)): Patient's last name.
- date_of_birth (DATE): Patient's date of birth.
- phone (VARCHAR(30)): Patient's contact phone number.
- zip (VARCHAR(15)): ZIP or postal code associated with the patient.
- created_date (DATE): Date on which the patient record was created.

Table: publish.pub_dim_providers
description: Contains healthcare provider information

Columns:
- provider_id (VARCHAR(20), Not Null): Identifier assigned to the healthcare provider. Multiple records may exist for a provider when role or effective-date history is maintained.
- npi (VARCHAR(10)): National Provider Identifier assigned to the healthcare provider.
- first_name (VARCHAR(200)): Provider's first name.
- last_name (VARCHAR(200)): Provider's last name.
- specialty (VARCHAR(100)): Medical specialty of the provider.
- role (VARCHAR(50)): Provider's role within the healthcare organization.
- effective_date (DATE): Date from which the provider record becomes effective.
- location (VARCHAR(100)): Clinic or location associated with the provider.

Table: publish.pub_fact_referrals
description: Incremental table contains referral events

Columns:
- referral_id (VARCHAR(20), Not Null, Unique): Unique identifier assigned to each referral event.
- patient_id (VARCHAR(20), Not Null): Identifier of the patient associated with the referral.
- referring_provider_id (VARCHAR(20)): Identifier of the provider initiating the referral.
- receiving_provider_id (VARCHAR(20)): Identifier of the provider receiving the referral.
- referral_date (DATE): Date on which the referral was made.

Table: publish.pub_fact_appointments
description: Incremental table containing appointment data. New and updated records are merged using appointment_id.
Columns:
- appointment_id (VARCHAR(20), Not Null): Unique identifier assigned to an appointment.
- patient_id (VARCHAR(20)): Identifier of the patient associated with the appointment.
- provider_id (VARCHAR(20)): Identifier of the provider associated with the appointment.
- appointment_date (DATE): Date on which the appointment is scheduled.
- status (VARCHAR(30), Not Null, Allowed Values: 'CANCELLED', 'NO_SHOW', 'COMPLETED', 'SCHEDULED'): Current status of the appointment.
- updated_at (TIMESTAMP): Timestamp indicating when the appointment record was last updated.

Relationships:
- pub_fact_appointments.patient_id -> pub_dim_patients.patient_id, many-to-one relationship.
- pub_fact_appointments.provider_id -> pub_dim_providers.provider_id, many-to-many relationship
- pub_fact_appointments.patient_id -> pub_fact_referrals.patient_id, many-to-many relationship
- pub_fact_appointments.provider_id -> pub_fact_referrals.provider_id, many-to-many relationship
- pub_fact_referrals.patient_id -> pub_dim_patients.patient_id, many-to-one relationship
- pub_fact_referrals.referring_provider_id -> pub_dim_providers.provider_id, many-to-one relationship
- pub_fact_referrals.receiving_provider_id -> pub_dim_providers.provider_id, many-to-one relationship
- pub_fact_referrals.receiving_provider_id -> pub_fact_appointments.provider_id, many-to-one relationship

Use PostgreSQL SQL supported syntax.
"""


def generate_sql(llm_model, question: str) -> str:
    """
        Convert the user's question into a PostgreSQL SELECT query.
    Args:
        llm model
        question: str
    Returns:
        query: str"""

    # llm_model = llm_model("cohere/north-mini-code:free", 0.2)

    prompt = f"""
You are a PostgreSQL expert answering questions about clinic referrals
and appointments.

Database schema:
{SCHEMA}

Rules:
1. Generate one read-only SELECT query.
2. Use only the tables and columns listed in the schema.
3. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, or other
   data-modifying statements.
4. Use appropriate JOIN, GROUP BY, date filtering, and aggregations.
5. If user's question not relevent to the schema and tables, you should provide empty string.
6. Avoid counting a referral multiple times when several appointments
   match it. Use EXISTS or COUNT(DISTINCT referral_id) as appropriate.
7. Return only SQL, without Markdown or explanations.

User question:
{question}
"""
    messages=[
                {
                    "role": "system",
                    "content": "Generate accurate, read-only PostgreSQL query."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
    response = llm_model.invoke(messages)

    sql = response.content.strip()

    return sql.rstrip(";")