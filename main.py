import os
from enum import Enum
import pygame


#Class made in order to easily store and retrieve employee data 
class EmployeeData(Enum):
    NAME = ("What is the employee's name?: ", str)
    HOURS = ("How many hours a week does the employee work?: ", float)
    REG_HOURS = ("How many of those hours are regular hours?: ", float)
    HOL_HOURS = ("How many of those hours are holiday hours?: ", float)
    RATE = ("What is the rate of pay?: ", float)
    ROTH = ("What is the employee's ROTH percentage (To be applied with taxes): %", float)
    _401K = ("What is the employee's 401K percentage (To be applied without taxes): %", float)

class Employee:
    #Defines what to do when a new Employee is made, includes: calculating pay, collecting data, and storing it
    def __init__(self):
        self.employee_data = {}
        self.gross = 0.0
        self.net = 0.0
        self.collect_employee_data()
        self.calculate_pay()[0]
    
    #Gathers user input for the employee data 
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

    #Calculating the amount of gross income the employee earns, this includes 401K
    def get_gross(self):
        data = self.employee_data
        rate = data['RATE']
        reg = data['REG_HOURS'] * rate
        hol = data['HOL_HOURS'] * rate
        over_hours = max(0, data['HOURS'] - 40)
        over_pay = over_hours * rate * 1.5
        pre_tax_401k = (reg + hol + over_pay) * (data['_401K'] / 100)
        self.gross = round((reg + hol + over_pay) - pre_tax_401k,2)
        dub = round((reg + hol + over_pay) - pre_tax_401k,2)
        return (self.gross, dub)

    #Gets federal tax using a withholding table 
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

    #Calculates the net pay of the employee incorperating SS tax, state tax, federal tax, gross income, and ROTH
    def calculate_pay(self):
        gross = self.get_gross()[0]
        ss_tax = gross * 0.0765
        state_tax = gross * 0.03
        fed_tax = self.get_fed_tax()
        roth_deduction = gross * (self.employee_data['ROTH'] / 100)
        self.net = round(gross - ss_tax - state_tax - fed_tax - roth_deduction,2)
        dub = round(gross - ss_tax - state_tax - fed_tax - roth_deduction,2)
        return (self.net, dub)

    #Prints employee's most critcal data, including: name, gross income, and net income
    def __str__(self):
        return f"Employee: {self.employee_data['NAME']} | Gross: ${self.gross:.2f} | Net: ${self.net:.2f}"

class Company:
    #Defines want to do when class is initalized
    def __init__(self, employee_count=None):
        self.employees = []
        if employee_count is not None:
            self.hire_bulk(employee_count)

    #Creates new employee classes
    def hire_bulk(self, count):
        for i in range(count):
            print(f"\nEntering data for Employee #{i+1}:")
            new_emp = Employee()
            self.employees.append(new_emp)

    #Shows all the critical employee data for the entire company 
    def show_payroll(self):
        print("\n--- Company Payroll ---")
        for emp in self.employees:
            print(emp)
    
    #Graphical display of the information
    def show(self):
        global count
        #Opening the library
        pygame.init() 
        #Defining a color palate 
        black = (0,0,0)
        white = (255, 255, 255)
        #Defining the size of window as tuple
        (width, height) = (500,500)
        #Setting the screen up
        screen = pygame.display.set_mode((width, height))
        #Setting window name
        pygame.display.set_caption('Payroll Program')
        #Setting the visual elements/text of the window, initalized but blank until update while running
        EMPLOYEE_NUM = 0 
        font = pygame.font.Font('freesansbold.ttf', 32)
        txt = font.render("Employee: " + str(EMPLOYEE_NUM + 1), True, white, black)
        txtRect = txt.get_rect()
        txtRect.center = (100, 25)
        font2 = pygame.font.Font('freesansbold.ttf', 16)
        trt = font2.render("Name: " , True, white, black)
        t2 = font2.render("Hours this week: " , True, white, black)
        t3 = font2.render("Hourly rate: " , True, white, black)
        t4 = font2.render("Regular hours: " , True, white, black)
        t5 = font2.render("Holiday hours: " , True, white, black)
        t6 = font2.render("Over hours: " , True, white, black)
        t7 = font2.render("Gross Pay: $" , True, white, black)
        t8 = font2.render("Net Pay: $", True, white, black)
        t9 = font2.render("401K rate: " + "" + "%", True, white, black)
        t10 = font2.render("Roth rate: " + "" + "%", True, white, black)
        #Initalizing the boxes/rects of the text
        trtRect = trt.get_rect()
        t2R = t2.get_rect() 
        t3R = t3.get_rect()
        t4R = t4.get_rect()
        t5R = t5.get_rect()
        t6R = t6.get_rect()
        t7R = t7.get_rect()
        t8R = t8.get_rect()
        t9R = t9.get_rect()
        t10R = t10.get_rect()
        #Intializing text positions
        trtRect.left = 10
        trtRect.centery = 65
        t2R.left = 10
        t3R.left = 10
        t4R.left = 10
        t5R.left = 10
        t6R.left = 10
        t7R.left = 10
        t8R.left = 300
        t9R.left = 300
        t10R.left = 300 
        t2R.centery = 110
        t3R.centery = 160
        t4R.centery = 210
        t5R.centery = 260
        t9R.centery = 260
        t6R.centery = 310
        t10R.centery = 310
        t7R.centery = 360
        t8R.centery = 360
        #Loading in outside graphics and setting position
        img = pygame.image.load('sizedRight.png').convert_alpha()
        img_rect = img.get_rect()
        img_rect.center = (450, 450) 
        img1 = pygame.image.load('sizedLeft.png').convert_alpha()
        img_rect1 = img1.get_rect()
        img_rect1.center = (50, 450) 
        #Setting up a main loop for window
        running = True 
        EMPLOYEE_NUM = 0
        while running: 
            #Getting all actions in the window
            for event in pygame.event.get():
                #Checking if window is terminated
                if event.type == pygame.QUIT:
                    running = False
                #Checking if mouse is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #Checking if you clicked the right arrow
                        if img_rect.collidepoint(event.pos):
                            EMPLOYEE_NUM = int(EMPLOYEE_NUM)
                            if (EMPLOYEE_NUM + 1) == count:
                                EMPLOYEE_NUM = 0
                            else:
                                EMPLOYEE_NUM +=1 
                        #Checking if you clicked the left arrow
                        elif img_rect1.collidepoint(event.pos):
                            EMPLOYEE_NUM = int(EMPLOYEE_NUM)
                            if EMPLOYEE_NUM <= 0: 
                                EMPLOYEE_NUM = count
                            else:
                                EMPLOYEE_NUM -=1 
            #Updating the text values based on the employee you are currently viewing      
            txt = font.render("Employee: " + str(EMPLOYEE_NUM + 1), True, white, black)
            trt = font2.render("Name: " + my_company.employees[EMPLOYEE_NUM].employee_data.get('NAME'), True, white, black)
            t2 = font2.render("Hours this week: " + str(my_company.employees[EMPLOYEE_NUM].employee_data.get('HOURS')) , True, white, black)
            t3 = font2.render("Hourly rate: " + str(my_company.employees[EMPLOYEE_NUM].employee_data.get('REG_HOURS')) , True, white, black)
            t4 = font2.render("Regular hours: " + str(my_company.employees[EMPLOYEE_NUM].employee_data.get('HOL_HOURS')), True, white, black)
            t6 = font2.render("Over hours: " + str(40 - my_company.employees[EMPLOYEE_NUM].employee_data.get('REG_HOURS') + my_company.employees[0].employee_data.get('HOL_HOURS')), True, white, black)
            t7 = font2.render("Gross Pay: $" + str(my_company.employees[EMPLOYEE_NUM].get_gross()[1]), True, white, black)
            t8 = font2.render("Net Pay: $" + str(my_company.employees[EMPLOYEE_NUM].calculate_pay()[1]), True, white, black)
            t9 = font2.render("401K rate: " + str(my_company.employees[EMPLOYEE_NUM].employee_data.get('_401K')) + "%", True, white, black)
            t10 = font2.render("Roth rate: " + str(my_company.employees[EMPLOYEE_NUM].employee_data.get('ROTH')) + "%", True, white, black)
            #Setting the black background
            screen.fill((0,0,0))
            #Setting up the arrows 
            screen.blit(img, img_rect)
            screen.blit(img1, img_rect1)
            #Setting up the texts 
            screen.blit(txt, txtRect)
            screen.blit(trt, trtRect)
            screen.blit(t2, t2R)
            screen.blit(t3, t3R)
            screen.blit(t4, t4R)
            screen.blit(t5, t5R)
            screen.blit(t6, t6R)
            screen.blit(t7, t7R)
            screen.blit(t8, t8R)
            screen.blit(t9, t9R)
            screen.blit(t10, t10R)
            #Updating the window with these changes
            pygame.display.flip()

while True:
    try:
        #Gets number of employees wanted with an ID10T proofing loop
        count = int(input("How many employees to process?: "))
        if count <= 0:
            print("Must have at least one employee")
        else: 
            break
    except ValueError:
        print("Invalid input")

#Uses number of employees and shows critical employee data 
my_company = Company(count)
my_company.show_payroll()


while True:
    #Asks if full display of data is wanted, with ID10T proofing
    graphics = input("Would you like to see a full display of the information? (y/n): ")
    graphics = graphics.lower()
    if graphics == "y":
        os.system('cls')
        my_company.show()
        os.system('cls')
        break
    elif graphics == "n":
        break
    else: 
        print("Print invalid input!")
        
#Prints farewell message
os.system('cls')
print("Thank you for using Alex & John's payroll program!")
