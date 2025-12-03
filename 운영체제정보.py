# 운영체제정보.py
import os 
import os.path 
import glob 

print(os.name) #운영체제 이름
print(os.environ)

print("---파일정보---")
#raw string notation: \\를 두번 사용하지 않고 처리 
fileName = r"c:\python310\python.exe"

if os.path.exists(fileName):
    print("파일크기:", os.path.getsize(fileName), "바이트")
else:
    print("파일이 존재하지 않습니다.")

print("파일명:", os.path.basename(fileName))
print("전체이름", os.path.abspath("python.exe"))

print("--------파일목록--------")
#print(glob.glob("c:\\work\\*.py"))
for item in glob.glob(r"c:\work\*.py"):
    print(item)


