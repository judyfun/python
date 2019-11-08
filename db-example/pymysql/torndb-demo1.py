import torndb


sql = ('SELECT * from users limit 10')

db = torndb.Connection("127.0.0.1:3306", "test", user="root", password="root")

rows = db.query(sql)

for r in rows:
    print(r.id)
