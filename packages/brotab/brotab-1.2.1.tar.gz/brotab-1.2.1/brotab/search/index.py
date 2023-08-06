"""
This module contains helpers to work with an index of text from a browser.
"""

import argparse
import sys
import csv
import sqlite3
import logging
from contextlib import suppress


MAX_FIELD_LEN = 131072


logger = logging.getLogger('brotab')


def index(sqlite_filename, tsv_filename):
    logger.info('Reading tsv file %s', tsv_filename)
    csv.field_size_limit(sys.maxsize)
    with open(tsv_filename) as tsv_file:
        lines = [tuple(line) for line in csv.reader(tsv_file, delimiter='\t',
                                                    quoting=csv.QUOTE_NONE)]

    logger.info(
        'Creating sqlite DB filename %s from tsv %s (%s lines)',
        sqlite_filename, tsv_filename, len(lines))
    conn = sqlite3.connect(sqlite_filename)
    cursor = conn.cursor()
    with suppress(sqlite3.OperationalError):
        cursor.execute('drop table tabs;')
    cursor.execute(
        'create virtual table tabs using fts5('
        '    tab_id, title, url, body, tokenize="porter unicode61");')
    cursor.executemany('insert into tabs values (?, ?, ?, ?)', lines)
    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description='Index text from tabs')
    parser.add_argument('sqlite', help='output sqlite DB file name')
    parser.add_argument('tsv', help='input tsv file name')
    args = parser.parse_args()

    index(args.sqlite, args.tsv)


if __name__ == '__main__':
    main()
