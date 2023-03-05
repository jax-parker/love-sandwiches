import gspread
from google.oauth2.service_account import Credentials

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
    Get sales figures input from the user
    '''
    print('Please enter sales data from the last market.')
    print('Data should be six numbers, separated by commas.')
    print('Example: 10,20,30,40,50,60\n')

    data_str = input('Enter your data here:')
    '''The split() method returns the broken up values as a list and remove the commas from the string'''
    sales_data = data_str.split(",")
    '''call validate data function passing it the sales_data variable'''
    validate_data(sales_data)


def validate_data(values):
    '''Validate the data inputed - values will be our sales data list'''
    '''Inside the try, converts all string values into integes. Raised ValueError if strings
    cannot be converted into int, or if there aren't exactly 6 values'''
    try:
        if len(values) !=6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
            print(f'Invalid data: {e}, please try again.\n')



get_sales_data()