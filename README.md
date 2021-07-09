# Privacy-Inquiry
CLI program for searching spending history through Privacy.com.

[Privacy](https://www.privacy.com) is a service that allows online purchases to be made without your bank knowing what merchant you are shopping at, and without the merchant knowing your true name, credit card number, or address. A side effect of this privacy enhancing service is that my bank statements show dates and amounts, but do not show which store a transaction took place. This program implements the Privacy API and allows me to quickly search through all my transactions made through Privacy and return useful information. 

## Usage
Transactions can be searched by date or transaction amount, or simply listed. Command line arguments dictate what results are returned. 
An API key from Privacy.com is required for this script to function. The `apikey` variable can be modified to equal the API key. 

### Search by Date
Passing a date will initiate a search for all transactions made on that date. The date argument can be formatted as yyyy-m-d, or m-d. Omitting the year will search for most recent corresponding day and month(current year, or previous year). Single digit days and months are also accepted. For example:

    $ ./privacy_inquiry.py 2020-4-11
    CHIPOTLE ONLINE was paid $8.53 on April 11, 2020

### Search by Amount
Passing an integer will initiate a search for all transactions of that amount in cents. This value can be positive or negative (indicating a refund). 

    $ ./privacy_inquiry.py 1176
    CHICK-FIL-A #02855 was paid $11.76 on June 19, 2020
    CHICK-FIL-A #02855 was paid $11.76 on October 1, 2019

### Search by Merchant
Passing a string (other than 'ls') will initiate a search for all transactions made with merchants whos descriptor includes the passed string. 

    $ ./privacy_inquiry.py moss
    MOSS MOTORS was paid $57.33 on March 03, 2021

### List Transactions
Passing the `ls` argument will list all available transactions (up to the most recent 1000 transactions). Including a number after `ls` will show that many of the most recent transactions. 

    $ ./privacy_inquiry.py ls 3
    -------------------------  -------  ----------
    Vendor                     Amount   Date
    Amazon web services        $6.19    2021-03-06
    MOSS MOTORS                $57.33   2021-03-03
    RACEDAYQUADS               $23.14   2021-03-03
    -------------------------  -------  ----------

### `more` Option
Appending a search by date or search by amount with `m` or `more` will return information in addition to just the merchant, transaction amount, and date. For example:

    $ ./privacy_inquiry.py 2020-04-11 m
    CHIPOTLE ONLINE was paid $8.53 on April 11, 2020
    This transaction is APPROVED and SETTLED
    The card used is named: Chipotle
    CHIPOTLE ONLINE is located in DENVER, CO
