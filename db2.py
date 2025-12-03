# db1.py 
import sqlite3
#연결객체 생성(영구적으로 저장)
#raw string 처리: r"경로명"
con = sqlite3.connect(r"c:\work\sample.db")
#커서객체 생성
cur = con.cursor()
#테이블 생성
cur.execute("CREATE TABLE IF NOT EXISTS PhoneBook (name text, phoneNum text);")
#데이터 삽입
cur.execute("INSERT INTO PhoneBook VALUES ('홍길동', '010-1234-5678');")

#입력파라메터처리 
name = '김삿갓'
phoneNum = '010-8765-4321'
cur.execute("INSERT INTO PhoneBook VALUES (?, ?);", (name, phoneNum))   

#다중의 리스트를 입력 
datalist = (("전우치","010-222-1234"), ("이순신","010-333-5678"))   
cur.executemany("INSERT INTO PhoneBook VALUES (?, ?);", datalist)

cur.execute("SELECT * FROM PhoneBook;")
#블럭주석처리:ctrl+/
for row in cur:
    print(row)

#변경내용 저장
con.commit()