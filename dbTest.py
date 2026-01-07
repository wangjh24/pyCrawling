import psycopg2

db = psycopg2.connect(host = 'localhost',dbname = 'PyCrawling',user= 'test',password = '1234',port=5432)
cur = db.cursor()
cur. execute("SELECT * FROM test_table; ")
rows = cur.fetchall()
print (rows)
for row in rows:
            print(f"ID: {row[0]} | 내용: {row[1]} ")
# DB 연결 종료
cur.close()
db.close()
