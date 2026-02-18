import os 
import time
import math
import csv

class Employee: 
    def __init__(self, name, hours, reg_hours, hol_hours, over_hours, rate, roth, fourOhOneK):
        pass
    def get_SS_tax(self):
        tax = self.gross * 0.0765 
        return tax 
    def get_state_tax(self):
        tax = self.gross * 0.03
        return tax 
    def get_fed_tax(self):
        pass
    def get_gross(self):
        reg = self.reg_hours * self.rate
        hol = self.hol_hours * self.rate 
        over = self.over_hours * self.rate * 1.5 
        fourohonek = self.fourOhOneK
        self.gross = reg + hol + over - fourohonek
        return self.gross 
    def get_net(self):
        stateTax = self.get_state_tax()
        ssTax = self.get_SS_tax()
        fedTax = self.get_fed_tax()
        netVal = self.gross - stateTax - ssTax - fedTax - self.roth
        self.net = netVal 
        return self.net 
    def seperate_hours(self): 
        regHrs = int(input("How many hours were regular hours?: "))
        holHrs = int(input("How many hours were holiday hours?: "))
        oveHrs = 40 - (regHrs + holHrs)
        self.reg_hours = regHrs
        self.hol_hours = holHrs
        self.over_hours = oveHrs 
employ1 = Employee(inp1, 1,1,1,1,1,1,1,1)
