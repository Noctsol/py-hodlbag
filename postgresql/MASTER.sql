/*

    Master script for generating DB
    - Generate at will


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


DROP TRIGGER IF EXISTS updated_at_stamp_historical_status ON historical_status;
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
DROP TABLE IF EXISTS historical_status;
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
    details varchar(250) NULL,
    category_id integer NOT NULL REFERENCES category(category_id),
    crypto_status_id INTEGER NOT NULL REFERENCES crypto_status(crypto_status_id),
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_crypto BEFORE UPDATE ON crypto
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- Insert some data
INSERT INTO crypto(crypto_name, alternate_name, symbol, details, category_id, crypto_status_id) 
VALUES
    ('bitcoin', 'digitalgold', 'btc', 'The grandaddy of them all. Please stop betting against it and hurting yourself.', 1, 1),
    ('ethereum', 'memecontracts', 'eth', 'Made by Satoshi Nakamoto''s son, Vitalik Buterin.', 1, 1),
    ('cardano', 'peerreviewedlul', 'ada', 'Made by Vitalik''s jealous cousin. "Can we stop talking about Ethereum?" - Charles Hoskinson.', 1, 1),
    ('polkadot', 'connect4', 'dot', 'Ethereum''s cool cousin that decided to do something different.', 1, 1),
    ('nano', 'prodigalgrandson', 'nano', 'If bitcoin had a son to carry the family legacy, nano would be it. Fast and feeless(I know, I know).', 1, 1),
    ('cryptocap10', 'top 10 cryptos', 'ccap10', 'Composite tracker made of the top 10 crytocurrencies', 2, 1),
    ('cryptocap20', 'top 20 cryptos', 'ccap20', 'Composite tracker made of the top 20 crytocurrencies', 2, 1),
    ('cryptocap30', 'top 30 cryptos', 'ccap30', 'Composite tracker made of the top 30 crytocurrencies', 2, 1),
    ('cryptocap50', 'top 50 cryptos', 'ccap50', 'Composite tracker made of the top 50 crytocurrencies', 2, 1),
    ('cryptocap100', 'top 100 cryptos', 'ccap100', 'Composite tracker made of the top 100 crytocurrencies', 2, 1),
    ('cryptocap200', 'top 200 cryptos', 'ccap200', 'Composite tracker made of the top 200 crytocurrencies', 2, 1);


/* ###### HISTORICAL ###### */
-- Create Table
CREATE TABLE historical_status(
    historical_status_id SERIAL PRIMARY KEY NOT NULL,
    historical_status_name VARCHAR(15) NOT NULL,
    long_description VARCHAR(250) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Trigger
CREATE TRIGGER updated_at_stamp_historical_status BEFORE UPDATE ON historical_status
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- insert
INSERT INTO historical_status(historical_status_name, long_description)
VALUES
    ('closed', 'All data was retrieved and no more work is required'),
    ('incomplete', 'Data was found but is not final or completed'),
    ('nodata', 'After multiple attempts, no data was retrievable for this item. Chances are there was an outage or no trading activity.');


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