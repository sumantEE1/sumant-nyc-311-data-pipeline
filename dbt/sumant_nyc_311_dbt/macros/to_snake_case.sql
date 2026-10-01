{% macro to_snake_case(column_expression) %}
    lower(
        regexp_replace(
            regexp_replace({{ column_expression }}, '([a-z])([A-Z])', $$\1_\2$$),
            '[^A-Za-z0-9]+',
            '_'
        )
    )
{% endmacro %}