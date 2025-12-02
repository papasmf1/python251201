# class2.py
# Developer클래스를 정의하려고 하는데, id, name, skill속성을 추가
class Developer:
    def __init__(self, id, name, skill):
        self.id = id
        self.name = name
        self.skill = skill
    def get_info(self):
        return f"ID: {self.id}, Name: {self.name}, Skill: {self.skill}"
    
#인스턴스를 생성 
dev = Developer(1, "Alice", "Python")
print(dev.get_info())  # 출력: ID: 1, Name: Alice, Skill: Python






