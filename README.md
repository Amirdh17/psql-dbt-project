### Clinical Data Pipeline
- Followed medallion architecture with stage, transform and publish schema within warehouse database.
- Created stage, transform, and publish schemas and created tables in stage schema for patient, providers, referrals and appointments.
- Loaded raw csv data into the stage layer tables.
- setup the dbt environment to establish connection to PostgreSQL.
- Defined stage layer tables as sources in models/source.yml file.
- Created the following models to apply required transformations: dim_patients, dim_providers, fact_referrals, fact_appointments.
- Faced data issue with date columns which contains multiple formats in a column. So created standardize_date macro to manage it.
- Faced data issue with status column in fact_appointments table. So, created standardize_app_status macro to manage it.
- Created the following models to validate and load data publish schema: pub_dim_patients, pub_dim_providers, pub_fact_referrals, pub_fact_appointments.
- Built Incremental flow for pub_fact_referrals and pub_fact_appointments tables.
- Applied unique, not_null, relationship and accepted_values data tests for required columns.

### GenAI application
- Created the following python files app.py (main), execute_sql.py, generate_sql.py and generate_answer.sql.
- generate_sql has llm_model which can receive user question and write sql query if user's question can be converted into query.
- execute_sql establish connection to PostgreSQL and can execute the query.
- generate_answer connects to llm model and passes the user question, generated sql and sql results. Then llm model gives the answer approriate to the given prompt.
