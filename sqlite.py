# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('flags.db')

c = conn.cursor()

conn.commit()

conn.close()