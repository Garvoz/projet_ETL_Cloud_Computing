with source as (
    select * from {{ source('mini_projet_dbt', 'raw_customers') }}
),
renamed as (
    select
        id as customer_id,
        name as customer_name
    from source
)
select * from renamed