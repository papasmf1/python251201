# DemoForm2.py 
# DemoForm2.ui(화면단) + DemoForm2.py(로직단) = DemoForm 완성
import sys 
from PyQt5.QtWidgets import * 
from PyQt5 import uic   
#웹크롤링을 위한 선언
from bs4 import BeautifulSoup
#웹서버에 요청 
import urllib.request

#디자인 문서를 로딩(로딩하는 화면을 변경)
form_class = uic.loadUiType("DemoForm2.ui")[0]

#DemoForm 클래스 정의(상속받는 부모 - QMainWindow)
class DemoForm(QMainWindow, form_class):
    #초기화 메서드
    def __init__(self):
        super().__init__()
        self.setupUi(self)  #화면단 로딩
    #슬롯메서드 추가
    def firstClick(self):
        f = open("clien.txt", "wt", encoding="utf-8")
        for i in range(0,10):
            url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(i)    
            print(url)    
            #페이지 실행 결과를 문자열로 받기 
            page = urllib.request.urlopen(url).read() 
            #검색이 용이한 객체 
            soup = BeautifulSoup(page, 'html.parser')
            lst = soup.find_all("span", attrs={"data-role":"list-title-text"})
            for tag in lst:
                title = tag.text.strip() 
                print(title)
                f.write(title + "\n")
        f.close()
        self.label.setText("클리앙 중고장터 크롤링 완료")
    def secondClick(self):
        self.label.setText("두번째 버튼 클릭~~")
    def thirdClick(self):
        self.label.setText("세번째 버튼 클릭합니다")


#진입점 체크 
if __name__ == "__main__":
    #실행프로세스를 생성 
    app = QApplication(sys.argv)
    #폼을 생성 
    demoForm = DemoForm() 
    #화면에 보이기 
    demoForm.show() 
    #이벤트 루프 진입
    app.exec_()

