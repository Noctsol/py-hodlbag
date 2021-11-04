SELECT 
    cry.crypto_id,
    cry.crypto_name AS "name",
    cry.alternate_name AS "alt_name",
    cry.symbol,
    cry.details,
    cat.category_name,
    cs.crypto_status_name,
    cry.created_at,
    cry.updated_at
FROM crypto AS cry
    INNER JOIN crypto_status AS cs ON cs.crypto_status_id = cry.crypto_status_id
    INNER JOIN category AS cat ON cat.category_id = cry.category_id