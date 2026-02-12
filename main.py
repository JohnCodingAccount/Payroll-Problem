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
        gros = self.gross
        if gros <=  12400:
            tax = gros * 0.1 
        elif gros > 12400 and gros <= 50400:
            taxUno = 12400 * 0.1
            taxDos = (gros - 12400) * 0.12
            tax = taxUno + taxDos 
        elif gros > 50400 and gros <= 105700:
            taxUno = 12400 * 0.1
            taxDos =  (50400 - 12400) * 0.12
            taxTres = (gros - 5400) * 0.22
            tax = taxUno + taxDos + taxTres
        
            
            
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
        