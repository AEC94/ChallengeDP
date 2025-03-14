{{
    config(
        materialized='view'
    )
}}

with source as (
    select
        -- Keys
        try_cast(invoice_id as bigint) as invoice_id,
        try_cast(parent_invoice_id as bigint) as parent_invoice_id,
        try_cast(transaction_id as bigint) as transaction_id,
        try_cast(organization_id as bigint) as organization_id,
        
         -- Properties
        try_cast(type as bigint) as type,
        trim(upper(status)) as status,
        trim(upper(currency)) as currency,
        trim(upper(payment_currency)) as payment_currency,
        trim(upper(payment_method)) as payment_method,

        -- Amounts
        try_cast(amount as double) as amount,
        try_cast(payment_amount as double) as payment_amount,
        try_cast(fx_rate as double) as fx_rate,
        try_cast(fx_rate_payment as double) as fx_rate_payment,

        -- Timestamps
        try_cast(created_at as timestamp) as created_at,
        try_cast(created_at as date) as created_date,
        -- I'd request this to be added
        current_localtimestamp() as updated_at
    from {{ source('db', 'invoices') }}
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
        updated_at
    from source
)

select * from final