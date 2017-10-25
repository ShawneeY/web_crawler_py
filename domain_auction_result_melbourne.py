from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import sys
import pymysql.cursors
db = pymysql.connect(host='localhost',
                    user='dbUser',
                    password='1234',
                    db='PropertyCrawler',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)

# def prepPriceStringForConversion(value)
#     value = value[1:]
#     value value[:-1]

# def parsePriceFromStringToFloat(value, defaultValue):
#     try:
#         targetPrice = def prepPriceStringForConversion(value)
#         targetPrice = float(targetPrice) * 1000000
#         return "$" + str(targetPrice)
#     except IgnoreException:
#         return defaultValue


my_url = 'https://www.domain.com.au/auction-results/melbourne/'

# opening connection and download the page
uClient = uReq(my_url)

# offload content to a var
page_html = uClient.read()

# close  connection
uClient.close()

# HTML parsing
page_soup = soup(page_html, "html.parser")

# grab suburb based auction details
suburb_transaction_records = page_soup.findAll("div",{"class", "suburb-listings"})

class transactionRecord:

    def __init__(self, suburb, address, price, properttype, result, agent):
        self.suburb = suburb
        self.address = address
        self.price = price
        self.properttype = properttype
        self.result = result
        self.agent = agent


data_retrival_date = page_soup.find('h2',{"class", "sales-results-hero-content__heading"}).text
with db.cursor() as cursor:
    cursor.execute("SELECT `retrieval_date` FROM `weekly_auction_results_from_domain` WHERE `Id`=(SELECT MAX(id) FROM `weekly_auction_results_from_domain`)")
    result = cursor.fetchone()
    if bool(result):
        if str(result['retrieval_date']) == data_retrival_date:
            print("Record up to " + data_retrival_date + " is up to date.")
            db.close()
            sys.exit()
totallen = 0
for suburb_transaction_record in suburb_transaction_records :
    surburb_name = suburb_transaction_record.h6.text
    transactions = suburb_transaction_record.findAll("a",{"class", "auction-details"})
    totallen = len(transactions) + totallen
    for transaction in transactions:
        address = transaction.find("span", {"class", "auction-details__address"}).text
        if transaction.find("span", {"class", "auction-details__failed"}):
            price = transaction.find("span", {"class", "auction-details__price-label"}).text
            result = transaction.find("span", {"class", "auction-details__price"}).text
        else:
            price = transaction.find("span", {"class", "auction-details__price"}).text
            result = transaction.find("span", {"class", "auction-details__price-label"}).text
            if result == "":
                result="Sold"
        propertyType = transaction.find("span", {"class", "auction-details__bedroom"}).text + " br " + transaction.find("span", {"class", "auction-details__property-type"}).text
        agent = transaction.find("span", {"class", "auction-details__agent"}).text
        print("retrieval_date : " + data_retrival_date 
            + " suburb : " + surburb_name
            + " address : " + address
            + " price : " + price
            + " property_type : " + propertyType
            + " result : " + result 
            + "agent : " + agent)
        try:
            with db.cursor() as cursor:
                cursor.execute("INSERT INTO `weekly_auction_results_from_domain`(`retrieval_date`,`suburb`,`address`,`price`,`property_type`,`result`,`agent`) VALUES (%s,%s,%s,%s,%s,%s,%s)",(data_retrival_date,surburb_name,address,price,propertyType,result,agent))
                db.commit()
        except Exception as e: 
            print 'My exception occurred, value:', e   
            db.rollback()
        newRecord = transactionRecord(surburb_name,address,price,propertyType,result,agent)
    
print(str(totallen) + " records from " + data_retrival_date + " have been saved." )
db.close()

# print(transactionRecords)