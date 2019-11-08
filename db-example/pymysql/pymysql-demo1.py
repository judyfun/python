import pymysql.cursors



connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
# cursor.execute("""
# CREATE TABLE persons (
#     id INT NOT NULL,
#     name VARCHAR(100),
#     salesrep VARCHAR(100),
#     PRIMARY KEY(id)
# )
# """)
# cursor.executemany(
#     "INSERT INTO persons VALUES (%s, %s, %s)",
#     [(1, 'John Smith', 'John Doe'),
#      (2, 'Jane Doe', 'Joe Dog'),
#      (3, 'Mike T.', 'Sarah H.')])
# you must call commit() to persist your data if you don't set autocommit to True
# connection.commit()

# cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
# row = cursor.fetchone()

cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')

for r in cursor:
    print(r)
# while row:
#     print(row)
    # print("ID=%s, Name=%s" % (row[0], row[1]))
    # row = cursor.fetchone()

connection.close()