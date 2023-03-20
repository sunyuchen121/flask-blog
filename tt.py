import collections
import itertools
import sys
import views.admin

print(sys.modules.get("views.admin"))
print(sys.modules.get("admin"))


# import itertools
# from itertools import zip_longest

class aaa:
    print(__qualname__)


class bbb(aaa):
    print(__qualname__)


try:
    print(int(5))
    print(int("1.2"))
    print(int(None))
except (TypeError, ValueError):
    print(1111)

test_d = {"a": 1}

# print(getattr(test_d, "a"))

print('\n' * 50)


class Score:
    _count = 0

    def __init__(self):
        cls = self.__class__
        prefix = "Score#"
        self.attr_name = f"{prefix}{cls._count}"
        cls._count += 1

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("必须是整数！")
        elif value < 0 or value > 100:
            raise ValueError("分数必须在[0,100]区间内！")
        setattr(instance, self.attr_name, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.attr_name)


class Student:
    math = Score()
    chinese = Score()
    english = Score()

    def __init__(self, math, chinese, english):
        self.math = math
        self.chinese = chinese
        self.english = english


s1 = Student(10, 11, 12)
s2 = Student(20, 21, 22)
print(vars(s1))
print(s1.__dict__)
print(vars(s2))
print(s2.__dict__)
print(s1.chinese)
print(s2.chinese)
print(Student.__dict__)


class TC:
    a = 1

    # def __init__(self, b=99):
    #     self.a = b


tc = TC()
print(tc.a)
TC.a = 5
print(tc.a)

print("\n" * 5)
data_errors = {'email': ['1xxxxxx@qq.com已被注册！', "测试"], 'password': ['密码长度太少！']}
print("\n".join(itertools.chain(*data_errors.values())))

print("\n" * 5)

__dd = collections.defaultdict(lambda: {"parent": None, "child": []})
__dd2 = collections.defaultdict(lambda: {"parent": None, "child": []})
__dd[5]["parent"] = 555
__dd2[5]["child"] = [123, 4444]
print(__dd2.get(6))
print(__dd)
print(__dd2)

print("\n" * 5)
print(15 / 2)
print(15 // 2)
print(16 / 2)
print(16 // 2)
print(16 / 2.0)
print(16 // 2.0)

print(list(range(1, 10)))


def func_ta(param):
    print("func_ta  running")

    def inner():
        print("aaaaaaaaaaaaaaa inner")
        return param()

    return inner


def func_tb(func_):
    print("func_tb  running")

    def inner():
        print("bbbbbbbbbbbbbbb inner")
        return func_()

    return inner


def test___():
    print(111111111111)


func_tb(func_ta(test___))()


# 装饰器执行顺序和加载顺序不一样！！！！！！！！！！！！
@func_tb
@func_ta
def test():
    pass


test()
