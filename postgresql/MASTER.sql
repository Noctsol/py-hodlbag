/*

    Master script for generating DB

    is_capped_supply =  ["consensus_and_emission"]["supply"]["is_capped_supply"]
    max_supply = ["consensus_and_emission"]["supply"]["max_supply"]

    genesis_block_date = ["economics"]["launch"]["initial_distribution"]["genesis_block_date "]
    token_distribution_date = ["economics"]["launch"]["initial_distribution"]["token_distribution_date "]

    New crypto asset
    1. Add new crypto to asset table
    2. Mark as new status
    3. Add genesis block if available as inception
    4. 

*/
/* ########################### DROP sequence ########################### */

DROP TRIGGER IF EXISTS updated_at_stamp_crypto_status ON crypto_status;
DROP TRIGGER IF EXISTS updated_at_stamp_category ON category;
DROP TRIGGER IF EXISTS updated_at_stamp_crypto ON crypto;
DROP TRIGGER IF EXISTS updated_at_stamp_historical ON historical;
DROP TRIGGER IF EXISTS updated_at_stamp_tag ON tag;
DROP TRIGGER IF EXISTS updated_at_stamp_crypto_to_tag ON crypto_to_tag;
DROP TRIGGER IF EXISTS updated_at_stamp_crypto_profile ON crypto_profile;

DROP TABLE IF EXISTS crypto_profile;
DROP TABLE IF EXISTS crypto_to_tag;
DROP TABLE IF EXISTS historical;
DROP TABLE IF EXISTS crypto;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS crypto_status;
DROP TABLE IF EXISTS tag;

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
CREATE TABLE IF NOT EXISTS category (
    category_id SERIAL PRIMARY KEY NOT NULL,
    category_name varchar(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger to Table
CREATE TRIGGER updated_at_stamp_category BEFORE UPDATE ON category
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- Insert
INSERT INTO category(category_name) 
VALUES
    ('crypto'),
    ('crypto-agg'),
    ('unknown');


/* ###### CRYPTO STATUS ###### */
CREATE TABLE IF NOT EXISTS crypto_status(
    crypto_status_id SERIAL PRIMARY KEY NOT NULL,
    crypto_status_name varchar(15) NOT NULL,
    long_description varchar(250) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger to Table
CREATE TRIGGER updated_at_stamp_crypto_status BEFORE UPDATE ON crypto_status
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- Insert
INSERT INTO crypto_status(crypto_status_name, long_description) 
VALUES
    ('new', 'This crypto has just been recently added in and needs to be backfilled'),
    ('active', 'This crypto is active and data is being actively retrieved for it'),
    ('inactive', 'This crypto is no longer active and no data is being retrieved for this crypto'),
    ('nodata', 'This crypto has no data that can be found. Probably needs to be investigated');


/* ###### ASSET TABLE ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS crypto (
    crypto_id SERIAL PRIMARY KEY NOT NULL,
    crypto_name varchar(50) UNIQUE NOT NULL,
    alternate_name varchar(50),
    symbol varchar(10) NOT NULL,
    category_id integer REFERENCES category(category_id),
    details varchar(250) NULL,
    worked_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_crypto BEFORE UPDATE ON crypto
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- Insert some data
INSERT INTO crypto(crypto_name, alternate_name, symbol, category_id, details) 
VALUES
    ('cryptocap10', 'top 10 cryptos', 'ccap10', 2, 'Composite tracker made of the top 10 crytocurrencies'),
    ('cryptocap20', 'top 20 cryptos', 'ccap20', 2, 'Composite tracker made of the top 20 crytocurrencies'),
    ('cryptocap30', 'top 30 cryptos', 'ccap30', 2, 'Composite tracker made of the top 30 crytocurrencies'),
    ('cryptocap50', 'top 50 cryptos', 'ccap50', 2, 'Composite tracker made of the top 50 crytocurrencies'),
    ('cryptocap100', 'top 100 cryptos', 'ccap100', 2, 'Composite tracker made of the top 100 crytocurrencies'),
    ('cryptocap200', 'top 200 cryptos', 'ccap200', 2, 'Composite tracker made of the top 200 crytocurrencies');


/* ###### HISTORICAL ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS historical (
    historical_id SERIAL PRIMARY KEY NOT NULL,
    crypto_id INTEGER REFERENCES crypto(crypto_id),
    open_price DECIMAL NOT NULL,
    high_price DECIMAL NOT NULL,
    low_price DECIMAL NOT NULL,
    close_price DECIMAL NOT NULL,
    circulating_supply DECIMAL NOT NULL,
    oustanding_marketcap DECIMAL NOT NULL,
    worked_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_historical BEFORE UPDATE ON historical
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();


/* ###### PROFILE ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS crypto_profile (
    crypto_profile_id SERIAL PRIMARY KEY NOT NULL,
    crypto_id INTEGER REFERENCES crypto(crypto_id),
    is_capped_supply BOOLEAN,
    max_supply DECIMAL,
    genesis_block_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);

CREATE TRIGGER updated_at_stamp_crypto_profile BEFORE UPDATE ON crypto_profile
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();

/* ###### TAGS ###### */
--Create Table
CREATE TABLE IF NOT EXISTS tag(
    tag_id SERIAL PRIMARY KEY NOT NULL,
    tag_name varchar(30) NOT NULL,
    short_description VARCHAR(150) NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_tag BEFORE UPDATE ON tag
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
--Insert
INSERT INTO tag(tag_name, short_description)
VALUES
    ('ethereum-ecosystem','Tokens that belong on the Ethereum block chain'),
    ('solana-ecosystem','Tokens that belong on the Solana block chain'),
    ('store-of-value','Cryptocurrencies that aim to act as a store of value like gold'),
    ('currency','Coins that aim to act as day-to-day currency like fiat(buty better)');


/* ###### CRYPTO TO TAG ###### */
--Create Table
CREATE TABLE IF NOT EXISTS crypto_to_tag(
    crypto_id INTEGER REFERENCES crypto(crypto_id),
    tag_id INTEGER REFERENCES tag(tag_id),
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_crypto_to_tag BEFORE UPDATE ON crypto_to_tag
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();


-- /* ###### TAGS ###### */

-- CREATE TABLE IF NOT EXISTS asset_tag(
--     created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
--     updated_at TIMESTAMP NULL

-- );

-- CREATE TABLE IF NOT EXISTS asset_tag(
--     created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
--     updated_at TIMESTAMP NULL

-- );
-- CREATE TABLE IF NOT EXISTS asset_tag(
--     created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
--     updated_at TIMESTAMP NULL

-- );



/* ########################### DEPRECATED ########################### 













*/