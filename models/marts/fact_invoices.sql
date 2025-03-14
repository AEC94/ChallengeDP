{{
    config(
        materialized='incremental',
        unique_key='invoice_id',
        incremental_strategy='delete+insert',
        on_schema_change='sync_all_columns'
    )
}}

with source as (
    select
        invoice_id,
        parent_invoice_id,
        transaction_id,
        organization_id,
        type,
        status,
        currency,
        payment_currency,
        payment_method,
        amount,
        payment_amount,
        fx_rate,
        fx_rate_payment,
        created_at,
        created_date,
        updated_at
    from {{ ref('stg_invoices') }}
    {% if is_incremental() %}
        where coalesce(updated_at,created_at) > (select max(created_at) from {{ this }})
    {% endif %}
),

final as (
    select
        invoice_id,
        parent_invoice_id,
        transaction_id,
        organization_id,
        type,
        status,
        currency,
        payment_currency,
        payment_method,
        amount,
        payment_amount,
        fx_rate,
        fx_rate_payment,
        created_at,
        created_date,
        updated_at,
        current_localtimestamp() as loaded_at
    from source
)

select * from final