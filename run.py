import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    '''
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated by commas.
    The loop will repeatedly request data, until it is valid.
    '''
    while True:
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, separated by commas.')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Enter your data here:')
        '''The split() method returns the broken up values as a list and remove the commas from the string'''
        sales_data = data_str.split(",")
        '''call validate data function passing it the sales_data variable'''
        if validate_data(sales_data):
            print('data is valid!')
            break
    return sales_data

def validate_data(values):
    '''Validate the data inputed - values will be our sales data list'''
    '''Inside the try, converts all string values into integes. Raised ValueError if strings
    cannot be converted into int, or if there aren't exactly 6 values'''
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
            print(f'Invalid data: {e}, please try again.\n')
            '''returns are based on the if condition inside the while loop above'''
            return False
    return True

def update_sales_worksheet(data):
    '''
    Update sales worksheet, add new row with the list data provided
    '''
    print('Updating sales worksheet...\n')
    '''Now we need to access our sales  worksheet from our Google Sheet  
    so that we can add our data to it using the gspread method to access
    the worksheet'''
    sales_worksheet = SHEET.worksheet('sales')
    '''The append_row method adds a new row to the  end of our
    data in the worksheet selected.  '''
    sales_worksheet.append_row(data)

    print('Sales Worksheet updated successfully.\n')

def calculate_surplus_data(sales_row):
    '''
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock: 
    - positive surplus indicates waste
    - negative surplus indicates extra made when stock was sold out.
    '''
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    '''In this case stock with square brackets giving it the list index of -1. This will slice the final item from the list and
    return it to the new stock variable.'''
    stock_row = stock[-1]
    pprint(stock_row)

def main():
    '''
    Run all program functions
    '''

    data = get_sales_data()
    '''new list comprehension'''
    sales_data = [int(num) for num in data]
    '''Call our function and pass it our sales_data list'''
    update_sales_worksheet(sales_data)
    '''Call function and pass in our sales data variable '''
    calculate_surplus_data(sales_data)

print('Welcome to Love Sandwiches Data Automation')
main()