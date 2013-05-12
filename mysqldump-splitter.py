#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import os

DB_BEGIN_MARK = '^-- Current Database:'
#ACCEPT_LINES = ['^INSERT INTO', '^DROP']
ACCEPT_LINES = [ '^INSERT INTO' ]
ADD_HEADER = """
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;
SET AUTOCOMMIT = 0;
"""
ADD_FOOTER = """
# -- SET UNIQUE_CHECKS = 1;
# -- SET FOREIGN_KEY_CHECKS = 1;
# -- COMMIT;
"""

MYSQLDUMP_FILE = sys.argv[1]
OUTPUT_PATH = sys.argv[2]

try:
    file = open(MYSQLDUMP_FILE, 'r')

except IOError:
    sys.stderr.write("Error opening %s.\n" % MYSQLDUMP_FILE)
    sys.exit(1)

# Read file
file.seek(0)
line = file.next()
count = 0
dbfound = False

while line:
    count += 1
    #if (count % 50) == 0:
    sys.stdout.write("\rReading line: %d." % count)
    sys.stdout.flush()

    # Check database regex
    r = re.match(DB_BEGIN_MARK + " `(.*)`$", line)
    if r:
        if dbfound:
            # End of database section processing
            if len(ADD_FOOTER):
                sys.stdout.write("Writing footer to %s.\n" % output_file)
                dbf.write(ADD_FOOTER)

            dbf.close()
 
        # Mark new database processing
        dbname = r.group(1)
        dbfound = True
        sys.stdout.write("Starting processing of database %s.\n" % dbname)
        output_file = OUTPUT_PATH + "/" + dbname + ".sql"
        sys.stdout.write("Writing SQL statements to %s.\n" % output_file)
        dbf = open(output_file, "w")
  
        if len(ADD_HEADER):
            sys.stdout.write("Writing header to %s.\n" % output_file)
            dbf.write(ADD_HEADER)

        line = file.next()
        continue

    # Check operation regexes
    for regex in ACCEPT_LINES:
        if (re.match(regex, line)):
            dbf.write(line)

    # Load next line
    try:
        line = file.next()

    except:
        # End of file	
        break

if dbf:
    if len(ADD_FOOTER):
        sys.stdout.write("Writing footer to %s.\n" % output_file)
        dbf.write(ADD_FOOTER)

    dbf.close()

