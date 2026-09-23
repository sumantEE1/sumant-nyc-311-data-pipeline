{% macro get_resolution_hours(unit,created_date, closed_date) %}

    case 
        when {{ created_date }} is null then null
        when {{ closed_date }} is null then null
        when closed_date > created_date 
            then datediff({{unit}}, {{created_date}}, {{closed_date}})
        else null
    end

{% endmacro %}
