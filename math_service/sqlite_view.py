# Maxim Dragos, Data Engineer

import sqlite3
conn = sqlite3.connect(
    'C:/Endava/EnDevLocal/PYCHARMproj/Dava_X/ms_API_math_comp/requests.db'
)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# Show contents of a table
cursor.execute("SELECT * FROM requests_logs")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()

#
# import sqlite3
#
# conn = sqlite3.connect(
# 'C:/Endava/EnDevLocal/PYCHARMproj/Dava_X/ms_API_math_comp/requests.db'
# )
# cursor = conn.cursor()
# cursor.execute("""
#     INSERT INTO requests_logs (operation, input_data, result, status_code)
#     VALUES (?, ?, ?, ?)
# """, ('test', '{"a":3,"b":2}', '2', 200))
# conn.commit()
# conn.close()
