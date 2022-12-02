#!/usr/bin/env python3

import sqlite3


mapping = {
    'A': 'r',
    'B': 'p',
    'C': 's',
    'X': 'r',
    'Y': 'p',
    'Z': 's',
}

conn = sqlite3.connect("input.db")
conn.execute('DROP TABLE IF EXISTS strategy')
conn.execute('CREATE TABLE strategy(opp TEXT, self TEXT)''')

def read_input():
    with open('./input') as f:
        for line in f:
            o, s = line.strip().split()
            yield mapping[o], mapping[s]


conn.executemany('INSERT INTO strategy VALUES(?, ?)', read_input())
conn.commit()

