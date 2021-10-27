select  asset_id
,created_at
,updated_at
,worked_at
from public.asset
LIMIT 1000;

INSERT INTO asset(worked_at)
VALUES (timestamp '2021-10-26 21:02:57');