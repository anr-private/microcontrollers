#!/bin/bash

cat logs.ALL | \
grep -v MWSMAIN@ | \
grep -v ELFT@  | \
grep -v HP@  | \
grep -v RH@  | \
grep -v RHDATA@  | \
grep -v SENSORS@  | \
grep -v MwsSensors@  | \
grep -v LIBLCD@  | \
grep -v WEBSVR@  | \
grep -v MwsWifi@  | \
grep -v TimeMgr@   \
 >junk.out 

ls -l junk.out

head -39 junk.out

###
 