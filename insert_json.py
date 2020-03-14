import sqlite3
import json

conn = sqlite3.connect('db.sqlite3')
print('Open datebase successfully')

with open('./wechatapp/json_files/areas.json') as f:

    data = json.load(f)
    for line in data:
        sql = "INSERT INTO `wechatapp` (id, name, parent_id, type) VALUES('%s','%s','%s',%d)"%(
            line['id'], line['name'], line['parent_id'], line['type'])
        print(sql)
        conn.execute(sql)
        conn.commit()
print('Operation done successfully')
conn.close()
