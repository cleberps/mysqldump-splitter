#!/bin/bash

DATABASES="database1 database2 database3 database4 databaseN"
HOST="localhost"
DBUSER="root"
PASSWD="mypassword"
for db in ${DATABASES}; do
  mysql --skip-column-names -h ${HOST} -u ${DBUSER} -p${PASSWD} <<< \
	"SELECT CONCAT('ALTER TABLE ',table_schema,'.',table_name,' engine=InnoDB;') AS COMMANDS
	 FROM information_schema.tables 
	WHERE table_schema = '${db}' AND engine = 'MyISAM';"
done
