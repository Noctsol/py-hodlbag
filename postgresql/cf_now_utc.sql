
-- Creates a function to get utc 
CREATE FUNCTION NOW_UTC() RETURNS TIMESTAMP AS $$
  SELECT NOW() AT TIME ZONE 'utc';
$$ language sql;