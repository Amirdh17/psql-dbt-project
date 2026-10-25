{% macro standardize_app_status(column_name) %}

    CASE
        WHEN LOWER(
            REGEXP_REPLACE(TRIM({{ column_name }}), '[-_ ]+', '', 'g')
        ) = 'noshow'
            THEN 'NO_SHOW'

        WHEN LOWER(TRIM({{ column_name }})) IN ('completed', 'complete')
            THEN 'COMPLETED'

        WHEN LOWER(TRIM({{ column_name }})) IN ('cancelled', 'canceled')
            THEN 'CANCELLED'

        WHEN LOWER(TRIM({{ column_name }})) = 'scheduled'
            THEN 'SCHEDULED'

        ELSE NULL
    END

{% endmacro %}