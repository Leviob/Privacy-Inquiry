#! /usr/bin/python3

from dotenv import load_dotenv
load_dotenv()
import json, requests, sys, pprint, datetime, os
from tabulate import tabulate

apikey = os.environ.get('API_KEY')

def main():
    if len(sys.argv) < 2:
        print('Usage: Include transaction amount in cents, or date ([yyyy-]m-d), or merchant name as an argument')
        sys.exit()
         
        # For troublshooting:
        # print_transactions() 

    # Distinguish whether date or amount were provided in CL argument:
    # If purely numeric argument(positive or negative), search for tranasctions with this amount.
    if sys.argv[1].isnumeric() or (sys.argv[1][0] == '-' and sys.argv[1][1:].isnumeric()): 
        search_by_amount(int(sys.argv[1]))

    # If argument is formatted like a date, search for transactions with this date.
    elif '-' in sys.argv[1] and sys.argv[1][0] != '-': # Dash exists, but not as a negative number

        # If only month and day given (e.g. 1-20), assume current year
        if sys.argv[1].count('-') == 1:
            today = datetime.datetime.today()
            try:
                date = datetime.datetime.strptime(str(today.year) + '-' + sys.argv[1], '%Y-%m-%d') 
            except ValueError:
                print('That isn\'t a correct date format.') # Triggered by non-date inputs, e.g. 55-43
                sys.exit()
            # If month and day is in the future, use previous year
            if today < date:
                date = date.replace(year=(today.year - 1))


        elif sys.argv[1].count('-') == 2:
            try:
                date = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
            except ValueError:
                print('That isn\'t a correct date format.') # Triggered by non-date inputs with 2 hyphens, e.g. 55-43-1612
                sys.exit()
        else:
            print('Invalid format. Give amount in cents, or date in [yyyy-]m-d format')
            sys.exit()

        search_by_date(date.strftime('%Y-%m-%d')) 
    elif sys.argv[1].isalpha() and sys.argv[1] != 'ls':
        search_by_merchant(sys.argv[1])

    # List some or all recent transactions
    elif sys.argv[1] == 'ls':
        if len(sys.argv) > 2 and sys.argv[2].isnumeric():
            list_transactions(int(sys.argv[2]))
        else:
            list_transactions(1000)
        sys.exit()
    else: 
        print('Invalid format. Give amount in cents, or date in [yyyy-]m-d format')
        sys.exit()

def download_transactions():
    '''
    Downloads transaction history using Privacy.com's API.

    Parameters:
        None

    Returns:
        dict: downloaded transaction data
    '''
    transactions_url='https://api.privacy.com/v1/transaction?&page_size=1000'  # Only the first 1000 transactions
    response = requests.get(transactions_url, headers={'Authorization':f'api-key {apikey}'})
    response.raise_for_status()
    return json.loads(response.text)

def list_transactions(num_to_show):
    '''
    Prints tabulated list of the passed number of most recent transactions.

    Parameters:
        num_to_show (int): The number of transictions to print

    Returns:
        None
    '''
    transaction_data = download_transactions()
    results = [['Vendor', 'Amount', 'Date']]
    if len(transaction_data['data']) < num_to_show:
        num_to_show = len(transaction_data['data'])
    for transaction in transaction_data['data'][:num_to_show]:
        results.append([f'{transaction["merchant"]["descriptor"]}', f'${transaction["amount"]/100}', f'{transaction["created"][:10]}'])
    print (tabulate(results))

def search_by_date(transaction_date):
    '''
    Searches downloaded data for transactions made on passed date.

    Parameters:
        transaction_date (str): The date of transactions to return. Format: 'yyyy-mm-dd'

    Returns:
        None
    '''
    transaction_data = download_transactions()   
    # Iterate over 'data', whos value is a list of dictionaries, each of which is a transaction
    for transaction in transaction_data['data']: 
        if str(transaction['created'])[:10] == transaction_date:
            print_results(transaction)
            
def search_by_amount(amount):
    '''
    Searches downloaded data for transactions of passed amount.

    Parameters:
        amount (int): The amount in cents of transactions to return.

    Returns:
        None
    '''
    transaction_data = download_transactions()    
    for transaction in transaction_data['data']:
        if transaction['amount'] == amount:
            print_results(transaction)

def search_by_merchant(merchant):
    '''
    Searches downloaded data for transactions of passed amount.

    Parameters:
        merchant (str): The merchant descriptor of transactions to return.

    Returns:
        None
    '''
    transaction_data = download_transactions()    
    for transaction in transaction_data['data']:
        if merchant in transaction['merchant']['descriptor'].lower():
            print_results(transaction)

def print_results(transaction):
    '''
    Prints information of transactions.

    Parameters:
        transaction (dict): Dictionary of transaction details.

    Returns:
        None    
    '''
    merch_descriptor = transaction['merchant']['descriptor']
    dollar_amount = transaction['amount']/100
    datetime_object = datetime.datetime.strptime(transaction["created"], '%Y-%m-%dT%H:%M:%SZ')
    date_long = datetime_object.strftime('%B %d, %Y')

    # Return matching dates and amounts
    print(f'{merch_descriptor} was paid ${dollar_amount} on {date_long}')
        
    # Return more information if requested
    if len(sys.argv) > 2 and (sys.argv[2].lower() == 'more' or sys.argv[2].lower() == 'm'):
        trans_status = transaction['status']
        trans_result = transaction['result']
        card_name = transaction['card']['memo']
        merch_city = transaction['merchant']['city']
        merch_state = transaction['merchant']['state']
        print(f'This transaction is {trans_result} and {trans_status}')
        print(f'The card used is named: {card_name}')
        print(f'{merch_descriptor} is located in {merch_city}, {merch_state}\n')

def print_transactions(): 
    '''For troubleshooting - downloads and displays formatted json data of transactions.'''

    transactions_url='https://api.privacy.com/v1/transaction?begin=2020-01-01&page_size=1000' # Only the first 1000 transactions
    response = requests.get(transactions_url, headers={'Authorization':f'api-key {apikey}'})
    response.raise_for_status()
    # print(response.text)
    # load json to python variable
    pprint.pprint(json.loads(response.text))
    sys.exit()
    
main()