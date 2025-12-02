# 파일에쓰기와읽기연습.py

# demo.txt파일에 쓰기: write text  
# 파일 인스턴스가 리턴. 유니코드 작업 을 위해 encoding='utf-8' 지정
f = open('demo.txt', 'wt', encoding='utf-8')
f.write('안녕하세요.\n')
f.write('파일에 쓰기와 읽기 연습입니다.\n')
f.write("세번째 라인\n")
f.close()

# demo.txt파일에서 읽기: read text 
f = open('demo.txt', 'rt', encoding='utf-8')
#파일의 끝까지 읽기를 해서 문자열 변수로 리턴 
content = f.read()
print(content)
f.close()

