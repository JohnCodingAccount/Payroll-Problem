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
        gros = self.gross
        gros = gros * 52
        fed = 0 
        val = 0 
        tax = 0
        clamp = 0 
        if gros > 7500 and self.gross < 19900: 
            val = 0.0
            tax = 0.10 
            clamp = self.gross - 7500 
        elif self.gross >= 19900 and self.gross < 57900: 
            val = 1240.0
            tax = 0.12 
            clamp = self.gross - 19900
        elif self.gross >= 57900 and self.gross < 113200: 
            val = 5800.0
            tax = 0.22 
            clamp = self.gross - 57900
        elif self.gross >= 113200 and self.gross < 209275: 
            val = 17966.0
            tax = 0.24 
            clamp = self.gross - 113200
        elif self.gross >= 209275 and self.gross < 263725: 
            val = 41024.0
            tax = 0.32 
            clamp = self.gross - 209275
        elif self.gross >= 263725 and self.gross < 648100: 
            val = 58448.0
            tax = 0.35 
            clamp = self.gross - 263725
        elif self.gross >= 648100:
            val = 192979.25
            tax = 0.37 
            clamp = self.gross - 648100
        fed_tax = (clamp * tax) + val
        fed_tax = fed_tax / 52
        fed = round(fed_tax, 2)
        return fed
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


