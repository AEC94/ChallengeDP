{{
    config(
        materialized='incremental',
        unique_key='organization_id',
        incremental_strategy='delete+insert',
        on_schema_change='sync_all_columns'
    )
}}

with source as (
    select
        organization_id,
        first_payment_date,
        last_payment_date,
        legal_entity_country_code,
        created_date,
        updated_date
    from {{ ref('stg_organizations') }} 

    {% if is_incremental() %}
        where coalesce(updated_date,created_date) > (select max(created_date) from {{ this }})
    {% endif %}
),

final as (
    select
        organization_id,
        first_payment_date,
        last_payment_date,
        legal_entity_country_code,
        created_date,
        updated_date,
        current_localtimestamp() as loaded_at
    from source
)

select * from final
