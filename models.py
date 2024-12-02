"""
This module defines data container classes for a person, department, and employee.
These classes are used to represent entities in the application.
"""

class Persn:
    """Simple data container for a person."""
    def __init__(self, name, age):
        self.nm = name
        self.ag = age

    def gret(self):
        """
        Generate a greeting message for the person.

        Returns:
            str: A greeting message with the person's name.
        """
        return f"Hello {self.nm}!"

# pylint: disable=too-few-public-methods
class Department:
    """Simple data container for a department."""
    def __init__(self, name):
        self.name = name

# pylint: disable=too-few-public-methods
class Employee:
    """Simple data container for an employee."""
    def __init__(self, name, age, department):
        self.name = name
        self.age = age
        self.department = department
