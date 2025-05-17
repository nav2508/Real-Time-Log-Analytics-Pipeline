CREATE EXTERNAL TABLE logs (
  timestamp string,
  level string,
  message string,
  service string
)
PARTITIONED BY (`year` string, `month` string, `day` string, `hour` string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = '1',
  'field.delim' = '\n'
)
STORED AS TEXTFILE
LOCATION 's3://real-time-logs-streaming-bucket25/logs/'
TBLPROPERTIES (
  'classification'='json',
  'compressionType'='gzip'
);
