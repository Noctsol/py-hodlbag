-- These will exist glovally as types to reference. bruh
--CREATE TYPE  mood AS ENUM  ('sad', 'ok', 'happy');
/*CREATE TYPE inventory_item AS (
    name            text,
    supplier_id     integer,
    price           numeric
);*/

DROP TABLE IF exists test_types;

CREATE TABLE IF NOT EXISTS test_types (
    mainId SERIAL PRIMARY KEY NOT NULL,
	floatNum DECIMAL NULL,  -- float, also referred to as NUMERIC
	entryCount SERIAL NOT NULL, -- will auto increment, useful for auto entering entries without PK
	tinyInt SMALLINT NULL, -- integer but smaller space allocation, probably use when making FK fields
	price MONEY NULL, -- use to represent money, fix to 2 decimals, probably best used in SELECT
	isReal BOOLEAN DEFAULT true NOT NULL,
	variableText varchar(200) DEFAULT 'This is a test',
	unlimitedText TEXT DEFAULT 'UNENDING',   -- I think the equivalent of varchar max?
	current_mood mood DEFAULT 'sad' NOT NULL,	-- references ENUM. How to updade enum????? Can types be refd globally?
	insertTime TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() ,
	insertzTime TIMESTAMP WITH TIME ZONE DEFAULT NOW() ,
	squareArray INTEGER[][] DEFAULT '{{1,2,3},{4,5,6},{7,8,9}}',	-- ARRAY
	inventoryItem inventory_item DEFAULT ('fuzzy dice', 42, 1.99),  -- COMPOSITE aka JSON/class objects
	dtRange tsrange DEFAULT '[2010-01-01 14:30, 2010-01-01 15:30)', -- WHAT EVEN
	intRange int4range DEFAULT '[1, 6]'	  
);