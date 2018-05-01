import time
import mylibrary

cur = mylibrary.login()

while True:
    sql = 'select (select count(*) from picture), (select count(*) from picture where ifdownload = 0)'
    cur.execute(sql)
    print(cur.fetchone())
    time.sleep(3)
