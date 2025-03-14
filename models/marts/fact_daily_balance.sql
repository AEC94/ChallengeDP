{{
    config(
        materialized='incremental',
        unique_key='unique_id',
        incremental_strategy='append',
        on_schema_change='sync_all_columns',
        full_refresh=false
    )
}}

with invoices as (
    select
        current_date() as analyzed_date,
        organization_id,
        sum(amount * fx_rate) as invoiced_amount,
        sum(payment_amount * fx_rate_payment) as paid_amount,
        invoiced_amount - paid_amount as daily_balance
    from {{ ref('fact_invoices') }}
    where current_date > (select max(analyzed_date) from {{ this }})
    group by all

)

select
    {{ dbt_utils.generate_surrogate_key(['analyzed_date', 'organization_id']) }} as unique_id,
    analyzed_date,
    organization_id,
    coalesce(invoiced_amount,0) as invoiced_amount,
    coalesce(paid_amount,0) as paid_amount,
    coalesce(daily_balance, 0) as daily_balance
from invoices
