# 準備資料庫連線
#準備網站後端系統
from typing import Annotated
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
import json
app=FastAPI()
# 建立後端 RESTful APIs
# 新增留言的 API
from mysql.connector import pooling

dbconfig = {
    "user": "root",
    "password": "password",
    "host": "localhost",
    "database": "fastapi"
}

cnxpool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)
@app.post("/api/message")
def create_message(body=Body(None)):
    # 預期前端透過 Request Body 請求文本傳遞 {"author": "姓名", "content": "內容"}
    try:        
        print("Database Ready")
        body = json.loads(body)
        author = body["author"]
        content = body["content"]
        # 連線到資料庫，將資料新增到資料表中
        con = cnxpool.get_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO message (author, content) VALUES (%s, %s)", (author, content))
        con.commit()
        cursor.close()
        con.close()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
@app.get("/api/message")
def get_message():
    print("Database Ready")
    con=cnxpool.get_connection()
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM message")
    data=cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return data
# 根據編號刪除留言的 API
@app.delete("/api/message/{id}")
def delete_message(id):
    # 連線到資料庫，根據 id 的值，刪除留言資料
    con=cnxpool.get_connection()
    cursor=con.cursor()
    cursor.execute("DELETE FROM message WHERE id=%s", [id])
    con.commit()
    cursor.close()
    con.close()
    return {"ok":True}
# 靜態檔案處理，支援前端網頁呈現
app.mount("/", StaticFiles(directory="public", html=True))
