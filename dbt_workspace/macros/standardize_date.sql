{% macro standardize_date(column_name) %}

    CASE
        -- Format: YYYY-MM-DD
        WHEN {{ column_name }} ~ '^\d{4}-\d{2}-\d{2}$'
            THEN TO_DATE({{ column_name }}, 'YYYY-MM-DD')

        -- Format: MM/DD/YYYY
        WHEN {{ column_name }} ~ '^\d{2}/\d{2}/\d{4}$'
            THEN TO_DATE({{ column_name }}, 'MM/DD/YYYY')

        -- Format: DD-Mon-YYYY
        WHEN {{ column_name }} ~ '^\d{2}-[A-Za-z]{3}-\d{4}$'
            THEN TO_DATE({{ column_name }}, 'DD-Mon-YYYY')

        ELSE NULL
    END

{% endmacro %}