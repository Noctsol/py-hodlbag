SELECT 
    cry.crypto_id,
    cry.crypto_name AS "name",
    cry.alternate_name AS "alt_name",
    cry.symbol,
    cry.details,
    ccat.ccategory_name,
    csta.cstatus_name,
    cry.created_at,
    cry.updated_at
FROM crypto AS cry
    INNER JOIN cstatus AS csta ON csta.cstatus_id = cry.cstatus_id
    INNER JOIN ccategory AS ccat ON ccat.ccategory_id = cry.ccategory_id