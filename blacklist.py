import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "user_login",
    charset = "utf8"
      )

cursor = db.cursor()

def add(url):
  value=(url)
  query = "INSERT INTO blacklist (url) VALUES (%s)"
  cursor.execute(query,value)
  
  db.commit()
  return "Added Successfully"
