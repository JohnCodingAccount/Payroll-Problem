import os 
import time
import math
import csv


class Company: 
    def __init__(self):
        pass
    def get_SS_tax(self):
        tax = self.gross * 0.0765 
        return tax 
    def get_state_tax(self):
        tax = self.gross * 0.03
        return tax 
    def get_fed_tax(self):
        fed = 0 
        with open('federal.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            # Convert all rows to a list
            data = list(reader) 
            for i in range(7):
                min = int(data[i+1][0])
                if self.gross > min:
                    hib = float(data[i+1][2])
                    tax = self.gross * hib 
                    fed = fed + tax 
                else: 
                    break
        return fed 
    def get_gross(self):
        reg = self.reg_hours * self.rate
        hol = self.hol_hours * self.rate 
        over = self.over_hours * self.rate * 1.5 
        fourohonek = self.four0oneK
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
#Notes: I assume 401K and Roth will be in getting the employee data, along with their percentages / set amounts, let me know if you want to change this 
