class Student:
    def __init__(self,name,age,chinese,math,english):
        self.name = name
        self.age = age
        self.chinese = chinese
        self.math = math
        self.english = english
    def __str__(self):
        return f"姓名：{self.name} | 年龄：{self.age} | 语文成绩：{self.chinese}| 数学成绩：{self.math}| 英语成绩：{self.english} | 总分：{self.chinese+self.math+self.english}"

class EduSystem:
    system_name = "教务管理系统"
    def __init__(self):
        self.students = []
    def add_student(self):
        print("请输入学生信息：")
        name = input("姓名：").strip()
        age = input("年龄：").strip()
        for s in self.students:
            if s.name == name and s.age == age:
                print("该学生已经存在。")
                return
        while True:
            try:
                chinese = int(input("语文：").strip())
                math = int(input("数学：").strip())
                english = int(input("英语：").strip())
            except ValueError:
                print("请输入数字")
                continue
            if 0<=chinese<=120 and 0<=math<=120 and 0<=english<=120:
                stu = Student(name,age,chinese,math,english)
                self.students.append(stu)
                print("添加成功")
                break
            else:
                print("成绩异常")
    def change_student(self):
        name = input("选择修改的姓名：").strip()
        age = input("选择修改的年龄：").strip()
        for s in self.students:
            if s.name == name and s.age == age:
                print("输入修改的成绩:")
                while True:
                    try:
                        chinese = int(input("语文："))
                        math = int(input("数学："))
                        english = int(input("英语："))
                    except ValueError:
                        print("请输入数字")
                        continue
                    if 0 <= chinese <= 120 and 0 <= math <= 120 and 0 <= english <= 120:
                        s.chinese = chinese
                        s.math = math
                        s.english = english
                        print("修改成功")
                        return
                    else:
                        print("成绩异常")
        print("未找到该学生，无法修改")

    def del_student(self):
        name = input("选择删除的学生的姓名：")
        age = input("选择删除的学生的年龄：")
        for s in self.students:
            if s.name == name and s.age == age:
                self.students.remove(s)
                print("删除成功")
                return
        print("未找到该学生，无法删除")

    def search_one(self):
        name = input("查询学生的姓名：")
        found = False

        for s in self.students:
            if s.name == name:
                print(s)
                found = True
        if not found:
            print("找不着")

    def search(self):
        if not self.students:
            print("当前没有学生信息")
            return
        for stu in self.students:
            print(stu)
    def run_student(self):
        print(f"欢迎使用{self.system_name}：")
        while True:
            print()
            print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
            print("# 1.添加学生信息 2.修改学生信息 3.删除学生信息 4.查询个人信息 5.查询所有学生信息 6 退出#")
            print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
            print()
            choice = input("请输入执行的操作（1-6）：")
            try:
                match choice:
                    case "1":
                        self.add_student()
                    case "2":
                        self.change_student()
                    case "3":
                        self.del_student()
                    case "4":
                        self.search_one()
                    case "5":
                        self.search()
                    case "6":
                        print("加纳")
                        break
                    case _:
                        print("无效")
            except ValueError:
                print("输入数据有问题")
            except Exception:
                print("程序有问题")


if __name__ == '__main__':
    edu = EduSystem()
    edu.run_student()
