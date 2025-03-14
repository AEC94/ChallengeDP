{{
    config(
        materialized='view'
    )
}}
with source as (
    select
        -- Primary key
        try_cast(organization_id as bigint) as organization_id,
        
        -- Date fields
        try_cast(first_payment_date as date) as first_payment_date,
        try_cast(last_payment_date as date) as last_payment_date,
        
        -- Properties
        try_cast(legal_entity_country_code as bigint) as legal_entity_country_code,
        try_cast(count_total_contracts_active as bigint) as count_total_contracts_active,
        
        -- Timestamps
        try_cast(created_date as timestamp) as created_date,
        -- I'd request this to be added
        current_date() as updated_date
    from {{ source('db','organizations') }} 
),

final as (
    select
        organization_id,
        first_payment_date,
        last_payment_date,
        legal_entity_country_code,
        count_total_contracts_active,
        created_date,
        updated_date
    from source
)

select * from final
