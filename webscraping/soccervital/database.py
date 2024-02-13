import pyodbc
import pandas as pd

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=THYAGOPC\SQLEXPRESS;'
                      'Database=SQLTutorial;'
                      'Trusted_Connection=yes;')

# conn = pyodbc.connect(connectionString)


class Connection:
    def __init__(self):
        self.conn = conn
        self.cursor = conn.cursor()

    def close(self):
        self.conn.close()
