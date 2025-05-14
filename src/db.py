# db.py
# This module handles all database operations for the CheckIn/Out System.
# It uses SQLite to persistently store individuals and log entries.
# Functions include initializing the database, saving/loading individuals, logging events, and clearing all data.

import sqlite3
import os
import datetime

# Path to the SQLite database file (appdata.db in the same directory as this script)
DB_PATH = os.path.join(os.path.dirname(__file__), 'appdata.db')

# Helper function to get a new database connection
def get_connection():
    return sqlite3.connect(DB_PATH)

# Initialize the database: create tables if they do not exist
# - individuals: stores all person data for both tables (guests and team)
# - log: stores all status change events with timestamp
def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS individuals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_type TEXT,           -- 'guest' or 'team'
            name TEXT,                 -- Last name
            vorname TEXT,              -- First name
            reisegruppe TEXT,          -- Group
            age INTEGER,               -- Age
            geschlecht TEXT,           -- Gender
            anwesend INTEGER,          -- 1 if present, 0 if not
            evakuiert INTEGER,         -- 1 if evacuated, 0 if not
            notiz TEXT                 -- Notes
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,            -- When the event happened
            fullname TEXT,             -- Full name (or table+status)
            reisegruppe TEXT,          -- Group
            status TEXT                -- Status string (e.g. 'Gäste arrived')
        )''')
        conn.commit()

# Save all individuals for a given table_type ('guest' or 'team')
# Overwrites all previous entries for that table_type
# Each individual is an instance of backend.Individual
def save_individuals(table_type, individuals):
    with get_connection() as conn:
        c = conn.cursor()
        # Remove old entries for this table_type
        c.execute('DELETE FROM individuals WHERE table_type=?', (table_type,))
        # Insert all current individuals
        for ind in individuals:
            c.execute('''INSERT INTO individuals (table_type, name, vorname, reisegruppe, age, geschlecht, anwesend, evakuiert, notiz)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (table_type, ind.name, ind.vorname, ind.reisegruppe, ind.alter, ind.geschlecht, int(ind.anwesend), int(ind.evakuiert), ind.notiz))
        conn.commit()

# Load all individuals for a given table_type ('guest' or 'team')
# Returns a list of backend.Individual objects
def load_individuals(table_type):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT name, vorname, reisegruppe, age, geschlecht, anwesend, evakuiert, notiz FROM individuals WHERE table_type=?', (table_type,))
        rows = c.fetchall()
        from backend import Individual
        individuals = []
        for row in rows:
            ind = Individual(row[0], row[1], row[2], row[3], row[4])
            ind.anwesend = bool(row[5])
            ind.evakuiert = bool(row[6])
            ind.notiz = row[7]
            individuals.append(ind)
        return individuals

# Add a new log entry for a status change
# fullname: string (e.g. 'Gäste arrived'), reisegruppe: group, status: status string
# Timestamp is generated automatically
def add_log_entry(fullname, reisegruppe, status):
    with get_connection() as conn:
        c = conn.cursor()
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO log (timestamp, fullname, reisegruppe, status) VALUES (?, ?, ?, ?)',
                  (now, fullname, reisegruppe, status))
        conn.commit()

# Load all log entries, ordered by insertion (oldest first)
# Returns a list of (timestamp, fullname, reisegruppe, status) tuples
def load_log():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT timestamp, fullname, reisegruppe, status FROM log ORDER BY id ASC')
        return c.fetchall()

# Clear all data from both tables (individuals and log)
def clear_all():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM individuals')
        c.execute('DELETE FROM log')
        conn.commit()
