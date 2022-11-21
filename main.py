import secrets
import time
import glob
from datetime import date
from fpdf import FPDF

# Function to Display Options
def options():
    print("1. Order")
    print("2. Search Bill")
    print("3. Exit")

# Functions to Display Menu
def get_menu():
    menu = open('menu.txt', 'r')
    for line in menu:
        print(line, end='')
    print("\ne   Exit")
    menu.close()

# Function to get the Order from User
def order():
    token = secrets.token_hex(16)
    cart = [token]

    get_menu()
    while (True):
        print()
        dish = input("Enter Your Dish/[E/e]: ")
        if (dish.upper() == 'E'):
            if (len(cart) > 1):
                generate_bill(cart, user)
            print()
            return

        while (True):
            quantity = int(input("Quantity: "))
            print()
            if (quantity > 0):
                break
            print("Invalid!")

        dish = dish.lower().capitalize()
        cart = add_items_to_cart(cart, dish, quantity)

        order_again = input("Order Again? [Yes/No]: ").upper()
        if (order_again == 'NO'):
            generate_bill(cart, user)
            print()
            return
        else:
            continue
    return

# Function to add User Selected Items to Cart
def add_items_to_cart(cart, dish, quantity):
    file = open('menu.txt', 'r')

    for item in cart:
        if (item != cart[0]):
            if (item['name'] == dish):
                item['quantity'] += quantity
                return cart

    for line in file:
        if (line.find(dish) != -1):
            value = line.split()
            cart.append({
                'id': value[0],
                'name': value[1],
                'price': value[2],
                'quantity': quantity
            })
    return cart

# Function to Generate TXT File of the Bill
def generate_bill(cart, user):
    current_date = date.today()
    current_time = time.strftime("%H:%M:%S", time.localtime())
    total = 0
    bill = open(f"./Bills/{cart[0]}_{user}.txt", 'w')
    bill.write(f"Bill ID: {cart[0]}\n\n")
    bill.write(f"Date: {current_date}\n\n")
    bill.write(f"Time: {current_time}\n\n")
    bill.write(
        f"\n{'id' : <5}{'name' : <50}{'price' : >20}{'quantity' : >20}\n\n")
    for item in cart:
        if (item != cart[0]):
            bill.write(
                f"{item['id'] : <5}{item['name'] : <50}{item['price'] : >20}{item['quantity'] : >20}\n"
            )
            total += int(item['price']) * int(item['quantity'])
    bill.write(f"\nTotal: {total}")
    bill.close()
    generate_pdf(cart, user)
    return

# Function to Generate PDF of the Bill
def generate_pdf(cart, user):
    file = open(f"./Bills/{cart[0]}_{user}.txt", 'r')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    for line in file:
        pdf.cell(200, 10, txt=line, ln=1, align="L")

    pdf.output(f"./PDFs/{cart[0]}_{user}.pdf")
    file.close()
    return

# Function to Search Bill
def search_bill(user):
    files = glob.glob(f'./Bills/*_{user}.txt')
    if (len(files) < 1):
        print("\nNo Bills Found!\n")
        return
    print()
    counter = 1
    for file in files:
        print(f"{counter}) {str(file)}")
        counter += 1
    print()

    return

# Start of the Program
user = str()
while (not user):
    user = input("Enter Your Name: ")
    if (not user):
        print("Username Cannot be Empty!\n")
    else:
        break

if (user):
    print(f"\nHello {user}, Welcome!\n")

    while (True):
        options()
        print()
        choice = int(input("Enter Your Choice: "))

        if (choice == 1):
            print()
            order()
        elif (choice == 2):
            search_bill(user)
        else:
            exit(0)