/*

    Master script for generating DB

*/


-- ########################### FUNCTIONS ###########################

-- Creates a function to get utc 
CREATE FUNCTION NOW_UTC() RETURNS TIMESTAMP AS $$
  SELECT NOW() AT TIME ZONE 'utc';
$$ language sql;

-- Function used to generate trigger object for updated_at field in every table
DROP FUNCTION IF EXISTS trg_updated_at();
CREATE FUNCTION trg_updated_at() RETURNS trigger AS $updated_stamp$
    BEGIN
        -- Remember who changed the payroll when
        NEW.updated_at := NOW_UTC();
        RETURN NEW;
    END;
$updated_stamp$ LANGUAGE plpgsql;

-- ########################### TABLES ###########################

-- ###### CATEGORY TABLE ######

DROP TRIGGER IF EXISTS asset_category_updated_at_stamp ON asset_category;
DROP TABLE IF exists asset_category;

-- Create Table
CREATE TABLE IF NOT EXISTS asset_category (
    id SERIAL PRIMARY KEY NOT NULL,
    pname varchar(20) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NULL
);

-- Create Trigger to Table
CREATE TRIGGER asset_category_updated_at_stamp BEFORE INSERT OR UPDATE ON asset_category
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();


-- ###### ASSET TABLE ######


DROP TRIGGER IF EXISTS asset_updated_at_stamp ON asset;
DROP TABLE IF exists asset;

 

CREATE TABLE IF NOT EXISTS asset (
    id SERIAL PRIMARY KEY NOT NULL,
    pname varchar(50) UNIQUE NOT NULL,
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


CREATE TRIGGER asset_updated_at_stamp BEFORE INSERT OR UPDATE ON asset
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
