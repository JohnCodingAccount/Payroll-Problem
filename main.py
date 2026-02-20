import os
import time
import math
import csv
from enum import Enum

class EmployeeData(Enum):
    NAME = ("What is the employee's name?: ", str)
    HOURS = ("How many hours a week does the employee work?: ", float)
    REG_HOURS = ("How many of those hours are regular hours?: ", float)
    HOL_HOURS = ("How many of those hours are holiday hours?: ", float)
    RATE = ("What is the rate of pay?: ", float)
    ROTH = ("What is the employee's ROTH percentage (To be applied with taxes): %", float)
    _401K = ("What is the employee's 401K percentage (To be applied without taxes): %", float)

class Employee:
    def __init__(self):
        self.employee_data = {}
        self.gross = 0.0
        self.net = 0.0
        self.collect_employee_data()
        self.calculate_pay()

    def collect_employee_data(self):
        for item in EmployeeData:
            prompt, data_type = item.value
            while True:
                try:
                    user_input = input(prompt)
                    self.employee_data[item.name] = data_type(user_input)
                    break
                except ValueError:
                    print("Invalid input. Please enter the correct data type.")

    def get_gross(self):
        data = self.employee_data
        rate = data['RATE']
        reg = data['REG_HOURS'] * rate
        hol = data['HOL_HOURS'] * rate
       
        over_hours = max(0, data['HOURS'] - 40)
        over_pay = over_hours * rate * 1.5
       
        pre_tax_401k = (reg + hol + over_pay) * (data['_401K'] / 100)
        self.gross = (reg + hol + over_pay) - pre_tax_401k
        return self.gross

    def get_fed_tax(self):
        annual_gross = self.gross * 52
        val, tax_rate, threshold = 0.0, 0.0, 0.0

        if annual_gross >= 648100:
            val, tax_rate, threshold = 192979.25, 0.37, 648100
        elif annual_gross >= 263725:
            val, tax_rate, threshold = 58448.0, 0.35, 263725
        elif annual_gross >= 209275:
            val, tax_rate, threshold = 41024.0, 0.32, 209275
        elif annual_gross >= 113200:
            val, tax_rate, threshold = 17966.0, 0.24, 113200
        elif annual_gross >= 57900:
            val, tax_rate, threshold = 5800.0, 0.22, 57900
        elif annual_gross >= 19900:
            val, tax_rate, threshold = 1240.0, 0.12, 19900
        elif annual_gross >= 7500:
            val, tax_rate, threshold = 0.0, 0.10, 7500

        weekly_fed = ((annual_gross - threshold) * tax_rate + val) / 52
        return round(weekly_fed, 2)

    def calculate_pay(self):
        gross = self.get_gross()
        ss_tax = gross * 0.0765
        state_tax = gross * 0.03
        fed_tax = self.get_fed_tax()
        roth_deduction = gross * (self.employee_data['ROTH'] / 100)
       
        self.net = gross - ss_tax - state_tax - fed_tax - roth_deduction
        return self.net

    def __str__(self):
        return f"Employee: {self.employee_data['NAME']} | Gross: ${self.gross:.2f} | Net: ${self.net:.2f}"

class Company:
    def __init__(self, employee_count=None):
        self.employees = []
        if employee_count is not None:
            self.hire_bulk(employee_count)

    def hire_bulk(self, count):
        for i in range(count):
            print(f"\nEntering data for Employee #{i+1}:")
            new_emp = Employee()
            self.employees.append(new_emp)

    def show_payroll(self):
        print("\n--- Company Payroll ---")
        for emp in self.employees:
            print(emp)

count = int(input("How many employees to process?: "))
my_company = Company(count)
my_company.show_payroll()
