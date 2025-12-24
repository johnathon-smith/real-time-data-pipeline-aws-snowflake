-- Now create the snowpipe
CREATE OR REPLACE PIPE MYDB.PUBLIC.MY_PIPE AUTO_INGEST = TRUE AS
COPY INTO MYDB.PUBLIC.MY_TABLE
FROM @MYDB.PUBLIC.S3_STAGE
FILE_FORMAT = (TYPE = 'JSON');

-- Now get the ARN of the SQS Queue created with the snowpipe in the last step
SHOW PIPES;

-- Get snowpipe status
SELECT SYSTEM$PIPE_STATUS( 'MYDB.PUBLIC.MY_PIPE' );
