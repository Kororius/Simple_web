class Persn:
    def __init__(self, name, age):
        self.nm = name
        self.ag = age

    def gret(self):
        return f"Hello {self.nm}!"
class Department:
    def __init__(self, name):
        self.name = name

class Employee:
    def __init__(self, name, age, department):
        self.name = name
        self.age = age
        self.department = department