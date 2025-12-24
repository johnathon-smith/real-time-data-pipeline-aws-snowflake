CREATE OR REPLACE DATABASE MYDB;

USE SCHEMA MYDB.PUBLIC;

-- Create S3 integration
CREATE OR REPLACE STORAGE INTEGRATION S3_INT
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = 'S3'
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::778277577883:role/dea-realtimeproject-snowpipe-role'
STORAGE_ALLOWED_LOCATIONS = ('s3://dea-realtimeproject-data-bucket-001/data/');

-- Describe newly formed integration to get external user role ARN and ID
DESC INTEGRATION S3_INT;

-- Create Stage with S3 integration
CREATE OR REPLACE STAGE MYDB.PUBLIC.S3_STAGE
STORAGE_INTEGRATION = S3_INT
URL = 's3://dea-realtimeproject-data-bucket-001/data/';

-- Test connection to S3 integration in the stage
ls @S3_STAGE;

-- Now create a raw table for the snowpipe to load data into
CREATE OR REPLACE TABLE MYDB.PUBLIC.MY_TABLE
(
    DATA VARIANT
);
