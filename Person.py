# Person.py 

class Person:
    """
    Person 클래스는 사람을 나타냅니다.
    이 클래스는 사람의 ID와 이름을 저장합니다.
    """

    def __init__(self, id, name):
        """
        Person 클래스의 생성자입니다.
        ID와 이름을 설정합니다.

        :param id: 사람의 고유한 번호
        :param name: 사람의 이름
        """
        self.id = id  # 사람의 ID를 저장합니다.
        self.name = name  # 사람의 이름을 저장합니다.

    def printInfo(self):
        """
        사람의 정보를 출력하는 메서드입니다.
        ID와 이름을 보여줍니다.
        """
        print(f'ID: {self.id}, Name: {self.name}')  # ID와 이름을 출력합니다.

class Manager(Person):
    """
    Manager 클래스는 Person 클래스를 상속받아
    관리자를 나타냅니다. 관리자는 추가로 직책을 가집니다.
    """

    def __init__(self, id, name, title):
        """
        Manager 클래스의 생성자입니다.
        ID, 이름, 직책을 설정합니다.

        :param id: 관리자의 고유한 번호
        :param name: 관리자의 이름
        :param title: 관리자의 직책
        """
        super().__init__(id, name)  # 부모 클래스의 생성자를 호출하여 ID와 이름을 설정합니다.
        self.title = title  # 관리자의 직책을 저장합니다.

    def printInfo(self):
        """
        관리자의 정보를 출력하는 메서드입니다.
        ID, 이름, 직책을 보여줍니다.
        """
        super().printInfo()  # 부모 클래스의 printInfo 메서드를 호출하여 ID와 이름을 출력합니다.
        print(f'Title: {self.title}')  # 관리자의 직책을 출력합니다.

class Employee(Person):
    """
    Employee 클래스는 Person 클래스를 상속받아
    직원을 나타냅니다. 직원은 추가로 기술을 가집니다.
    """

    def __init__(self, id, name, skill):
        """
        Employee 클래스의 생성자입니다.
        ID, 이름, 기술을 설정합니다.

        :param id: 직원의 고유한 번호
        :param name: 직원의 이름
        :param skill: 직원의 기술
        """
        super().__init__(id, name)  # 부모 클래스의 생성자를 호출하여 ID와 이름을 설정합니다.
        self.skill = skill  # 직원의 기술을 저장합니다.

    def printInfo(self):
        """
        직원의 정보를 출력하는 메서드입니다.
        ID, 이름, 기술을 보여줍니다.
        """
        super().printInfo()  # 부모 클래스의 printInfo 메서드를 호출하여 ID와 이름을 출력합니다.
        print(f'Skill: {self.skill}')  # 직원의 기술을 출력합니다.

# 테스트 코드: 진입점을 체크(모듈을 직접 실행했는지를 체크)
if __name__ == "__main__":
    # 여러 사람을 만들기 위한 리스트입니다.
    people = [
        Manager(1, 'Alice', 'Project Manager'),  # 관리자를 생성합니다.
        Employee(2, 'Bob', 'Python Developer'),  # 직원을 생성합니다.
        Manager(3, 'Charlie', 'Team Lead'),  # 또 다른 관리자를 생성합니다.
        Employee(4, 'David', 'Java Developer'),  # 또 다른 직원을 생성합니다.
        Employee(5, 'Eve', 'Data Analyst'),  # 또 다른 직원을 생성합니다.
        Manager(6, 'Frank', 'Product Manager'),  # 또 다른 관리자를 생성합니다.
        Employee(7, 'Grace', 'Web Developer'),  # 또 다른 직원을 생성합니다.
        Employee(8, 'Heidi', 'DevOps Engineer'),  # 또 다른 직원을 생성합니다.
        Manager(9, 'Ivan', 'Operations Manager'),  # 또 다른 관리자를 생성합니다.
        Employee(10, 'Judy', 'UX Designer')  # 마지막 직원을 생성합니다.
    ]

    # 모든 사람의 정보를 출력합니다.
    for person in people:
        person.printInfo()  # 각 사람의 정보를 출력합니다.
        print('---')  # 구분선을 출력합니다.

    p1 = Person(100, "전우치")
    p1.printInfo()