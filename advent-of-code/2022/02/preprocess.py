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

mapping2 = {
    'X': 'l',
    'Y': 'd',
    'Z': 'w',
}

conn = sqlite3.connect("input.db")
with open('./init.sql') as f:
    conn.executescript(f.read())

def read_input():
    with open('./input') as f:
        for line in f:
            o, s = line.strip().split()
            yield mapping[o], mapping[s], mapping2[s]


conn.executemany('INSERT INTO strategy VALUES(?, ?, ?)', read_input())
conn.commit()

