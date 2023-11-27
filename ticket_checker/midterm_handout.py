# BTW: There's a lot of repeatative error checks that could be functions,
# but I chose not to use functions because it hasn't been covered in class.

# dictionary of the valid months and their numbers
months = {
    1  : "January",
    2  : "February",
    3  : "March",
    4  : "April",
    5  : "May",
    6  : "June",
    7  : "July",
    8  : "August",
    9  : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}

# No provided dictionary for ages? Did you mean this dictionary?
# vvv

# dictionary of the different ticket classes
ticket_classes = {      # <-- Changed ticket_class to ticket_classes for readability
    "VIP"       : 200,
    "First"     : 100,
    "Business"  : 50,
    "Economy"   : 0
}

# available seats
seats = ["A3", "A5", "B3", "B4", "C5", "D2", "D4", "E2", "E3"]

# BEGIN USER INPUT AND VALIDATION
#================================

### Print welcome text
welcome_text = "WELCOME TO THE TICKET CHECKER\n"
print(welcome_text + '=' * len(welcome_text) + '\n')

### Get input
abort_error = "Program Aborting"

## Ticket date
# Error text
ticket_date_error = "{} is not a valid month. Ticket cannot be processed."

# Get input
ticket_date = input("Enter the date of the ticket in MM/DD/YYYY format: ")
ticket_date = ticket_date.split('/')

# Test if month is a number
if not ticket_date[0].isnumeric():
    print(ticket_date_error.format(ticket_date[0]), abort_error)
    quit()
month = int(ticket_date[0])

# Test if month is valid month
if month not in months:
    print(ticket_date_error.format(month), abort_error)
    quit()

# Assemble date text
day = int(ticket_date[1])
year = int(ticket_date[2])
ticket_date_text = f'{months[month]} {day}, {year}'

## Ticket class
# Error text
ticket_class_error = "'{}' is not a valid ticket class."

# Get input
ticket_class = input("Enter the ticket class (VIP, First, Economy, Business): ")

# Test if class is valid
if ticket_class not in ticket_classes:
    print(ticket_class_error.format(ticket_class), abort_error)
    quit()

## Customer age
# Error text
customer_age_error = "Age must be a number greater than 0."

# Get input
customer_age = input("Enter the age: ")

# Test if age is a number
if not customer_age.isnumeric():
    print(customer_age_error, abort_error)
    quit()
customer_age = int(customer_age)

# Test if age is valid
if customer_age <= 0:
    print(customer_age_error, abort_error)
    quit()

## Carry-on bags
# Error text
carryon_bags_error = "Proper input is 0 or 1 for carry on bags."

# Get input
carryon_bags = input("How many carry on bags? (0/1): ")

# Test if carry on bags is valid
if carryon_bags != '0' and carryon_bags != '1':
    print(carryon_bags_error, abort_error)
    quit()
carryon_bags = int(carryon_bags)

## Checked bags
# Error text
checked_bags_error = "This must be a number greater than 0."

# Get input
checked_bags = input("How many checked bags? ")

# Test if checked bags is a number
if not checked_bags.isnumeric():
    print(checked_bags_error, abort_error)
    quit()
checked_bags = int(checked_bags)

### Print available seats
print("\nAvailable Seats:", seats)

# BEGIN PROCESSING TICKET CHARGE
# ==============================

## Find ticket price
# Base charge
base_charge = 0
if customer_age < 2:
    pass
elif customer_age >= 2 and customer_age < 60:
    base_charge = 300
elif customer_age < 80:
    base_charge = 290
elif customer_age > 80:
    base_charge = 200

# Ticket class charge
class_charge = ticket_classes[ticket_class]

# Carry on bag charge
carryon_charge = 10 if carryon_bags == 1 else 0

# Checked bags charge
checked_charge = (25 if checked_bags >= 2 else 0) + max(0, checked_bags - 2) * 50

# Total
total_charge = base_charge + class_charge + carryon_charge + checked_charge

## Find seat
seat = seats.pop(0)
seat_aisle = seat[0]
seat_number = seat[1]
    
# DISPLAY OUTPUT
# ==============

summary_text = "\nTICKET SUMMARY\n"
print(summary_text + '=' * 25)
print(f"{'Ticket Date:':<17} {ticket_date_text}")
print(f"{'Passenger Age:':<17} {customer_age}")
print(f"{'Base Charge:':<17} ${base_charge:.2f}")
print(f"{ticket_class + ' Class:':<17} ${class_charge:.2f}")
print(f"{str(carryon_bags) + ' Carry On:':<17} ${carryon_charge:.2f}")
print(f"{str(checked_bags) + ' Checked Bag(s):':<17} ${checked_charge:.2f}")
print(f"{'Seat Aisle:':<17} {seat_aisle}")
print(f"{'Seat Number:':<17} {seat_number}")
print('=' * 25)
print(f"{'TOTAL_CHARGE:':<17} ${total_charge:.2f}")
print("\nAvailable Seats:", seats)
