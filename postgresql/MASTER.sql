/*

    Master script for generating DB

    is_capped_supply =  ["consensus_and_emission"]["supply"]["is_capped_supply"]
    max_supply = ["consensus_and_emission"]["supply"]["max_supply"]
    genesis_block_date = ["economics"]["launch"]["initial_distribution"]["genesis_block_date "]

    New crypto asset
    1. Add to asset table

*/
/* ########################### DROP sequence ########################### */

DROP TRIGGER IF EXISTS asset_category_updated_at_stamp ON asset_category;
DROP TRIGGER IF EXISTS asset_updated_at_stamp ON asset;
DROP TRIGGER IF EXISTS historical_updated_at_stamp ON historical;
DROP TRIGGER IF EXISTS asset_tag_updated_at_stamp ON asset_tag;
DROP TRIGGER IF EXISTS asset_to_tag_updated_at_stamp ON asset_to_tag;


DROP TABLE IF EXISTS asset_to_tag;
DROP TABLE IF EXISTS asset_tag;
DROP TABLE IF EXISTS historical;
DROP TABLE IF EXISTS asset;
DROP TABLE IF EXISTS asset_category;

DROP FUNCTION IF EXISTS trg_updated_at();
DROP FUNCTION IF EXISTS now_utc();

/* ########################### FUNCTIONS ########################### */

-- Creates a function to get utc time

CREATE FUNCTION now_utc() RETURNS TIMESTAMP AS $$
  SELECT NOW() AT TIME ZONE 'utc';
$$ language sql;

-- Function used to generate trigger object for updated_at field in every table

CREATE FUNCTION trg_updated_at() RETURNS trigger AS $updated_stamp$
    BEGIN
        -- Remember who changed the payroll when
        NEW.updated_at := NOW_UTC();
        RETURN NEW;
    END;
$updated_stamp$ LANGUAGE plpgsql;

/* ########################### TABLES ########################### */

/* ###### CATEGORY TABLE ###### */

-- Create Table
CREATE TABLE IF NOT EXISTS asset_category (
    asset_category_id SERIAL PRIMARY KEY NOT NULL,
    asset_category_name varchar(20) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NULL
);

-- Create Trigger to Table
CREATE TRIGGER asset_category_updated_at_stamp BEFORE UPDATE ON asset_category
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();

INSERT INTO asset_category(asset_category_name)
VALUES
    ('crypto'),
    ('stock'),
    ('crypto-agg'),
    ('stock-agg'),
    ('precious-metal'),
    ('unknown');


/* ###### ASSET TABLE ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS asset (
    asset_id SERIAL PRIMARY KEY NOT NULL,
    asset_name varchar(50) UNIQUE NOT NULL,
    alternate_name varchar(50),
    symbol varchar(10) NOT NULL,
    asset_category_id integer REFERENCES asset_category(asset_category_id),
    short_description varchar(250) NULL,
    worked_at TIMESTAMP WITH TIME ZONE NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NULL
);
-- Create Trigger
CREATE TRIGGER asset_updated_at_stamp BEFORE UPDATE ON asset
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- Insert some data
INSERT INTO asset(asset_name, alternate_name, symbol, asset_category_id, short_description)
VALUES
    ('cryptocap10', 'top 10 cryptos', 'ccap10', 3, 'Composite tracker made of the top 10 crytocurrencies'),
    ('cryptocap20', 'top 20 cryptos', 'ccap20', 3, 'Composite tracker made of the top 20 crytocurrencies'),
    ('cryptocap30', 'top 30 cryptos', 'ccap30', 3, 'Composite tracker made of the top 30 crytocurrencies'),
    ('cryptocap50', 'top 50 cryptos', 'ccap50', 3, 'Composite tracker made of the top 50 crytocurrencies'),
    ('cryptocap100', 'top 100 cryptos', 'ccap100', 3, 'Composite tracker made of the top 100 crytocurrencies'),
    ('cryptocap200', 'top 200 cryptos', 'ccap200', 3, 'Composite tracker made of the top 200 crytocurrencies'),
    ('stockcap10', 'top 10 stocks', 'scap10', 4, 'Composite tracker made of the top 10 stocks'),
    ('stockcap20', 'top 20 stocks', 'scap20', 4, 'Composite tracker made of the top 20 stocks'),
    ('stockcap30', 'top 30 stocks', 'scap30', 4, 'Composite tracker made of the top 30 stocks'),
    ('S&P 500', 'Standard and Poor''s 500' , '^GSPC', 4, 'The flaming pile of shit');


/* ###### HISTORICAL ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS historical (
    historical_id SERIAL PRIMARY KEY NOT NULL,
    asset_id INTEGER REFERENCES asset(asset_id),
    open_price DECIMAL NOT NULL,
    high_price DECIMAL NOT NULL,
    low_price DECIMAL NOT NULL,
    close_price DECIMAL NOT NULL,
    circulating_supply DECIMAL NOT NULL,
    oustanding_marketcap DECIMAL NOT NULL,
    worked_at TIMESTAMP WITH TIME ZONE NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NULL
);
-- Create Trigger
CREATE TRIGGER historical_updated_at_stamp BEFORE UPDATE ON historical
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();


/* ###### TAGS ###### */
--Create Table
CREATE TABLE IF NOT EXISTS asset_tag(
    asset_tag_id SERIAL PRIMARY KEY NOT NULL,
    asset_tag_name varchar(30) NOT NULL,
    short_description VARCHAR(150) NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NULL
);
-- Create Trigger
CREATE TRIGGER asset_tag_updated_at_stamp BEFORE UPDATE ON asset_tag
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();

/* ###### ASSET TO TAG ###### */
--Create Table
CREATE TABLE IF NOT EXISTS asset_to_tag(
    asset_id INTEGER REFERENCES asset(asset_id),
    asset_tag_id INTEGER REFERENCES asset_tag(asset_tag_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NULL
);
-- Create Trigger
CREATE TRIGGER asset_to_tag_updated_at_stamp BEFORE UPDATE ON asset_to_tag
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();


-- /* ###### TAGS ###### */

-- CREATE TABLE IF NOT EXISTS asset_tag(
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
--     updated_at TIMESTAMP WITH TIME ZONE NULL

-- );

-- CREATE TABLE IF NOT EXISTS asset_tag(
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
--     updated_at TIMESTAMP WITH TIME ZONE NULL

-- );
-- CREATE TABLE IF NOT EXISTS asset_tag(
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW_UTC() NOT NULL,
--     updated_at TIMESTAMP WITH TIME ZONE NULL

-- );



/* ########################### DEPRECATED ###########################













*/