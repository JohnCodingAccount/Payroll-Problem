#Getting imports
import os
from enum import Enum
import pygame
import time


#Validation functions for each employee data field
def verify_name(name, data):
    return len(name.strip()) > 0

def verify_hours(hours, data):
    hours_in_week = 168
    try:
        newH = float(hours)
        return 0 < newH <= hours_in_week
    except ValueError:
        return False

def verify_reg_hours(reg_hours, data):
    try:
        newR = float(reg_hours)
        return 0 < newR <= data.get('HOURS', 0)
    except ValueError:
        return False

def verify_hol_hours(hol_hours, data):
    try:
        newHol = float(hol_hours)
        return newHol >= 0 and (newHol + data.get('REG_HOURS', 0)) <= data.get('HOURS', 0)
    except ValueError:
        return False

def verify_rate(rate, data):
    try:
        return float(rate) > 0
    except ValueError:
        return False

def verify_roth(roth, data):
    try:
        return 0 <= float(roth) <= 100
    except ValueError:
        return False

def verify_401k(_401k, data):
    try:
        return 0 <= float(_401k) <= 100
    except ValueError:
        return False


class EmployeeData(Enum):
    NAME     = ("What is the employee's name?: ",                                          str,   verify_name)
    HOURS    = ("How many hours a week does the employee work?: ",                         float, verify_hours)
    REG_HOURS= ("How many of those hours are regular hours?: ",                            float, verify_reg_hours)
    HOL_HOURS= ("How many of those hours are holiday hours?: ",                            float, verify_hol_hours)
    RATE     = ("What is the rate of pay?: ",                                              float, verify_rate)
    ROTH     = ("What is the employee's ROTH percentage (To be applied with taxes): %",   float, verify_roth)
    _401K    = ("What is the employee's 401K percentage (To be applied without taxes): %",float, verify_401k)

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
            prompt, converter, validator = item.value
            while True:
                user_input = input(prompt)
                if validator(user_input, self.employee_data):
                    self.employee_data[item.name] = converter(user_input)
                    break
                else:
                    print("Invalid input. Please enter a valid value.")

    #Calculating the amount of gross income the employee earns, this includes 401K
    def get_gross(self):
        data = self.employee_data
        rate = data['RATE']
        reg = data['REG_HOURS'] * rate
        hol = data['HOL_HOURS'] * rate
        over_hours = max(0, data['HOURS'] - (data['HOL_HOURS'] + data['REG_HOURS']))
        over_pay = over_hours * rate * 1.5
        self.gross = round((reg + hol + over_pay), 2)
        dub = round((reg + hol + over_pay), 2)
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
        data = self.employee_data
        _401K_deduct = (self.get_gross()[0] * (data['_401K'] / 100))
        gross = self.get_gross()[0] - _401K_deduct
        ss_tax = gross * 0.0765
        state_tax = gross * 0.03
        fed_tax = self.get_fed_tax()
        roth_deduction = round(gross * (self.employee_data['ROTH'] / 100),2)
        self.net = round(gross - ss_tax - state_tax - fed_tax - roth_deduction, 2)
        dub = round(gross - ss_tax - state_tax - fed_tax - roth_deduction, 2)
        return (self.net, dub, ss_tax, state_tax, fed_tax, roth_deduction, _401K_deduct)

    #Prints employee's most critcal data, including: name, gross income, and net income
    def __str__(self):
        return f"Employee: {self.employee_data['NAME']} | Gross: ${self.gross:.2f} | Net: ${self.net:.2f} | Social Security Deduction: {self.calculate_pay()[2]} | State Deduction: {self.calculate_pay()[3]} | Federal Deduction: {self.calculate_pay()[4]} | Roth Deduction: {self.calculate_pay()[5]} | 401K Deduction: {self.calculate_pay()[6]}"

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
            os.system('cls')

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
        clock = pygame.time.Clock()
        #Defining a color palate
        black   = (0,   0,   0  )
        white   = (255, 255, 255)
        green   = (0,   210, 100)
        dark_green = (0, 140, 60)
        gray    = (30,  30,  30 )
        gold    = (255, 200, 50 )
        #Defining the size of window as tuple
        (width, height) = (600, 520)
        #Setting the screen up
        screen = pygame.display.set_mode((width, height))
        #Setting window name
        pygame.display.set_caption('Payroll Program')

        #Sets up different font
        title_path = "ChelseaMarket-Regular.ttf"

        #Sets up title font & regitsters other fonts
        font_title = pygame.font.Font(title_path, 28)
        font_label = pygame.font.Font('freesansbold.ttf', 14)
        font_val   = pygame.font.Font('freesansbold.ttf', 14)

        
        #Defines variable for latter use
        EMPLOYEE_NUM = 0

        #Animation state
        slide_offset = 0        # horizontal offset for slide-in animation
        slide_direction = 0     # -1 = sliding left in, 1 = sliding right in
        sliding = False
        SLIDE_SPEED = 20        # pixels per frame
        alpha_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        #Arrow button rects (drawn manually, no images needed)
        arrow_left_rect  = pygame.Rect(10,  height - 70, 80, 50)
        arrow_right_rect = pygame.Rect(width - 90, height - 20, 80, 50)

        #Loading in outside graphics and setting position
        try:
            img = pygame.image.load('sizedRight.png').convert_alpha()
            img_rect = img.get_rect()
            img_rect.center = (width - 45, height - 45)
            img1 = pygame.image.load('sizedLeft.png').convert_alpha()
            img_rect1 = img1.get_rect()
            img_rect1.center = (50, height - 45)
            use_images = True
        except:
            use_images = False

        def draw_arrow_button(rect, direction, hovered):
            color = gold if hovered else green
            border_color = white if hovered else dark_green
            pygame.draw.rect(screen, border_color, rect.inflate(4, 4), border_radius=10)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            cx, cy = rect.centerx, rect.centery
            if direction == 'left':
                pts = [(cx+14, cy-14), (cx-14, cy), (cx+14, cy+14)]
            else:
                pts = [(cx-14, cy-14), (cx+14, cy), (cx-14, cy+14)]
            pygame.draw.polygon(screen, black, pts)

        def draw_card(x, y, w, h, label, value, label_color, val_color):
            pygame.draw.rect(screen, gray, (x, y, w, h), border_radius=8)
            pygame.draw.rect(screen, green, (x, y, w, h), width=1, border_radius=8)
            lbl_surf = font_label.render(label, True, label_color)
            val_surf = font_val.render(value, True, val_color)
            screen.blit(lbl_surf, (x + 8, y + 6))
            screen.blit(val_surf, (x + 8, y + 26))

        def get_employee_lines(emp_idx):
            emp = my_company.employees[emp_idx]
            data = emp.employee_data
            over_hours = max(0, data['HOURS'] - (data['REG_HOURS'] + data['HOL_HOURS']))
            return {
                'name':     data.get('NAME'),
                'hours':    str(data.get('HOURS')),
                'rate':     f"${data.get('RATE'):.2f}",
                'reg':      str(data.get('REG_HOURS')),
                'hol':      str(data.get('HOL_HOURS')),
                'over':     str(round(over_hours, 2)),
                'gross':    f"${emp.get_gross()[1]:.2f}",
                'net':      f"${emp.calculate_pay()[1]:.2f}",
                '401k':     f"{data.get('_401K')}%",
                'roth':     f"{data.get('ROTH')}%",
                '_401k_deduct': f"${emp.calculate_pay()[6]:.2f}",
                'roth_deduct' : f"${emp.calculate_pay()[5]:.2f}",
                "ss_tax_deduct" : f"${emp.calculate_pay()[2]:.2f}",
                "state_tax_deduct" : f"${emp.calculate_pay()[3]:.2f}",
                "fed_tax_deduct" : f"${emp.calculate_pay()[4]:.2f}",
                "reg_hours_pay" : f"${data.get('REG_HOURS') * data.get('RATE'):.2f}",
                "hol_hours_pay" : f"${data.get('HOL_HOURS') * data.get('RATE'):.2f}",
                "over_hours_pay" : f"${round(over_hours * data.get('RATE') * 1.5, 2)}",
            }

        #Setting up a main loop for window
        running = True

        #Adds background music to the program 
        pygame.mixer.music.load("Stars.mp3")
        pygame.mixer.music.set_volume(0.0)
        pygame.mixer.music.play(-1)

        debounce = False
        while running:
            
            
            dt = clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            #Getting all actions in the window
            for event in pygame.event.get():
                #Checking if window is terminated
                if event.type == pygame.QUIT:
                    running = False
                #Checking if mouse is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #Checking if you clicked the right arrow
                        if arrow_right_rect.collidepoint(event.pos) or (use_images and img_rect.collidepoint(event.pos)):
                            if not sliding:
                                if debounce == False:
                                    debounce = True
                                    EMPLOYEE_NUM = (EMPLOYEE_NUM + 1) % count
                                    slide_offset = width
                                    slide_direction = -1
                                    sliding = True
                                    debounce = False
                        #Checking if you clicked the left arrow
                        elif arrow_left_rect.collidepoint(event.pos) or (use_images and img_rect1.collidepoint(event.pos)):
                            if not sliding:
                                if debounce == False:
                                    debounce = True
                                    EMPLOYEE_NUM = (EMPLOYEE_NUM - 1) % count
                                    slide_offset = -width
                                    slide_direction = 1
                                    sliding = True
                                    debounce = False
                elif event.type == pygame.KEYDOWN:
                    #Checking if you pressed the left key
                    if event.key == pygame.K_LEFT:
                        if not sliding:
                            if debounce == False:
                                debounce = True
                                EMPLOYEE_NUM = (EMPLOYEE_NUM - 1) % count
                                slide_offset = -width
                                slide_direction = 1
                                sliding = True
                                debounce = False
                           
                    #Checking if you pressed the right key
                    if event.key == pygame.K_RIGHT:
                        if not sliding:
                            if debounce == False:
                                debounce = True
                                EMPLOYEE_NUM = (EMPLOYEE_NUM + 1) % count
                                slide_offset = width
                                slide_direction = -1
                                sliding = True
                                debounce = False
            
            #Setting the dark background
            screen.fill((10, 10, 20))

            #Draw subtle grid lines for style
            for gx in range(0, width, 40):
                pygame.draw.line(screen, (20, 20, 35), (gx, 0), (gx, height))
            for gy in range(0, height, 40):
                pygame.draw.line(screen, (20, 20, 35), (0, gy), (width, gy))

            #Draw the content panel with slide offset
            panel_x = slide_offset

            #Title bar
            pygame.draw.rect(screen, dark_green, (panel_x, 0, width, 50), border_radius=0)
            title_surf = font_title.render(f"Employee {EMPLOYEE_NUM + 1} of {count}", True, white)
            screen.blit(title_surf, (panel_x + 20, 12))

            #Get current employee data
            lines = get_employee_lines(EMPLOYEE_NUM)

            #Draw info cards in a 2-column grid
            card_w = 265
            card_h = 52
            margin = 16
            start_y = 65

            

            cards_left_1 = [
                ("Name",          lines['name'],  white, gold),
                ("Hours / Week",  lines['hours'], white, white),
                ("Regular Hours", lines['reg'],   white, white),
                ("Holiday Hours", lines['hol'],   white, white),
                ("Overtime Hours",lines['over'],  white, white),
            ]

            cards_right_1 = [
                ("Hourly Rate",   lines['rate'],  white, gold),
                ("401K Rate",     lines['401k'],  white, white),
                ("ROTH Rate",     lines['roth'],  white, white),
                ("Gross Pay",     lines['gross'], white, gold),
                ("Net Pay",       lines['net'],   white, green),
            ]

            for i, (lbl, val, lc, vc) in enumerate(cards_left_1):
                y = start_y + i * (card_h + margin)
                draw_card(panel_x + margin, y, card_w, card_h, lbl, val, lc, vc)

            for i, (lbl, val, lc, vc) in enumerate(cards_right_1):
                y = start_y + i * (card_h + margin)
                draw_card(panel_x + margin*2 + card_w, y, card_w, card_h, lbl, val, lc, vc)

                        #Animate slide
            if sliding:
                if slide_direction == -1:
                    slide_offset -= SLIDE_SPEED
                    if slide_offset <= 0:
                        slide_offset = 0
                        sliding = False

                else:
                    slide_offset += SLIDE_SPEED
                    if slide_offset >= 0:
                        slide_offset = 0
                        sliding = False
                    for i, (lbl, val, lc, vc) in enumerate(cards_left_1):
                        y = start_y + i * (card_h + margin)
                        draw_card(panel_x + margin, y, card_w, card_h, lbl, val, lc, vc)

                    for i, (lbl, val, lc, vc) in enumerate(cards_right_1):
                        y = start_y + i * (card_h + margin)
                        draw_card(panel_x + margin*2 + card_w, y, card_w, card_h, lbl, val, lc, vc)

            #Draw arrow buttons
            left_hovered  = arrow_left_rect.collidepoint(mouse_pos)
            right_hovered = arrow_right_rect.collidepoint(mouse_pos)

            if use_images:
                screen.blit(img1, img_rect1)
                screen.blit(img,  img_rect)
            else:
                draw_arrow_button(arrow_left_rect,  'left',  left_hovered)
                draw_arrow_button(arrow_right_rect, 'right', right_hovered)

            #Updating the window with these changes
            pygame.display.flip()

        pygame.quit()

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
