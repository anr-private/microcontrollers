#!/bin/bash
#
# renumber the line numbers in markers in try_easy_logger.py


cp -p try_easy_logger.py  try_easy_logger.1

python3 ./renumber_line_numbers.py  try_easy_logger.1  '@T1@'

mv try_easy_logger.1.out  try_easy_logger.2
rm try_easy_logger.1.bak

python3 ./renumber_line_numbers.py  try_easy_logger.2  '@T2@'
mv try_easy_logger.2.out  try_easy_logger.3
rm try_easy_logger.2.bak

python3 ./renumber_line_numbers.py  try_easy_logger.3  '@T3@'
mv try_easy_logger.3.out  try_easy_logger.4
rm try_easy_logger.3.bak

python3 ./renumber_line_numbers.py  try_easy_logger.4  '@T4@'
mv try_easy_logger.4.out  try_easy_logger.5
rm try_easy_logger.4.bak

python3 ./renumber_line_numbers.py  try_easy_logger.5  '@T5@'
mv try_easy_logger.5.out  try_easy_logger.6
rm try_easy_logger.5.bak

python3 ./renumber_line_numbers.py  try_easy_logger.6  '@T6@'
mv try_easy_logger.6.out  try_easy_logger.7
rm try_easy_logger.6.bak

python3 ./renumber_line_numbers.py  try_easy_logger.7  '@T7@'
mv try_easy_logger.7.out  try_easy_logger.8
rm try_easy_logger.7.bak

python3 ./renumber_line_numbers.py  try_easy_logger.8  '@T8@'
mv try_easy_logger.8.out  try_easy_logger.9
rm try_easy_logger.8.bak

python3 ./renumber_line_numbers.py  try_easy_logger.9  '@T9@'
mv try_easy_logger.9.out  try_easy_logger.10
rm try_easy_logger.9.bak

cp -p try_easy_logger.10  try_easy_logger.py

rm -f try_easy_logger.?
rm -f try_easy_logger.1?

#more try_easy_logger.2
