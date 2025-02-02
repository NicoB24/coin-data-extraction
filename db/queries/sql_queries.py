insert_coin_data = """
    INSERT INTO coin_data (coin_id, price_usd, date, json_response)
    VALUES (:coin_id, :price_usd, :date, :json_response);
"""

insert_aggregated_data_from_coin_data = """
    DELETE FROM aggregated_data WHERE coin_id = :coin_id;

    INSERT INTO aggregated_data (coin_id, year, month, max_value, min_value)
    SELECT
        cd.coin_id,
        EXTRACT(YEAR FROM cd.date) AS year,
        EXTRACT(MONTH FROM cd.date) AS month,
        MAX(cd.price_usd) AS max_value,
        MIN(cd.price_usd) AS min_value
    FROM
        coin_data cd
    WHERE
        cd.coin_id = :coin_id
    GROUP BY
        cd.coin_id,
        EXTRACT(YEAR FROM cd.date),
        EXTRACT(MONTH FROM cd.date)
"""
