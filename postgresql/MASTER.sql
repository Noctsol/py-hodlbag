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
DROP TRIGGER IF EXISTS updated_at_stamp_cts_outstanding_mcap ON cts_outstanding_mcap;
DROP TRIGGER IF EXISTS updated_at_stamp_cts_outstanding_supply ON cts_outstanding_supply;
DROP TRIGGER IF EXISTS updated_at_stamp_cts_circulating_supply ON cts_circulating_supply;
DROP TRIGGER IF EXISTS updated_at_stamp_cts_status ON cts_status;
DROP TRIGGER IF EXISTS updated_at_stamp_cstatus ON cstatus;
DROP TRIGGER IF EXISTS updated_at_stamp_ccategory ON ccategory;
DROP TRIGGER IF EXISTS updated_at_stamp_crypto ON crypto;
DROP TRIGGER IF EXISTS updated_at_stamp_cts_price ON cts_price;
DROP TRIGGER IF EXISTS updated_at_stamp_ctag ON ctag;
DROP TRIGGER IF EXISTS updated_at_stamp_crypto_to_ctag ON crypto_to_ctag;
DROP TRIGGER IF EXISTS updated_at_stamp_cprofile ON cprofile;

-- NOTE: DO NOT CHANGE THE DAMN ORDER
DROP TABLE IF EXISTS cprofile;
DROP TABLE IF EXISTS crypto_to_ctag;
DROP TABLE IF EXISTS cts_price;
DROP TABLE IF EXISTS cts_circulating_supply;
DROP TABLE IF EXISTS cts_outstanding_supply;
DROP TABLE IF EXISTS cts_outstanding_mcap;
DROP TABLE IF EXISTS cts_status;
DROP TABLE IF EXISTS crypto;
DROP TABLE IF EXISTS ccategory;
DROP TABLE IF EXISTS cstatus;
DROP TABLE IF EXISTS ctag;


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



/* ###### ccategory TABLE ###### 
    I only did this because I wanted to track custom things like the top 10/20 cryptos but
    didn't want to make an entirely different table system for them. I may live to regret this.
*/
-- Create Table
CREATE TABLE IF NOT EXISTS ccategory (
    ccategory_id SERIAL PRIMARY KEY NOT NULL,
    ccategory_name varchar(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger to Table
CREATE TRIGGER updated_at_stamp_ccategory BEFORE UPDATE ON ccategory
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- Insert
INSERT INTO ccategory(ccategory_name) 
VALUES
    ('crypto'),
    ('crypto-agg'),
    ('unknown');


/* ###### CRYPTO STATUS ###### 
    Determines the status of a newly added crypto. Wehther its new, active or whatever.
*/

CREATE TABLE IF NOT EXISTS cstatus(
    cstatus_id SERIAL PRIMARY KEY NOT NULL,
    cstatus_name varchar(15) NOT NULL,
    long_description varchar(250) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger to Table
CREATE TRIGGER updated_at_stamp_cstatus BEFORE UPDATE ON cstatus
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- Insert
INSERT INTO cstatus(cstatus_name, long_description) 
VALUES
    ('new', 'This crypto has just been recently added in and needs to be backfilled'),
    ('active', 'This crypto is active and data is being actively retrieved for it'),
    ('inactive', 'This crypto is no longer active and no data is being retrieved for this crypto'),
    ('nodata', 'This crypto has no data that can be found. Probably needs to be investigated');


/* ###### crypto TABLE ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS crypto (
    crypto_id SERIAL PRIMARY KEY NOT NULL,
    crypto_name varchar(50) UNIQUE NOT NULL,
    alternate_name varchar(50),
    symbol varchar(10) NOT NULL,
    details varchar(250) NULL,
    ccategory_id integer NOT NULL REFERENCES ccategory(ccategory_id),
    cstatus_id INTEGER NOT NULL REFERENCES cstatus(cstatus_id),
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL,
    sources varchar(150)[] NOT NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_crypto BEFORE UPDATE ON crypto
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- Insert some data
INSERT INTO crypto(crypto_name, alternate_name, symbol, details, ccategory_id, cstatus_id, sources) 
VALUES
    ('bitcoin', 'digitalgold', 'btc', 'The grandaddy of them all. Please stop betting against it and hurting yourself.', 1, 1, '{"manual"}'),
    ('ethereum', 'memecontracts', 'eth', 'Made by Satoshi Nakamoto''s son, Vitalik Buterin.', 1, 1, '{"manual"}'),
    ('cardano', 'peerreviewedlul', 'ada', 'Made by Vitalik''s jealous cousin. "Can we stop talking about Ethereum?" - Charles Hoskinson.', 1, 1, '{"manual"}'),
    ('polkadot', 'connect4', 'dot', 'Ethereum''s cool cousin that decided to do something different.', 1, 1, '{"manual"}'),
    ('nano', 'prodigalgrandson', 'nano', 'If bitcoin had a son to carry the family legacy, nano would be it. Fast and feeless(I know, I know).', 1, 1, '{"manual"}'),
    ('cryptocap10', 'top 10 cryptos', 'ccap10', 'Composite tracker made of the top 10 crytocurrencies', 2, 1, '{"manual"}'),
    ('cryptocap20', 'top 20 cryptos', 'ccap20', 'Composite tracker made of the top 20 crytocurrencies', 2, 1, '{"manual"}'),
    ('cryptocap30', 'top 30 cryptos', 'ccap30', 'Composite tracker made of the top 30 crytocurrencies', 2, 1, '{"manual"}'),
    ('cryptocap50', 'top 50 cryptos', 'ccap50', 'Composite tracker made of the top 50 crytocurrencies', 2, 1, '{"manual"}'),
    ('cryptocap100', 'top 100 cryptos', 'ccap100', 'Composite tracker made of the top 100 crytocurrencies', 2, 1, '{"manual"}'),
    ('cryptocap200', 'top 200 cryptos', 'ccap200', 'Composite tracker made of the top 200 crytocurrencies', 2, 1, '{"manual"}');


/* ###### cts_status ###### 
    To mark the status of any time series data I'm actively gathering. Things in the crypto data world are not perfect.
    Some websites will post data before its finished or change it back after its finalized.
*/
-- Create Table
CREATE TABLE cts_status(
    cts_status_id SERIAL PRIMARY KEY NOT NULL,
    cts_status_name VARCHAR(15) NOT NULL,
    long_description VARCHAR(250) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Trigger
CREATE TRIGGER updated_at_stamp_cts_status BEFORE UPDATE ON cts_status
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
-- insert
INSERT INTO cts_status(cts_status_name, long_description)
VALUES
    ('closed', 'All data was retrieved and no more work is required'),
    ('current', 'Most up-to-date. This data is not finalized at all.'),
    ('dubious', 'This status indicates doubt that the data is correct or finished'),
    ('nodata', 'After multiple attempts, no data was retrievable for this item. Chances are there was an outage or no trading activity.');


/* ###### cprofile ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS cprofile (
    cprofile_id SERIAL PRIMARY KEY NOT NULL,
    crypto_id INTEGER REFERENCES crypto(crypto_id),
    cts_status_id INTEGER REFERENCES cts_status(cts_status_id),
    is_capped_supply BOOLEAN,
    max_supply DECIMAL,
    genesis_block_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL,
    sources varchar(150)[] NOT NULL
);

CREATE TRIGGER updated_at_stamp_cprofile BEFORE UPDATE ON cprofile
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();


/* ############ crypto timeseries tqables (cts for short) ############ 
    This section will contain all the tables for time series data. This was separated out because information
    for all of these differe vbery differently and how they are sources and calculated and even when they arte finished.
*/


/* ###### cts_price ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS cts_price (
    cts_price_id SERIAL PRIMARY KEY NOT NULL,
    crypto_id INTEGER REFERENCES crypto(crypto_id),
    cts_status_id INTEGER REFERENCES cts_status(cts_status_id),
    record_time TIMESTAMP NOT NULL,
    open_price DECIMAL,
    high_price DECIMAL,
    low_price DECIMAL,
    close_price DECIMAL,
    volume DECIMAL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL,
    sources varchar(150)[] NOT NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_cts_price BEFORE UPDATE ON cts_price
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();


/* ###### cts_circulating_supply ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS cts_circulating_supply (
    cts_circulating_supply_id SERIAL PRIMARY KEY NOT NULL,
    crypto_id INTEGER REFERENCES crypto(crypto_id),
    cts_status_id INTEGER REFERENCES cts_status(cts_status_id),
    record_time TIMESTAMP NOT NULL,
    circulating_supply DECIMAL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL,
    sources varchar(150)[] NOT NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_cts_circulating_supply BEFORE UPDATE ON cts_circulating_supply
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();


/* ###### cts_outstanding_supply ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS cts_outstanding_supply (
    cts_outstanding_supply_id SERIAL PRIMARY KEY NOT NULL,
    crypto_id INTEGER REFERENCES crypto(crypto_id),
    cts_status_id INTEGER REFERENCES cts_status(cts_status_id),
    record_time TIMESTAMP NOT NULL,
    outstanding_supply DECIMAL NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL,
    sources varchar(150)[] NOT NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_cts_outstanding_supply BEFORE UPDATE ON cts_outstanding_supply
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();


/* ###### cts_outstanding_mcap ###### */
-- Create Table
CREATE TABLE IF NOT EXISTS cts_outstanding_mcap (
    cts_outstanding_mcap_id SERIAL PRIMARY KEY NOT NULL,
    crypto_id INTEGER REFERENCES crypto(crypto_id),
    cts_status_id INTEGER REFERENCES cts_status(cts_status_id),
    record_time TIMESTAMP NOT NULL,
    outstanding_marketcap DECIMAL NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL,
    sources varchar(150)[] NOT NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_cts_outstanding_mcap BEFORE UPDATE ON cts_outstanding_mcap
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();










/* ###### ctag TABLE ###### 
    For tagging crypto with various categories. I decided to go for normalized approach.
    Hopefully, this doesn't bite me in the ass. Well, both directions have their pros and cons
*/
--Create Table
CREATE TABLE IF NOT EXISTS ctag(
    ctag_id SERIAL PRIMARY KEY NOT NULL,
    ctag_name varchar(30) NOT NULL,
    short_description VARCHAR(150) NULL,
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_ctag BEFORE UPDATE ON ctag
    FOR EACH ROW EXECUTE FUNCTION trg_updated_at();
--Insert
INSERT INTO ctag(ctag_name, short_description)
VALUES
    ('ethereum-ecosystem','Tokens that belong on the Ethereum block chain'),
    ('solana-ecosystem','Tokens that belong on the Solana block chain'),
    ('store-of-value','Cryptocurrencies that aim to act as a store of value like gold'),
    ('currency','Coins that aim to act as day-to-day currency like fiat(but better)');


/* ###### crypto_to_ctag ###### */
--Create Table
CREATE TABLE IF NOT EXISTS crypto_to_ctag (
    crypto_to_ctag_id SERIAL PRIMARY KEY NOT NULL,
    crypto_id INTEGER REFERENCES crypto(crypto_id),
    ctag_id INTEGER REFERENCES ctag(ctag_id),
    created_at TIMESTAMP DEFAULT NOW_UTC() NOT NULL,
    updated_at TIMESTAMP NULL
);
-- Create Trigger
CREATE TRIGGER updated_at_stamp_crypto_to_ctag BEFORE UPDATE ON crypto_to_ctag
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