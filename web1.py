# web1.py 
#웹크롤링을 위한 선언 
from bs4 import BeautifulSoup

#파일을 로딩(메서드 체인) 
page = open("Chap09_test.html", "rt", encoding="utf-8").read() 

#검색이 용이한 객체 생성
soup = BeautifulSoup(page, 'html.parser')

#전체를 출력
#print(soup.prettify())
#<p>를 몽땅 검색 
#print(soup.find_all('p'))
#첫번째 <p>를 검색
#print(soup.find('p'))
#조건검색: <p class="outer-text"> 필터링
#print(soup.find_all('p', class_='outer-text'))
#attrs는 attributes의 약자 
#print(soup.find_all('p', attrs={'class':'outer-text'}))

#태그 내부의 문자열만 추출: .text 
for item in soup.find_all('p'):
    title = item.text.strip() #strip: 양쪽 공백제거
    title = title.replace('\n', '') #\n을 공백으로 대체
    print(title)

