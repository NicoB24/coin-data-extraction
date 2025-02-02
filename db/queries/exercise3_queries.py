"""
select coin, EXTRACT(MONTH FROM date) AS month , AVG(price) as average_price
from coin_data cd
group by coin, month
order by coin, average_price desc;
"""

"""
with consecutive_price_drop as (
    select
        coin,
        date,
        price,
        CAST((json->'market_data'->'market_cap'->>'usd') AS numeric) AS market_cap_usd,
        case
            when LAG(price, 1) over (partition by coin order by date) > price then 1
            else 0
        end as drop
    from coin_data
),
consecutive_price_drop_groups AS (
    SELECT
        coin,
        date,
        price,
        market_cap_usd,
        SUM(drop) OVER (PARTITION BY coin ORDER BY date) AS drop_group
    FROM consecutive_price_drop
)
select
    coin,
    AVG(price) as avg_price_increase,
    MAX(market_cap_usd) as current_market_cap
from consecutive_price_drop_groups
group by coin, drop_group
having COUNT(*) >= 3;
"""
