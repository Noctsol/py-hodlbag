/*

Create the primary asset table that every is driven off of

*/
DROP TRIGGER IF EXISTS asset_updated_at_stamp ON asset;
 DROP TABLE IF exists asset;
 DROP FUNCTION IF EXISTS trg_updated_at();
 

CREATE TABLE IF NOT EXISTS asset (
    asset_id SERIAL PRIMARY KEY NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NULL,
    worked_at TIMESTAMP WITH TIME ZONE NULL

	-- floatNum DECIMAL NULL,  -- float, also referred to as NUMERIC
	-- entryCount SERIAL NOT NULL, -- will auto increment, useful for auto entering entries without PK
	-- tinyInt SMALLINT NULL, -- integer but smaller space allocation, probably use when making FK fields
	-- price MONEY NULL, -- use to represent money, fix to 2 decimals, probably best used in SELECT
	-- isReal BOOLEAN DEFAULT true NOT NULL,
	-- variableText varchar(200) DEFAULT 'This is a test',
	-- unlimitedText TEXT DEFAULT 'UNENDING',   -- I think the equivalent of varchar max?
	-- current_mood mood DEFAULT 'sad' NOT NULL,	-- references ENUM. How to updade enum????? Can types be refd globally?
	-- insertTime TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() ,
	-- insertzTime TIMESTAMP WITH TIME ZONE DEFAULT NOW() ,
	-- squareArray INTEGER[][] DEFAULT '{{1,2,3},{4,5,6},{7,8,9}}',	-- ARRAY
	-- inventoryItem inventory_item DEFAULT ('fuzzy dice', 42, 1.99),  -- COMPOSITE aka JSON/class objects
	-- dtRange tsrange DEFAULT '[2010-01-01 14:30, 2010-01-01 15:30)', -- WHAT EVEN
	-- intRange int4range DEFAULT '[1, 6]'
);


CREATE FUNCTION trg_updated_at() RETURNS trigger AS $updated_stamp$
    BEGIN


        -- Remember who changed the payroll when
        NEW.updated_at := NOW_UTC();
        RETURN NEW;
    END;
$updated_stamp$ LANGUAGE plpgsql;

CREATE TRIGGER asset_updated_at_stamp BEFORE INSERT OR UPDATE ON asset
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();